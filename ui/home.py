"""Tampilan awal aplikasi KosEats AI."""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components


def render_home() -> None:
    """Render halaman awal sebelum user mencari paket makan."""

    st.markdown(
        """
        <div style="
            max-width: 900px;
            margin: 0 auto 22px auto;
            padding: 18px 22px;
            background: linear-gradient(135deg, #1e2235 0%, #151824 100%);
            border: 1px solid #2a2f45;
            border-left: 5px solid #f5a623;
            border-radius: 16px;
            text-align: center;
        ">
            <div style="font-size:1.05rem; font-weight:700; color:#f5a623; margin-bottom:6px;">
                Mulai dari sini 👇
            </div>
            <div style="font-size:0.95rem; color:#e8eaf0; line-height:1.7;">
                Klik tombol <b>Cari Paket Makan Sekarang</b> untuk langsung mendapat rekomendasi menu.
                Kalau mau lebih spesifik, atur budget, lokasi, rasa, dan pantangan bahan di sidebar kiri.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1.2, 1, 1.2])
    with c2:
        if st.button(
            "🍽️ Cari Paket Makan Sekarang",
            type="primary",
            use_container_width=True,
            key="home_search_button",
        ):
            st.session_state["has_searched"] = True
            st.session_state["reroll_count"] = st.session_state.get("reroll_count", 0) + 1
            st.session_state["recent_menu_ids"] = []
            st.rerun()

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#7b8099;
            font-size:0.82rem;
            margin-top:8px;
            margin-bottom:22px;
        ">
            Tips: buka sidebar kiri untuk mengubah preferensi sebelum mencari menu.
        </div>
        """,
        unsafe_allow_html=True,
    )

    components.html(
        """
<!DOCTYPE html>
<html>
<head>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: transparent;
    font-family: 'Source Sans Pro', 'Segoe UI', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
  }
  .tagline {
    font-size: 0.8rem;
    color: #888;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 32px;
    font-weight: 500;
  }
  .typing-wrapper {
    min-height: 90px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 100%;
    max-width: 720px;
    margin-bottom: 42px;
  }
  #typing-output {
    font-size: 1.3rem;
    line-height: 1.75;
    color: #f5a623;
    font-weight: 600;
    text-align: center;
    display: inline;
    text-shadow: 0 0 14px rgba(245, 166, 35, 0.18);
  }
  #typing-cursor {
    display: inline-block;
    width: 2px;
    height: 1.2em;
    background: #f5a623;
    margin-left: 3px;
    vertical-align: middle;
    animation: blink 0.9s step-end infinite;
  }
  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
  }
  .hero-stats {
    display: flex;
    justify-content: center;
    gap: 36px;
    flex-wrap: wrap;
    opacity: 0;
    animation: fadeUp 0.8s ease 0.5s forwards;
    margin-bottom: 30px;
  }
  .hero-stat { text-align: center; }
  .hero-stat .num { font-size: 1.5rem; display: block; margin-bottom: 6px; }
  .hero-stat .lbl {
    font-size: 0.72rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  .hero-hint {
    font-size: 0.85rem;
    color: #666;
    opacity: 0;
    animation: fadeUp 0.8s ease 1s forwards;
    text-align: center;
  }
  .hero-hint strong { color: #f5a623; }
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
</style>
</head>
<body>
  <div class="tagline">untuk mahasiswa, dari mahasiswa</div>

  <div class="typing-wrapper">
    <span id="typing-output"></span><span id="typing-cursor"></span>
  </div>

  <div class="hero-stats">
    <div class="hero-stat"><span class="num">💸</span><span class="lbl">Hemat Budget</span></div>
    <div class="hero-stat"><span class="num">🍽️</span><span class="lbl">Menu Variatif</span></div>
    <div class="hero-stat"><span class="num">📍</span><span class="lbl">Sesuai Lokasi</span></div>
    <div class="hero-stat"><span class="num">⚡</span><span class="lbl">Rekomendasi AI</span></div>
  </div>

  <div class="hero-hint">
    Atur preferensi di sidebar kiri, atau langsung klik tombol cari di atas.
  </div>

  <script>
    const lines = [
      "Bingung mau makan apa hari ini?",
      "Uang saku mepet, tapi tetap mau makan enak?",
      "Capek pesan ojol terus dan dompet makin tipis?",
      "Sering pilih menu yang itu-itu saja?",
      "KosEats AI bantu kamu cari menu harian yang pas di kantong, sesuai selera, dan anti bosan. Setiap hari! 🍱"
    ];

    const el = document.getElementById('typing-output');
    const cur = document.getElementById('typing-cursor');

    let lineIdx = 0;
    let charIdx = 0;
    let isDeleting = false;
    let pause = 0;
    const PAUSE_HOLD = 40;

    function tick() {
      const line = lines[lineIdx];

      if (!isDeleting) {
        el.textContent = line.substring(0, charIdx);
        charIdx++;

        if (charIdx > line.length) {
          pause++;

          if (pause < PAUSE_HOLD) {
            setTimeout(tick, 55);
            return;
          }

          pause = 0;
          isDeleting = true;
        }

        setTimeout(tick, 48);
      } else {
        el.textContent = line.substring(0, charIdx);
        charIdx--;

        if (charIdx < 0) {
          isDeleting = false;
          charIdx = 0;
          lineIdx = (lineIdx + 1) % lines.length;

          setTimeout(tick, 350);
          return;
        }

        setTimeout(tick, 22);
      }
    }

    setTimeout(tick, 700);
  </script>
</body>
</html>
        """,
        height=360,
    )