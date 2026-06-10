"""Helper untuk tips finansial harian."""


def get_financial_tip(sisa: int, budget: int) -> tuple[str, str]:
    """Kembalikan ikon dan pesan tips finansial sesuai sisa budget."""
    persen = (sisa / budget * 100) if budget > 0 else 0

    if persen >= 40:
        return "🏆", (
            f"Luar biasa! Kamu menghemat <strong>Rp {sisa:,}</strong> hari ini ({persen:.0f}% dari budget). "
            "Sisihkan ke tabungan darurat. Konsisten 30 hari = uang jajan bonus hampir seminggu!"
        )

    if persen >= 20:
        return "💪", (
            f"Bagus! Hemat <strong>Rp {sisa:,}</strong> hari ini. "
            "Transfer sisa ini ke e-wallet terkunci sekarang sebelum tergoda beli kopi kekinian."
        )

    if persen >= 5:
        return "🌱", (
            f"Kamu berhasil menyisakan <strong>Rp {sisa:,}</strong>. "
            "Tips: kurangi 1 pesanan online per minggu. Efeknya terasa di akhir bulan."
        )

    if sisa == 0:
        return "⚖️", (
            "Pas! Budget terpakai semua tanpa boncos. "
            "Idealnya sisakan 5-10% sebagai buffer. Coba set budget 5% lebih rendah besok."
        )

    return "⚠️", (
        f"Budget hampir habis, sisa <strong>Rp {sisa:,}</strong>. "
        "Catat semua pengeluaran di Notes HP. Kesadaran finansial dimulai dari sini."
    )
