"""Komponen sidebar untuk input preferensi user."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config import WAKTU_OPTIONS


def render_sidebar(df: pd.DataFrame, vectorizer) -> dict:
    """Render sidebar dan kembalikan semua input user dalam dict."""
    with st.sidebar:
        st.markdown("## ⚙️ Preferensi Kamu")
        st.caption("Atur filter → tekan **Cari Paket Makan** untuk rekomendasi berbasis AI.")

        st.markdown('<div class="sidebar-section">💰 Budget Harian</div>', unsafe_allow_html=True)
        budget = st.slider(
            "Total Budget Makan Hari Ini",
            min_value=10_000,
            max_value=100_000,
            value=40_000,
            step=1_000,
            format="Rp %d",
            help="Menu yang direkomendasikan akan selalu <= budget ini.",
        )

        st.markdown('<div class="sidebar-section">🕐 Waktu Makan</div>', unsafe_allow_html=True)
        selected_waktu_label = st.selectbox(
            "Pilih Waktu Makan",
            options=list(WAKTU_OPTIONS.keys()),
            index=6,
        )
        selected_slots = WAKTU_OPTIONS[selected_waktu_label]

        st.markdown('<div class="sidebar-section">📍 Lokasi</div>', unsafe_allow_html=True)
        all_lokasi = sorted(df["Lokasi Tempat Makan"].dropna().unique().tolist())
        selected_lokasi = st.multiselect(
            "Lokasi Tempat Makan",
            options=all_lokasi,
            default=[],
            placeholder="Semua lokasi",
        )

        st.markdown('<div class="sidebar-section">🏪 Kategori Tempat</div>', unsafe_allow_html=True)
        all_kategori = sorted(df["Kategori Tempat"].dropna().unique().tolist())
        selected_kategori = st.multiselect(
            "Jenis Warung / Restoran",
            options=all_kategori,
            default=[],
            placeholder="Semua kategori",
        )

        st.markdown('<div class="sidebar-section">👅 Preferensi Rasa</div>', unsafe_allow_html=True)
        all_rasa = sorted(df["Rasa"].dropna().unique().tolist())
        selected_rasa = st.multiselect(
            "Pilih Rasa Favorit",
            options=all_rasa,
            default=[],
            placeholder="Semua rasa",
        )

        st.markdown('<div class="sidebar-section">🚫 Pantangan Bahan</div>', unsafe_allow_html=True)
        pantangan_input = st.text_input(
            "Bahan yang Ingin Dihindari",
            value="",
            placeholder="Contoh: Mie, Seafood, Daging Sapi",
            help="Pisahkan dengan koma. Sistem menyaring kolom Lauk/Bahan Utama.",
        )

      
        randomize = True
        show_ai_detail = False

        st.markdown("<hr class='divider-line'>", unsafe_allow_html=True)
        cari_btn = st.button("🍽️ Cari Paket Makan Hari Ini", type="primary", use_container_width=True)

        if cari_btn:
            st.session_state["has_searched"] = True
            st.session_state["reroll_count"] = st.session_state.get("reroll_count", 0) + 1
            st.session_state["recent_menu_ids"] = []
        st.markdown("<hr class='divider-line'>", unsafe_allow_html=True)
        st.caption(f"📊 Dataset: **{len(df)} menu** dari **{df['Nama Tempat Makan'].nunique()} tempat makan**.")
        # st.caption(f"🔤 Vocab TF-IDF: **{len(vectorizer.vocabulary_)} term**")

    return {
        "budget": budget,
        "selected_slots": selected_slots,
        "selected_lokasi": selected_lokasi,
        "selected_kategori": selected_kategori,
        "selected_rasa": selected_rasa,
        "pantangan_input": pantangan_input,
        "randomize": randomize,
        "show_ai_detail": show_ai_detail,
        "cari_btn": cari_btn,
    }
