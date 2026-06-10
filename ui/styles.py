"""CSS global aplikasi."""

import streamlit as st


def get_global_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg: #0f1117;
    --surface: #1a1d27;
    --surface2: #22263a;
    --accent: #f5a623;
    --accent2: #e84393;
    --green: #2dd4bf;
    --blue: #60a5fa;
    --text: #e8eaf0;
    --muted: #7b8099;
    --border: #2a2f45;
    --radius: 14px;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Naikkan konten utama agar judul tidak terlalu ke bawah */
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
}

[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

#MainMenu, footer {
    visibility: hidden;
}

header {
    visibility: visible !important;
    background: transparent !important;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -0.5px;
}

/* Header brand */
.brand-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0 0 18px 0 !important;
    margin-top: -18px !important;
}

.brand-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: -1px;
    line-height: 1.1;
}

.brand-sub {
    font-size: 0.8rem;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Score bar */
.score-bar-wrap {
    margin: 8px 0 12px 0;
}

.score-bar-label {
    font-size: 0.68rem;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    letter-spacing: 1px;
    margin-bottom: 4px;
}

.score-bar-bg {
    background: var(--surface2);
    border-radius: 4px;
    height: 6px;
    width: 100%;
}

.score-bar-fill {
    height: 6px;
    border-radius: 4px;
    background: linear-gradient(90deg, var(--green), var(--blue));
}

/* Meal card */
.meal-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 22px;
    position: relative;
    transition: border-color 0.2s;
    margin-bottom: 6px;
}

.meal-card:hover {
    border-color: var(--accent);
}

.meal-slot-badge {
    display: inline-block;
    background: var(--accent2);
    color: #fff;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 10px;
    font-family: 'DM Mono', monospace;
}

.meal-name {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
}

.meal-place {
    font-size: 0.85rem;
    color: var(--muted);
    margin-bottom: 10px;
}

.meal-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 12px;
}

.tag {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 20px;
    font-size: 0.72rem;
    padding: 3px 10px;
    color: var(--muted);
}

.meal-price {
    font-family: 'DM Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--accent);
}

/* Summary */
.summary-box {
    background: linear-gradient(135deg, #1e2235 0%, #16192b 100%);
    border: 1px solid var(--border);
    border-top: 3px solid var(--green);
    border-radius: var(--radius);
    padding: 24px 28px;
    margin-bottom: 28px;
}

.summary-label {
    font-size: 0.72rem;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.summary-value {
    font-size: 1.7rem;
    font-weight: 700;
    font-family: 'DM Mono', monospace;
    color: var(--green);
}

.summary-value.spent {
    color: var(--accent);
}

/* Boxes */
.tip-box {
    background: var(--surface2);
    border-left: 4px solid var(--accent);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 16px 20px;
    margin-top: 24px;
    font-size: 0.9rem;
    color: var(--text);
    line-height: 1.6;
}

.ai-explain-box {
    background: linear-gradient(135deg, #0f2035 0%, #0a1628 100%);
    border: 1px solid #1e3a5f;
    border-radius: var(--radius);
    padding: 18px 22px;
    margin-top: 20px;
    font-size: 0.83rem;
    color: #93c5fd;
    line-height: 1.7;
}

.ai-explain-box strong {
    color: var(--blue);
}

.empty-state {
    background: var(--surface);
    border: 1px dashed var(--border);
    border-radius: var(--radius);
    padding: 48px 24px;
    text-align: center;
    color: var(--muted);
}

.empty-title {
    font-size: 1.2rem;
    font-weight: 600;
    margin: 12px 0 8px;
    color: var(--text);
}

/* Sidebar */
.sidebar-section {
    font-size: 0.68rem;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 20px 0 6px 0;
    padding-top: 16px;
    border-top: 1px solid var(--border);
}

.sidebar-section:first-of-type {
    border-top: none;
}

.divider-line {
    border: none;
    border-top: 1px solid var(--border);
    margin: 20px 0;
}
</style>
"""


def get_sidebar_button_css() -> str:
    return """
<style>
/* Percobaan target langsung ke tombol bawaan Streamlit */
button[aria-label*="sidebar" i],
button[title*="sidebar" i],
button[data-testid="stSidebarCollapsedControl"],
button[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {
    background: #f5a623 !important;
    border: 2px solid #ffbd4a !important;
    border-radius: 12px !important;
    box-shadow: 0 0 22px rgba(245, 166, 35, 0.65) !important;
}

/* Overlay visual agar tombol sidebar pasti terlihat */
.sidebar-toggle-visual {
    position: fixed !important;
    top: 8px !important;
    left: 10px !important;
    width: 48px !important;
    height: 42px !important;
    z-index: 20 !important;

    background: #f5a623 !important;
    border: 2px solid #ffbd4a !important;
    border-radius: 12px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    box-shadow: 0 0 22px rgba(245, 166, 35, 0.75) !important;
    animation: sidebarButtonPulse 1.4s infinite !important;

    pointer-events: none !important;
}

.sidebar-toggle-visual::before {
    content: "»";
    color: #0f1117 !important;
    font-size: 1.55rem !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    transform: translateY(-1px);
}

.sidebar-toggle-hint {
    position: fixed !important;
    top: 12px !important;
    left: 67px !important;
    z-index: 20 !important;

    background: rgba(26, 29, 39, 0.96) !important;
    border: 1px solid rgba(245, 166, 35, 0.65) !important;
    border-radius: 999px !important;

    height: 34px !important;
    padding: 0 14px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    color: #f5a623 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;

    box-shadow: 0 0 16px rgba(245, 166, 35, 0.22) !important;
    pointer-events: none !important;
}

/* Pastikan sidebar menutup overlay saat dibuka */
[data-testid="stSidebar"] {
    z-index: 999 !important;
}

/* Animasi glow */
@keyframes sidebarButtonPulse {
    0% {
        box-shadow: 0 0 0 0 rgba(245, 166, 35, 0.75);
    }
    70% {
        box-shadow: 0 0 0 11px rgba(245, 166, 35, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(245, 166, 35, 0);
    }
}
</style>
"""


def apply_global_styles() -> None:
    st.markdown(get_global_css(), unsafe_allow_html=True)
    st.markdown(get_sidebar_button_css(), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="sidebar-toggle-visual"></div>
        <div class="sidebar-toggle-hint">Buka Preferensi</div>
        """,
        unsafe_allow_html=True,
    )