"""Komponen UI untuk hasil rekomendasi."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config import SLOT_ICONS
from services.finance import get_financial_tip


def render_brand_header() -> None:
    st.markdown(
        """
    <div class="brand-header">
        <span style="font-size:2.4rem">🍱</span>
        <div>
            <div class="brand-title">KosEats AI</div>
            <div class="brand-sub">Smart Budget Meal Planner • Tanpa Boncos Edition</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_empty_state(budget: int, selected_slots: list[str], df_filtered: pd.DataFrame) -> None:
    st.markdown(
        f"""
        <div class="empty-state">
            <div style="font-size:3rem">😔</div>
            <div class="empty-title">Tidak Ditemukan Paket yang Sesuai</div>
            <p style="font-size:0.88rem; max-width:420px; margin:0 auto;">
                Budget <strong>Rp {budget:,}</strong> tidak cukup untuk kombinasi menu
                dengan filter saat ini. Coba:
            </p>
            <ul style="text-align:left; display:inline-block; margin-top:12px; font-size:0.85rem;">
                <li>Naikkan slider budget</li>
                <li>Kurangi filter lokasi / kategori / rasa</li>
                <li>Hapus bahan pantangan</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    min_per_slot = []
    for slot in selected_slots:
        pool = df_filtered[df_filtered["Waktu Makan"] == slot]
        if pool.empty:
            pool = df_filtered
        if not pool.empty:
            min_per_slot.append(int(pool["Harga"].min()))

    if min_per_slot:
        st.info(f"💡 Estimasi budget minimum saat ini: **Rp {sum(min_per_slot):,}**")


def render_summary_cards(budget: int, total_spent: int, sisa: int) -> None:
    col_budget, col_spent, col_saved = st.columns(3)

    with col_budget:
        st.markdown(
            f"""
        <div class="summary-box">
            <div class="summary-label">💰 Budget Harian</div>
            <div class="summary-value spent">Rp {budget:,}</div>
        </div>""",
            unsafe_allow_html=True,
        )

    with col_spent:
        st.markdown(
            f"""
        <div class="summary-box">
            <div class="summary-label">🛒 Total Pengeluaran</div>
            <div class="summary-value spent">Rp {total_spent:,}</div>
        </div>""",
            unsafe_allow_html=True,
        )

    with col_saved:
        st.markdown(
            f"""
        <div class="summary-box">
            <div class="summary-label">✨ Berhasil Dihemat</div>
            <div class="summary-value">Rp {sisa:,}</div>
        </div>""",
            unsafe_allow_html=True,
        )


def _build_score_bar(sinfo: dict, show_ai_detail: bool) -> str:
    if not show_ai_detail:
        return ""

    score_pct = int(sinfo["final_score"] * 100)
    sim_pct = int(sinfo["similarity_score"] * 100)

    return (
        '<div class="score-bar-wrap">'
        '<div class="score-bar-label">Skor Kecocokan AI: '
        + str(score_pct)
        + '&#37; &nbsp;(similarity: '
        + str(sim_pct)
        + '&#37;)</div>'
        '<div class="score-bar-bg">'
        '<div class="score-bar-fill" style="width:'
        + str(score_pct)
        + '&#37;"></div>'
        '</div>'
        '</div>'
    )


def render_meal_cards(result: dict, scores_info: dict, selected_slots: list[str], show_ai_detail: bool) -> None:
    st.markdown("### 📋 Paket Makan Hari Ini")
    cols = st.columns(len(selected_slots))

    for idx, slot in enumerate(selected_slots):
        if slot not in result:
            continue

        row = result[slot]
        sinfo = scores_info[slot]
        icon = SLOT_ICONS.get(slot, "🍽️")
        lauk = str(row.get("Lauk/Bahan Utama", "-"))
        rasa = str(row.get("Rasa", "-"))

        tag_items = [
            f'<span class="tag">📍 {row["Lokasi Tempat Makan"]}</span>',
            f'<span class="tag">🏷️ {row["Kategori Tempat"]}</span>',
            f'<span class="tag">👅 {rasa}</span>',
        ]

        for bahan in lauk.split(",")[:3]:
            bahan = bahan.strip()
            if bahan:
                tag_items.append(f'<span class="tag">🥩 {bahan}</span>')

        tags_html = "".join(tag_items)
        score_bar = _build_score_bar(sinfo, show_ai_detail)

        with cols[idx]:
            card_html = (
                '<div class="meal-card">'
                '<div class="meal-slot-badge">'
                + icon
                + ' '
                + slot.upper()
                + '</div>'
                '<div class="meal-name">'
                + str(row["Nama Menu"])
                + '</div>'
                '<div class="meal-place">🏠 '
                + str(row["Nama Tempat Makan"])
                + '</div>'
                '<div class="meal-tags">'
                + tags_html
                + '</div>'
                + score_bar
                + '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
            st.markdown(
                f'<div class="meal-price" style="padding:0 22px 16px 22px;margin-top:-10px;">Rp {int(row["Harga"]):,}</div>',
                unsafe_allow_html=True,
            )

def _reroll_recommendation() -> None:
    """Jalankan ulang rekomendasi dengan menu yang lebih variatif."""
    st.session_state["has_searched"] = True
    st.session_state["reroll_count"] = st.session_state.get("reroll_count", 0) + 1


def render_reroll_button() -> None:
    """Tampilkan tombol untuk mencari kombinasi menu lain."""
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    col_left, col_button, col_right = st.columns([1.4, 1, 1.4])

    with col_button:
        st.button(
            "🔀 Cari Lagi / Acak",
            key="reroll_button",
            type="primary",
            use_container_width=True,
            on_click=_reroll_recommendation,
            help="Cari kombinasi menu lain dari kandidat yang masih sesuai budget dan filter.",
        )

    st.markdown(
        """
        <div style="text-align:center; color:var(--muted); font-size:0.8rem; margin-top:4px; margin-bottom:18px;">
            Sistem akan mencoba menu lain dan menghindari menu yang baru saja muncul.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_financial_tip(sisa: int, budget: int) -> None:
    tip_icon, tip_msg = get_financial_tip(sisa, budget)
    st.markdown(
        f"""
    <div class="tip-box">
        <span style="font-size:1.1rem; margin-right:8px;">{tip_icon}</span>
        <strong>Tips Finansial Hari Ini:</strong><br>
        {tip_msg}
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_ai_explanation(result: dict, scores_info: dict, selected_slots: list[str]) -> None:
    with st.expander("🧠 Bagaimana AI Memilih Menu Ini?"):
        st.markdown(
            """
            <div class="ai-explain-box">
            <strong>Algoritma: Content-Based Filtering dengan TF-IDF + Cosine Similarity</strong><br><br>
            <strong>1. Feature Engineering</strong><br>
            Setiap menu direpresentasikan sebagai teks gabungan dari kolom:
            Kategori Tempat, Rasa (bobot ×3), Lauk/Bahan Utama (bobot ×2), Tujuan Makan, Lokasi, dan Waktu Makan.<br><br>
            <strong>2. TF-IDF Vectorization</strong><br>
            Seluruh menu di dataset di-vectorize menggunakan <em>Term Frequency-Inverse Document Frequency</em>.
            Digunakan n-gram (1,2) untuk menangkap frasa seperti "asin gurih" atau "ayam goreng".<br><br>
            <strong>3. Query Vector</strong><br>
            Preferensi user diubah menjadi query teks lalu di-transform menggunakan TF-IDF yang sama.<br><br>
            <strong>4. Cosine Similarity</strong><br>
            Nilai mendekati 1.0 berarti menu semakin mirip dengan preferensi user.<br><br>
            <strong>5. Budget-Aware Scoring</strong><br>
            Skor akhir = <strong>0.70 × text_similarity + 0.30 × price_efficiency</strong>.<br><br>
            <strong>6. Budget Filtering</strong><br>
            Menu yang direkomendasikan selalu berada di bawah budget yang user pilih.
            </div>
            """,
            unsafe_allow_html=True,
        )

        score_rows = []
        for slot in selected_slots:
            if slot not in result:
                continue
            row = result[slot]
            sinfo = scores_info[slot]
            score_rows.append(
                {
                    "Slot": f"{SLOT_ICONS[slot]} {slot}",
                    "Menu Terpilih": row["Nama Menu"],
                    "Cosine Similarity": f"{sinfo['similarity_score']:.4f}",
                    "Price Score": f"{sinfo['price_score']:.4f}",
                    "Final Score": f"{sinfo['final_score']:.4f}",
                    "Kandidat Top-K": sinfo["top_k_count"],
                    "Harga": f"Rp {row['Harga']:,}",
                }
            )

        st.dataframe(pd.DataFrame(score_rows), use_container_width=True, hide_index=True)


def render_package_detail(result: dict, selected_slots: list[str]) -> None:
    with st.expander("📊 Lihat Detail Lengkap Paket"):
        rows_data = []
        for slot in selected_slots:
            if slot not in result:
                continue
            row = result[slot]
            rows_data.append(
                {
                    "Waktu": f"{SLOT_ICONS.get(slot, '')} {slot}",
                    "Nama Menu": row["Nama Menu"],
                    "Tempat Makan": row["Nama Tempat Makan"],
                    "Lokasi": row["Lokasi Tempat Makan"],
                    "Kategori": row["Kategori Tempat"],
                    "Harga": f"Rp {row['Harga']:,}",
                    "Rasa": row["Rasa"],
                    "Lauk/Bahan": row["Lauk/Bahan Utama"],
                    "Tujuan": row.get("Tujuan Makan", "-"),
                }
            )
        st.dataframe(pd.DataFrame(rows_data), use_container_width=True, hide_index=True)


def render_footer(vectorizer, df_filtered: pd.DataFrame, df_full: pd.DataFrame) -> None:
    st.markdown(
        f"""
    """,
        unsafe_allow_html=True,
    )
