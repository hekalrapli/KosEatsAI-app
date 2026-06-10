"""Algoritma rekomendasi Content-Based Filtering untuk KosEats AI."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from config import BUDGET_THRESHOLD, SLOTS, WEIGHT_PRICE, WEIGHT_TEXT


def build_user_query(
    rasa: list[str],
    kategori: list[str],
    lokasi: list[str],
    slot: str,
    pantangan: str,
) -> str:
    """Bangun query teks dari preferensi user untuk satu slot makan."""
    parts: list[str] = []

    if rasa:
        parts += [" ".join(rasa)] * 3
    if kategori:
        parts += [" ".join(kategori)] * 2
    if lokasi:
        parts.append(" ".join(lokasi))

    parts.append(slot)

    query = " ".join(parts)
    return query.lower().replace("/", " ").replace(",", " ")


def _get_source_ids(df: pd.DataFrame) -> pd.Series:
    """Ambil ID asli menu agar tetap stabil setelah DataFrame difilter."""
    if "_source_index" in df.columns:
        return df["_source_index"].astype(int)

    return pd.Series(df.index.astype(int), index=df.index)


def score_menus_for_slot(
    df_full: pd.DataFrame,
    df_filtered: pd.DataFrame,
    tfidf_matrix,
    vectorizer,
    harga_norm: np.ndarray,
    user_query: str,
    budget_per_slot: int,
    prefer_expensive: bool = False,
) -> pd.DataFrame:
    """Hitung skor rekomendasi untuk kandidat menu pada satu slot makan."""
    if df_filtered.empty or budget_per_slot <= 0:
        return df_filtered.iloc[0:0].copy()

    source_indices = _get_source_ids(df_filtered).tolist()

    query_vec = vectorizer.transform([user_query])
    tfidf_sub = tfidf_matrix[source_indices]
    text_sim = cosine_similarity(query_vec, tfidf_sub).flatten()

    harga_abs = df_filtered["Harga"].values.astype(float)
    in_budget = harga_abs <= budget_per_slot

    if prefer_expensive:
        price_score = np.where(in_budget, harga_abs / budget_per_slot, 0.0)
        text_weight = 0.55
        price_weight = 0.45
    else:
        price_score = np.where(in_budget, 1.0 - (harga_abs / budget_per_slot), 0.0)
        text_weight = WEIGHT_TEXT
        price_weight = WEIGHT_PRICE

    final_score = text_weight * text_sim + price_weight * price_score

    result = df_filtered.copy()
    result["similarity_score"] = np.round(text_sim, 4)
    result["price_score"] = np.round(price_score, 4)
    result["final_score"] = np.round(final_score, 4)

    result = result[result["Harga"] <= budget_per_slot]
    return result.sort_values("final_score", ascending=False).reset_index(drop=True)


def _base_slot_pool(df_filtered: pd.DataFrame, slot: str) -> pd.DataFrame:
    """Ambil kandidat berdasarkan waktu makan. Jika kosong, pakai semua kandidat."""
    if "Waktu Makan" not in df_filtered.columns:
        df_filtered = df_filtered.copy()
        df_filtered["Waktu Makan"] = "Makan Siang"

    slot_df = df_filtered[df_filtered["Waktu Makan"] == slot].copy()

    if slot_df.empty:
        slot_df = df_filtered.copy()

    return slot_df


def _apply_exclusions(
    df: pd.DataFrame,
    used_places: set[str],
    used_menus: set[str],
    excluded_menu_ids: set[int],
) -> pd.DataFrame:
    """Kurangi kandidat agar hasil tidak terlalu sering mengulang."""
    if df.empty:
        return df

    candidate = df.copy()

    if used_places:
        new_place = candidate[~candidate["Nama Tempat Makan"].isin(used_places)]
        if not new_place.empty:
            candidate = new_place

    if used_menus:
        new_menu = candidate[~candidate["Nama Menu"].isin(used_menus)]
        if not new_menu.empty:
            candidate = new_menu

    if excluded_menu_ids:
        source_ids = _get_source_ids(candidate)
        fresh_candidate = candidate[~source_ids.isin(excluded_menu_ids)]

        if not fresh_candidate.empty:
            candidate = fresh_candidate

    return candidate.reset_index(drop=True)


def _min_budget_for_remaining_slots(
    df_filtered: pd.DataFrame,
    remaining_slots: list[str],
    used_places: set[str],
    used_menus: set[str],
    excluded_menu_ids: set[int],
) -> int | None:
    """Hitung dana minimum yang harus disisakan untuk slot berikutnya."""
    minimum_total = 0

    for slot in remaining_slots:
        pool = _base_slot_pool(df_filtered, slot)
        pool = _apply_exclusions(
            df=pool,
            used_places=used_places,
            used_menus=used_menus,
            excluded_menu_ids=excluded_menu_ids,
        )

        if pool.empty:
            pool = _base_slot_pool(df_filtered, slot)
            pool = _apply_exclusions(
                df=pool,
                used_places=used_places,
                used_menus=used_menus,
                excluded_menu_ids=set(),
            )

        if pool.empty:
            return None

        minimum_total += int(pool["Harga"].min())

    return minimum_total


def _choose_candidate(
    scored: pd.DataFrame,
    randomize: bool,
    candidate_pool_size: int,
    rng: np.random.Generator,
    prefer_expensive: bool,
) -> pd.Series:
    """Pilih menu dari kandidat yang lebih luas, bukan hanya Top-5."""
    if scored.empty:
        raise ValueError("Tidak ada kandidat untuk dipilih.")

    if not randomize or len(scored) == 1:
        return scored.iloc[0]

    adaptive_pool_size = max(
        candidate_pool_size,
        int(math.ceil(len(scored) * 0.35)),
    )
    adaptive_pool_size = min(len(scored), adaptive_pool_size)

    pool = scored.head(adaptive_pool_size).copy()

    if prefer_expensive and len(pool) >= 4:
        premium_limit = pool["Harga"].quantile(0.50)
        premium_pool = pool[pool["Harga"] >= premium_limit].copy()

        if len(premium_pool) >= 3:
            pool = premium_pool.reset_index(drop=True)

    weights = pool["final_score"].astype(float).to_numpy()
    weights = weights - weights.min()

    if weights.sum() <= 0:
        weights = np.ones(len(pool), dtype=float)
    else:
        weights = weights + 0.001

    weights = weights / weights.sum()
    chosen_position = int(rng.choice(len(pool), p=weights))

    return pool.iloc[chosen_position]


def _build_one_package(
    df_full: pd.DataFrame,
    df_filtered: pd.DataFrame,
    tfidf_matrix,
    vectorizer,
    harga_norm: np.ndarray,
    rasa: list[str],
    kategori: list[str],
    lokasi: list[str],
    pantangan: str,
    budget: int,
    randomize: bool,
    active_slots: list[str],
    excluded_menu_ids: set[int],
    candidate_pool_size: int,
    rng: np.random.Generator,
) -> tuple[dict, dict] | None:
    """Bangun satu paket makan dengan total harga tetap aman."""
    result: dict = {}
    scores_info: dict = {}
    used_places: set[str] = set()
    used_menus: set[str] = set()

    prefer_expensive = budget > BUDGET_THRESHOLD

    for index, slot in enumerate(active_slots):
        remaining_slots = active_slots[index + 1:]
        spent_so_far = sum(int(row["Harga"]) for row in result.values())
        remaining_budget = budget - spent_so_far

        min_remaining = _min_budget_for_remaining_slots(
            df_filtered=df_filtered,
            remaining_slots=remaining_slots,
            used_places=used_places,
            used_menus=used_menus,
            excluded_menu_ids=excluded_menu_ids,
        )

        if min_remaining is None:
            return None

        budget_for_current_slot = remaining_budget - min_remaining

        if budget_for_current_slot <= 0:
            return None

        slot_df = _base_slot_pool(df_filtered, slot)
        slot_df = _apply_exclusions(
            df=slot_df,
            used_places=used_places,
            used_menus=used_menus,
            excluded_menu_ids=excluded_menu_ids,
        )

        if slot_df.empty:
            slot_df = _base_slot_pool(df_filtered, slot)
            slot_df = _apply_exclusions(
                df=slot_df,
                used_places=used_places,
                used_menus=used_menus,
                excluded_menu_ids=set(),
            )

        if slot_df.empty:
            return None

        user_query = build_user_query(rasa, kategori, lokasi, slot, pantangan)

        scored = score_menus_for_slot(
            df_full=df_full,
            df_filtered=slot_df,
            tfidf_matrix=tfidf_matrix,
            vectorizer=vectorizer,
            harga_norm=harga_norm,
            user_query=user_query,
            budget_per_slot=budget_for_current_slot,
            prefer_expensive=prefer_expensive,
        )

        if scored.empty and excluded_menu_ids:
            relaxed_df = _base_slot_pool(df_filtered, slot)
            relaxed_df = _apply_exclusions(
                df=relaxed_df,
                used_places=used_places,
                used_menus=used_menus,
                excluded_menu_ids=set(),
            )

            scored = score_menus_for_slot(
                df_full=df_full,
                df_filtered=relaxed_df,
                tfidf_matrix=tfidf_matrix,
                vectorizer=vectorizer,
                harga_norm=harga_norm,
                user_query=user_query,
                budget_per_slot=budget_for_current_slot,
                prefer_expensive=prefer_expensive,
            )

        if scored.empty:
            return None

        chosen = _choose_candidate(
            scored=scored,
            randomize=randomize,
            candidate_pool_size=candidate_pool_size,
            rng=rng,
            prefer_expensive=prefer_expensive,
        )

        result[slot] = chosen
        scores_info[slot] = {
            "similarity_score": float(chosen["similarity_score"]),
            "price_score": float(chosen["price_score"]),
            "final_score": float(chosen["final_score"]),
            "budget_slot": int(budget_for_current_slot),
            "candidate_pool_count": min(
                len(scored),
                max(candidate_pool_size, int(math.ceil(len(scored) * 0.35))),
            ),
            "available_candidate_count": int(len(scored)),
        }

        used_places.add(str(chosen["Nama Tempat Makan"]))
        used_menus.add(str(chosen["Nama Menu"]))

    total = sum(int(row["Harga"]) for row in result.values())

    if total > budget:
        return None

    return result, scores_info


def recommend_daily_package_cbf(
    df_full: pd.DataFrame,
    df_filtered: pd.DataFrame,
    tfidf_matrix,
    vectorizer,
    harga_norm: np.ndarray,
    rasa: list[str],
    kategori: list[str],
    lokasi: list[str],
    pantangan: str,
    budget: int,
    randomize: bool = False,
    top_k: int = 5,
    active_slots: list[str] | None = None,
    excluded_menu_ids: Iterable[int] | None = None,
    candidate_pool_size: int = 35,
    max_attempts: int = 80,
    random_seed: int | None = None,
) -> tuple[dict, dict] | None:
    """Rekomendasikan paket makan harian sesuai slot pilihan user."""
    if active_slots is None:
        active_slots = SLOTS

    if df_filtered.empty:
        return None

    excluded_set = {
        int(item)
        for item in (excluded_menu_ids or [])
        if item is not None
    }

    attempts = max_attempts if randomize else 1
    rng = np.random.default_rng(random_seed)

    candidate_pool_size = max(candidate_pool_size, top_k)

    for attempt in range(attempts):
        if attempt < max(1, int(attempts * 0.75)):
            active_excluded = excluded_set
        else:
            active_excluded = set()

        package = _build_one_package(
            df_full=df_full,
            df_filtered=df_filtered,
            tfidf_matrix=tfidf_matrix,
            vectorizer=vectorizer,
            harga_norm=harga_norm,
            rasa=rasa,
            kategori=kategori,
            lokasi=lokasi,
            pantangan=pantangan,
            budget=budget,
            randomize=randomize,
            active_slots=active_slots,
            excluded_menu_ids=active_excluded,
            candidate_pool_size=candidate_pool_size,
            rng=rng,
        )

        if package is not None:
            return package

    return None