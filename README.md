# KosEats AI

Aplikasi Streamlit untuk rekomendasi paket makan harian berbasis Content-Based Filtering.

## Cara menjalankan

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Struktur folder

```text
meal_planner_modular/
├── app.py
├── config.py
├── dataset_menu_makanan.csv
├── requirements.txt
├── services/
│   ├── data_service.py
│   ├── finance.py
│   └── recommender.py
└── ui/
    ├── home.py
    ├── results.py
    ├── sidebar.py
    └── styles.py
```

## Pembagian tanggung jawab file

- `app.py`: alur utama aplikasi.
- `config.py`: konfigurasi, path, slot makan, dan bobot scoring.
- `services/data_service.py`: load dataset, cleaning, TF-IDF index, dan filter preferensi.
- `services/recommender.py`: algoritma rekomendasi dan scoring.
- `services/finance.py`: tips finansial.
- `ui/styles.py`: CSS global.
- `ui/sidebar.py`: input preferensi user.
- `ui/home.py`: tampilan awal dan typing animation.
- `ui/results.py`: tampilan hasil rekomendasi, tabel detail, dan footer.
