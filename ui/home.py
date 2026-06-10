"""Hero page sebelum user menekan tombol cari."""

import streamlit.components.v1 as components


def render_home() -> None:
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
    padding: 40px 16px 32px;
    min-height: 380px;
  }
  .tagline {
    font-size: 0.8rem;
    color: #888;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 36px;
    font-weight: 500;
  }
  .typing-wrapper {
    min-height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 100%;
    max-width: 700px;
    margin-bottom: 48px;
  }
  #typing-output {
    font-size: 1.3rem;
    line-height: 1.75;
    color: #f5a623;
    font-weight: 500;
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
    margin-bottom: 36px;
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
    ← Atur preferensi di sidebar, lalu tekan <strong>Cari Paket Makan</strong>
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
        return;
      }

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

    setTimeout(tick, 700);
  </script>
</body>
</html>
        """,
        height=420,
    )
