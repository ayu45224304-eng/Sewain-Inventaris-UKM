# AGENT INSTRUCTIONS — SEWAIN SYSTEM

Dokumen ini adalah aturan dasar buat AI Agent dalam mengembangkan dan merawat aplikasi Sewain.
la
## 1. Identitas Sistem
- Nama Aplikasi: Sewain (Sistem Penyewaan Inventaris UKM).
- Bahasa Tampilan: Bahasa Indonesia baku (Penyewaan, Pengembalian, Inventaris, Riwayat, Laporan).

## 2. Tech Stack & Environment
- Framework: Python & Streamlit.
- Virtual Environment: Wajib pakai `.venv`.
- UI Styling: Pakai custom CSS (header tabel rata tengah, tanpa background gelap di header).

## 3. Database
- Database Engine: SQLite (`sewain.db`) di dalam folder `core/`.
- Menggunakan modul `sqlite3` bawaan Python untuk menyimpan data barang, peminjam, transaksi penyewaan, dan pengembalian.

## 4. Akses Pengguna
- Wajib menggunakan halaman autentikasi dengan pilihan **Masuk** dan **Daftar**.
- Aplikasi mendukung multi-user dengan username dan password; username harus unik.
- Password disimpan sebagai hash PBKDF2-HMAC-SHA256 dengan salt acak dan 600.000 iterasi; password asli tidak boleh disimpan.
- Akun admin awal dibuat dari `SEWAIN_ADMIN_USERNAME` dan `SEWAIN_ADMIN_PASSWORD`; kredensial default sementara adalah `admin` / `sewain123` dan wajib diganti setelah login.
- Sesi login memakai `st.session_state`; tersedia menu Ubah Password dan Logout di sidebar.

## 5. Acuan Perancangan
- Seluruh alur dan fitur merujuk pada dokumen PDF perancangan di folder project.

## 6. Aturan Tampilan Tabel (UI Rules)
- Judul kolom wajib KAPITAL (UPPERCASE).
- Posisi Tengah (Center): Kode barang/transaksi, tanggal sewa/kembali, dan status.
- Posisi Kiri (Left): Nama barang, nama peminjam, kategori, dan catatan.

## 7. Aturan Pengembalian & Denda
- Denda keterlambatan: Rp1.500 per hari (konstanta `DENDA_PER_HARI` di `core/utils.py`).
- Terlambat = status Disewa dan tanggal kembali aktual melebihi tanggal rencana kembali; tepat di tanggal rencana belum dikenai denda.
- Pengembalian dicatat pada tabel `pengembalian` (1 transaksi maksimal 1 catatan), lengkap dengan tanggal kembali aktual, lama terlambat, dan total denda yang disalin saat diproses.
- Kondisi barang dicatat per barang pada `detail_peminjaman.kondisi_barang`.
- Pengembalian sebagian dan riwayat mutasi stok belum didukung.

## 8. Data Master Penyewa
- Data master penyewa berfungsi sebagai sumber utama informasi penyewa, khususnya nomor telepon dan email.
- Menu baru `Data Penyewa` wajib menampilkan data penyewa, mengelola data master, dan menjadi satu-satunya titik perubahan nomor telepon atau email.
- Form `Penyewaan Baru` hanya menerima NIM dan membaca data penyewa dari master; data master tidak boleh diubah dari transaksi.
- Jurusan dan Program studi wajib diisi pada data penyewa.
- Data penyewa diubah lewat ikon edit pada kolom EDIT di tabel Data Penyewa.

## 9. Halaman Tentang
- Menu "Tentang" berisi deskripsi aplikasi, nama penyusun (Kelompok 5), dan kontak (sewain.inventaris.ukm@gmail.com).
- Halaman ini statis dan tidak memakai database.
