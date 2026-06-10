"""Fungsi untuk load data, bersihkan data, dan bangun index TF-IDF."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

REQUIRED_COLS = [
    "Nama Tempat Makan",
    "Lokasi Tempat Makan",
    "Nama Menu",
    "Kategori Tempat",
    "Harga",
    "Kategori Harga",
    "Tujuan Makan",
    "Lauk/Bahan Utama",
    "Rasa",
    "Waktu Makan",
]


@st.cache_data
def load_data(path: str | Path) -> pd.DataFrame:
    """Load dan bersihkan dataset menu makanan."""
    path = Path(path)

    if pd.__version__ < "2":
        df = pd.read_csv(path, mangle_dupe_cols=False)
    else:
        df = pd.read_csv(path)

    df.columns = df.columns.str.strip()

    duplicate_time_cols = [col for col in df.columns if col.startswith("Waktu Makan.")]
    if duplicate_time_cols:
        df = df.drop(columns=duplicate_time_cols)

    if isinstance(df.get("Waktu Makan"), pd.DataFrame):
        df["Waktu Makan"] = df["Waktu Makan"].iloc[:, 0]

    for timestamp_col in ["Timestamp", "timestamp"]:
        if timestamp_col in df.columns:
            df = df.drop(columns=[timestamp_col])

    if "Waktu Makan" not in df.columns:
        st.warning(
            "⚠️ Kolom 'Waktu Makan' tidak ditemukan di dataset. "
            "Semua menu akan diperlakukan sebagai 'Makan Siang'."
        )
        df["Waktu Makan"] = "Makan Siang"

    missing_cols = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Kolom wajib tidak ditemukan: {', '.join(missing_cols)}")

    df["Harga"] = (
        df["Harga"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["Harga"] = pd.to_numeric(df["Harga"], errors="coerce")
    df = df.dropna(subset=["Harga", "Nama Menu", "Nama Tempat Makan"])
    df["Harga"] = df["Harga"].astype(int)

    string_cols = df.select_dtypes(include=["object"]).columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()

    df["Waktu Makan"] = df["Waktu Makan"].str.strip()
    df = df.reset_index(drop=True)

    # Kolom ini menjaga mapping ke TF-IDF matrix setelah data difilter.
    df["_source_index"] = df.index
    return df


def build_feature_text(row: pd.Series) -> str:
    """Gabungkan fitur menu menjadi satu teks untuk TF-IDF."""
    parts = [
        str(row.get("Kategori Tempat", "")) * 2,
        str(row.get("Rasa", "")) * 3,
        str(row.get("Lauk/Bahan Utama", "")) * 2,
        str(row.get("Tujuan Makan", "")),
        str(row.get("Lokasi Tempat Makan", "")),
        str(row.get("Waktu Makan", "")),
    ]
    text = " ".join(parts)
    return text.lower().replace("/", " ").replace(",", " ").replace("-", " ")


@st.cache_data
def build_tfidf_index(df: pd.DataFrame):
    """Bangun TF-IDF matrix, vectorizer, scaler harga, dan harga normal."""
    df = df.copy()
    df["feature_text"] = df.apply(build_feature_text, axis=1)

    vectorizer = TfidfVectorizer(
        analyzer="word",
        ngram_range=(1, 2),
        min_df=1,
        sublinear_tf=True,
    )
    tfidf_matrix = vectorizer.fit_transform(df["feature_text"])

    scaler = MinMaxScaler()
    harga_norm = scaler.fit_transform(df[["Harga"]]).flatten()

    return tfidf_matrix, vectorizer, scaler, harga_norm


def filter_by_preference(
    df: pd.DataFrame,
    lokasi: list[str],
    kategori: list[str],
    rasa: list[str],
    pantangan: str,
) -> pd.DataFrame:
    """Hard filter dataset berdasarkan preferensi user."""
    filtered = df.copy()

    if lokasi:
        filtered = filtered[filtered["Lokasi Tempat Makan"].isin(lokasi)]

    if kategori:
        filtered = filtered[filtered["Kategori Tempat"].isin(kategori)]

    if rasa:
        def rasa_match(menu_rasa: str) -> bool:
            menu_rasas = {item.strip() for item in str(menu_rasa).split(",")}
            return bool(menu_rasas & set(rasa))

        filtered = filtered[filtered["Rasa"].apply(rasa_match)]

    if pantangan.strip():
        pantangan_list = [item.strip().lower() for item in pantangan.split(",") if item.strip()]

        def no_pantangan(lauk: str) -> bool:
            return not any(item in str(lauk).lower() for item in pantangan_list)

        filtered = filtered[filtered["Lauk/Bahan Utama"].apply(no_pantangan)]

    return filtered.reset_index(drop=True)
