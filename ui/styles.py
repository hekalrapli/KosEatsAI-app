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
/* Tombol buka sidebar: dibuat lebih mencolok */
button[aria-label="Open sidebar"],
button[title="Open sidebar"],
button[aria-label="Show sidebar"],
button[title="Show sidebar"],
[data-testid="stSidebarCollapsedControl"] button,
[data-testid="collapsedControl"] button {
    background: #f5a623 !important;
    border: 2px solid #ffbd4a !important;
    border-radius: 12px !important;
    width: 44px !important;
    height: 44px !important;
    padding: 8px !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    box-shadow: 0 0 20px rgba(245, 166, 35, 0.55) !important;
    animation: sidebarButtonPulse 1.5s infinite !important;
    transition: all 0.2s ease !important;
}

/* Warna icon panah */
button[aria-label="Open sidebar"] svg,
button[title="Open sidebar"] svg,
button[aria-label="Show sidebar"] svg,
button[title="Show sidebar"] svg,
[data-testid="stSidebarCollapsedControl"] button svg,
[data-testid="collapsedControl"] button svg {
    color: #0f1117 !important;
    fill: #0f1117 !important;
    stroke: #0f1117 !important;
    width: 24px !important;
    height: 24px !important;
}

/* Paksa path icon ikut berubah warna */
button[aria-label="Open sidebar"] svg path,
button[title="Open sidebar"] svg path,
button[aria-label="Show sidebar"] svg path,
button[title="Show sidebar"] svg path,
[data-testid="stSidebarCollapsedControl"] button svg path,
[data-testid="collapsedControl"] button svg path {
    fill: #0f1117 !important;
    stroke: #0f1117 !important;
}

/* Hover */
button[aria-label="Open sidebar"]:hover,
button[title="Open sidebar"]:hover,
button[aria-label="Show sidebar"]:hover,
button[title="Show sidebar"]:hover,
[data-testid="stSidebarCollapsedControl"] button:hover,
[data-testid="collapsedControl"] button:hover {
    background: #ffbd4a !important;
    transform: scale(1.08) !important;
    box-shadow: 0 0 28px rgba(245, 166, 35, 0.8) !important;
}

/* Animasi agar user sadar tombol bisa diklik */
@keyframes sidebarButtonPulse {
    0% {
        box-shadow: 0 0 0 0 rgba(245, 166, 35, 0.65);
    }
    70% {
        box-shadow: 0 0 0 10px rgba(245, 166, 35, 0);
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