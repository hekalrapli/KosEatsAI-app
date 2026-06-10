"""Entry point aplikasi KosEats AI."""

import streamlit as st

from config import DATASET_PATH, LAYOUT, PAGE_ICON, PAGE_TITLE, SIDEBAR_STATE
from services.data_service import build_tfidf_index, filter_by_preference, load_data
from services.recommender import recommend_daily_package_cbf
from ui.home import render_home
from ui.results import (
    render_ai_explanation,
    render_brand_header,
    render_empty_state,
    render_financial_tip,
    render_footer,
    render_meal_cards,
    render_package_detail,
    render_reroll_button,
    render_summary_cards,
    
)
from ui.sidebar import render_sidebar
from ui.styles import apply_global_styles


st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE,
)


def main() -> None:
    apply_global_styles()

    try:
        df = load_data(DATASET_PATH)
    except FileNotFoundError:
        st.error(f"❌ File `{DATASET_PATH.name}` tidak ditemukan. Pastikan berada di folder yang sama dengan `app.py`.")
        st.stop()
    except ValueError as exc:
        st.error(f"❌ Dataset belum sesuai format: {exc}")
        st.stop()

    tfidf_matrix, vectorizer, harga_scaler, harga_norm = build_tfidf_index(df)

    render_brand_header()
    user_input = render_sidebar(df, vectorizer)
    filter_signature = (
    user_input["budget"],
    tuple(user_input["selected_slots"]),
    tuple(user_input["selected_lokasi"]),
    tuple(user_input["selected_kategori"]),
    tuple(user_input["selected_rasa"]),
    user_input["pantangan_input"],
    )

    if st.session_state.get("last_filter_signature") != filter_signature:
        st.session_state["recent_menu_ids"] = []
        st.session_state["last_filter_signature"] = filter_signature

    if not st.session_state.get("has_searched", False):
        render_home()
        return

    df_filtered = filter_by_preference(
        df=df,
        lokasi=user_input["selected_lokasi"],
        kategori=user_input["selected_kategori"],
        rasa=user_input["selected_rasa"],
        pantangan=user_input["pantangan_input"],
    )

    cbf_result = recommend_daily_package_cbf(
    df_full=df,
    df_filtered=df_filtered,
    tfidf_matrix=tfidf_matrix,
    vectorizer=vectorizer,
    harga_norm=harga_norm,
    rasa=user_input["selected_rasa"],
    kategori=user_input["selected_kategori"],
    lokasi=user_input["selected_lokasi"],
    pantangan=user_input["pantangan_input"],
    budget=user_input["budget"],
    randomize=user_input["randomize"],
    top_k=5,
    active_slots=user_input["selected_slots"],
    excluded_menu_ids=st.session_state.get("recent_menu_ids", []),
    candidate_pool_size=35,
    max_attempts=100,
    random_seed=st.session_state.get("reroll_count", 0),
)

    if cbf_result is None:
        render_empty_state(
        budget=user_input["budget"],
        df_filtered=df_filtered,
        selected_slots=user_input["selected_slots"],
        )

        render_reroll_button()

        return

    result, scores_info = cbf_result
    total_spent = sum(row["Harga"] for row in result.values())
    sisa = user_input["budget"] - total_spent
    selected_menu_ids = [
    int(row["_source_index"])
    for row in result.values()
    if "_source_index" in row
    ]

    recent_menu_ids = st.session_state.get("recent_menu_ids", [])
    recent_menu_ids.extend(selected_menu_ids)

# Simpan 36 menu terakhir agar klik acak berikutnya tidak itu-itu saja
    st.session_state["recent_menu_ids"] = recent_menu_ids[-36:]

    render_summary_cards(user_input["budget"], total_spent, sisa)
    render_meal_cards(result, scores_info, user_input["selected_slots"], user_input["show_ai_detail"])
    render_reroll_button()
    render_financial_tip(sisa, user_input["budget"])

    if user_input["show_ai_detail"]:
        render_ai_explanation(result, scores_info, user_input["selected_slots"])

    render_package_detail(result, user_input["selected_slots"])
    render_footer(vectorizer, df_filtered, df)


if __name__ == "__main__":
    main()
