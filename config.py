"""Konfigurasi utama aplikasi KosEats AI."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset_menu_makanan.csv"

PAGE_TITLE = "KosEats AI - Smart Budget Meal Planner"
PAGE_ICON = "🍱"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

SLOTS = ["Sarapan", "Makan Siang", "Makan Malam"]
SLOT_ICONS = {"Sarapan": "🌅", "Makan Siang": "☀️", "Makan Malam": "🌙"}

# Bobot skor gabungan: 70% kemiripan konten, 30% efisiensi harga
WEIGHT_TEXT = 0.70
WEIGHT_PRICE = 0.30
BUDGET_THRESHOLD = 50_000

WAKTU_OPTIONS = {
    "🌅 Sarapan": ["Sarapan"],
    "☀️ Makan Siang": ["Makan Siang"],
    "🌙 Makan Malam": ["Makan Malam"],
    "🌅☀️ Sarapan + Makan Siang": ["Sarapan", "Makan Siang"],
    "🌅🌙 Sarapan + Makan Malam": ["Sarapan", "Makan Malam"],
    "☀️🌙 Makan Siang + Makan Malam": ["Makan Siang", "Makan Malam"],
    "🌅☀️🌙 Sarapan + Siang + Malam": ["Sarapan", "Makan Siang", "Makan Malam"],
}
