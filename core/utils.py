import re

HALAMAN = [
    "Dashboard",
    "Penyewaan Baru",
    "Pengembalian",
    "Riwayat Penyewaan",
    "Laporan",
    "Inventaris",
    "Data Penyewa",
    "Tentang",
]

DENDA_PER_HARI = 1500

PROGRAM_STUDI_PER_JURUSAN = {
    "Administrasi Bisnis": [
        "D3-Administrasi Bisnis",
        "D3-Manajemen Pemasaran",
        "D4-Manajemen Bisnis Internasional",
        "D4-Administrasi Bisnis Terapan",
    ],
    "Akuntansi": [
        "D3-Akuntansi",
        "D3-Keuangan dan Perbankan",
        "D4-Komputerisasi Akuntansi",
        "D4-Perbankan Syariah",
        "D4-Analis Keuangan",
        "D4-Akuntansi Manajerial",
    ],
    "Teknik Elektro": [
        "D3-Teknik Listrik",
        "D3-Teknik Elektronika",
        "D3-Teknik Telekomunikasi",
        "D3-Teknik Informatika",
        "D4-Teknik Telekomunikasi",
        "D4-Teknologi Rekayasa Instalasi Listrik",
        "D4-Teknologi Rekayasa Komputer",
        "D4-Teknologi Rekayasa Elektronika",
        "S2-Teknik Telekomunikasi",
    ],
    "Teknik Mesin": [
        "D3-Teknik Mesin",
        "D3-Teknik Konversi Energi",
        "D4-Teknik Mesin Produksi dan Perawatan",
        "D4-Teknologi Rekayasa Pembangkit Energi",
    ],
    "Teknik Sipil": [
        "D3-Konstruksi Gedung",
        "D3-Konstruksi Sipil",
        "D4-Teknik Perawatan dan Perbaikan Gedung",
        "D4-Perancangan Jalan dan Jembatan",
    ],
}


def validasi_penyewa(nim, nama, no_hp, email, jurusan, prodi):
    errors = []
    nim_value = str(nim or "").strip()
    nama_value = str(nama or "").strip()
    hp_value = str(no_hp or "").strip()
    email_value = str(email or "").strip()
    jurusan_value = str(jurusan or "").strip()
    prodi_value = str(prodi or "").strip()

    if not nama_value:
        errors.append("Nama penyewa wajib diisi.")
    if not nim_value:
        errors.append("NIM wajib diisi.")
    if not hp_value:
        errors.append("Nomor telepon wajib diisi.")
    if not email_value:
        errors.append("Email wajib diisi.")
    if not jurusan_value:
        errors.append("Jurusan wajib diisi.")
    if not prodi_value:
        errors.append("Program studi wajib diisi.")

    if nim_value and not nim_value.isdigit():
        errors.append("NIM hanya boleh berisi angka tanpa titik, spasi, atau huruf.")
    if hp_value and not hp_value.isdigit():
        errors.append("Nomor telepon hanya boleh berisi angka.")
    if email_value and not re.fullmatch(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email_value):
        errors.append("Format email tidak valid.")
    if jurusan_value and prodi_value and prodi_value not in PROGRAM_STUDI_PER_JURUSAN.get(jurusan_value, []):
        errors.append("Program studi harus sesuai dengan jurusan yang dipilih.")

    return errors
