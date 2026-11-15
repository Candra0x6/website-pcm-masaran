# Website Resmi PCM Masaran (Sragen) dengan Django

> **Tugas 1 — Pemrograman Web Berbasis Framework (TIF1336)**  
> Program Studi Informatika, Fakultas Komunikasi dan Informatika  
> Universitas Muhammadiyah Surakarta (UMS) — 2026

---

## 👥 Identitas Kelompok & Kontribusi Anggota

**Nama Kelompok:** Tim Pengembang PCM Masaran  
**Pimpinan Cabang Muhammadiyah (PCM) Pilihan:** **PCM Masaran**, Kabupaten Sragen, Jawa Tengah  

### Tabel Kontribusi Anggota

| No | Nama Mahasiswa | NIM | Peran Utama | Rincian Pekerjaan & Fitur yang Dikerjakan |
|---|---|---|---|---|
| 1 | **Kurniawan Candra Mahardika** | **L200240210** | *Lead Fullstack & DevOps* | Inisialisasi arsitektur uv & Django 6.x, konfigurasi environment, WhiteNoise, Dockerfile & Compose, management command `seed_pcm`, deployment setup, dan GitHub Actions CI. |
| 2 | *(Nama Anggota 2)* | *(NIM Anggota 2)* | *Frontend & UI Designer* | Desain sistem antarmuka responsif mengadopsi estetika Waabi, template inheritance `base.html`, halaman beranda, profil, dan pimpinan. |
| 3 | *(Nama Anggota 3)* | *(NIM Anggota 3)* | *Feature Developer (Warta & Agenda)* | Model Berita & Agenda, custom queryset/manager `published()`, fitur slug otomatis unik, pagination (6 per halaman), pencarian berita, filter agenda mendatang/lampau. |
| 4 | *(Nama Anggota 4)* | *(NIM Anggota 4)* | *Backend Developer & QA* | Model Ranting & Amal Usaha, `ModelForm` formulir kontak publik & validasi, messages framework, panel admin custom, dan pengujian unit (`manage.py test`). |

---

## 🏛️ Profil PCM Masaran & Sumber Data Riil

Website ini dibangun menggunakan **100% data riil** dari Pimpinan Cabang Muhammadiyah (PCM) Masaran, Kabupaten Sragen, Jawa Tengah (SK PDM Sragen No. `032/KEP/III.0/D/2023`).

- **Sekretariat:** Gedung Dakwah Muhammadiyah Masaran, Jl. Raya Solo – Sragen KM 13, Masaran, Sragen 57282.
- **Ketua Cabang:** H. Siyamto Umardani, S.Ag.
- **Sekretaris Cabang:** Muhammad Effendi, S.Psi.
- **Email:** `pcm.masaran@gmail.com` | **Telepon:** (0271) 8821032
- **Kanal Resmi:**
  - YouTube: [Muhammadiyah Masaran](https://youtube.com/@muhammadiyahmasaran)
  - Facebook: [PCM Masaran](https://www.facebook.com/profile.php?id=61553634994772)
  - Instagram: [@pcm.masaran](https://www.instagram.com/pcm.masaran)
  - TikTok: [@muhammadiyahmasar](https://tiktok.com/@muhammadiyahmasar)
  - Threads: [@pcm.masaran](https://www.threads.com/@pcm.masaran)
  - X (Twitter): [@PcmMasaran](https://x.com/PcmMasaran)

### Tabel Verifikasi Sumber Data

| Data | Sumber Pengambilan | Tanggal Diambil | Keterangan / Izin |
|---|---|---|---|
| **Struktur Pimpinan (Ketua, Sekretaris, Majelis)** | SK PDM Sragen No. 032/KEP/III.0/D/2023 via Portal PDM Sragen & PWM Jateng | 15 November 2026 | Data publik resmi kepengurusan periode 2022–2027 |
| **Daftar 13 Ranting Desa (PRM)** | Arsip Musyawarah Cabang ke-48 & Data Wilayah Kecamatan Masaran | 15 November 2026 | Sesuai 13 desa definitif di Kec. Masaran |
| **Data Amal Usaha (AUM Pendidikan, Kesehatan, Sosial, Ekonomi)** | Majelis Dikdasmen PCM Masaran & Direktori Sekolah Muhammadiyah Sragen | 15 November 2026 | SMK Muh 10, SMA Muh 3, SMP Muh 2, MTs Muh 3, PKU, Lazismu, BMT |
| **Warta Berita & Agenda Kajian** | Kanal YouTube resmi `@muhammadiyahmasaran` & Liputan PDM Sragen | 15 November 2026 | Rekaman video kajian Ahad pagi, Rakercab, dan Milad ke-113 |
| **Dokumen SK & Pedoman Ranting** | Arsip publik Lembaga Pengembangan Cabang dan Ranting (LPCR) | 15 November 2026 | Berkas PDF resmi persyarikatan |
| **Logo Resmi Muhammadiyah** | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Muhammadiyah.svg) | 15 November 2026 | Karya K. H. Siradj Dahlan, vektor oleh Hibensis, lisensi CC BY-SA 4.0 |

---

## 🚀 Fitur Unggulan & Konsep Django

1. **Desain Terinspirasi Waabi:** Tampilan minimalis editorial modern dengan palet *warm cream* (`#FAF9F5`), aksen hijau persyarikatan tajam (`#006633`), floating blur navigation bar, kartu berkontur halus, dan tipografi bold terstruktur.
2. **Context Processor Terpusat:** Profil organisasi (singleton) dan tautan persyarikatan (PDM Sragen, PWM Jateng, PP Muhammadiyah) otomatis tersedia di semua template.
3. **Custom QuerySet & Manager:** `Berita.objects.published()` memastikan hanya artikel bertatus 'terbit' dengan tanggal rilis valid yang tampil ke publik (artikel draf atau tanggal masa depan menghasilkan **HTTP 404**).
4. **Paginator & Fitur Pencarian:** Halaman berita membatasi 6 berita per halaman dan dilengkapi form pencarian kata kunci (`?q=...`).
5. **ModelForm & Messages Framework:** Formulir kontak publik tervalidasi dengan notifikasi flash pesan sukses.
6. **Auto Unique Slug:** Slug artikel dibuat otomatis dari judul dan tetap unik jika terjadi kesamaan judul artikel.
7. **WhiteNoise & Multi-Database Ready:** Mendukung SQLite untuk pengembangan lokal serta PostgreSQL (Supabase / Neon) untuk produksi via `DATABASE_URL`.
8. **Management Command `seed_pcm`:** Satu perintah untuk mengisi seluruh data profil, pimpinan, ranting, amal usaha, berita, agenda, dokumen unduhan, dan menyalin aset gambar asli ke direktori `media/`.
9. **Unit Testing Otomatis:** Minimal 6 test case lulus 100% dan terintegrasi dengan GitHub Actions CI.

---

## 💻 Cara Menjalankan di Laptop (Lokal dengan `uv`)

### 1. Prasyarat
- Python 3.12+ (disarankan Python 3.13 / 3.14)
- [`uv`](https://docs.astral.sh/uv/) terpasang di sistem (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### 2. Langkah Instalasi & Menjalankan

```bash
# 1. Clone repository
git clone <url-repo-anda>
cd website-pcm-masaran

# 2. Siapkan environment file
cp .env.example .env

# 3. Install seluruh dependensi menggunakan uv
uv sync

# 4. Jalankan migrasi database SQLite
uv run python manage.py migrate

# 5. Isi database dengan data riil PCM Masaran & gambar otomatis
uv run python manage.py seed_pcm --clear

# 6. Jalankan automated test
uv run python manage.py test

# 7. Jalankan development server
uv run python manage.py runserver
```

Buka browser di `http://localhost:8000`.  
Untuk mengakses admin panel: `http://localhost:8000/admin/` (Akun demo: username `admin` / password `adminpcm2026`).

---

## 🐳 Menjalankan dengan Docker

Siapa pun yang meng-clone repo ini cukup menjalankan **satu perintah** untuk mendapatkan website lengkap beserta database PostgreSQL 17:

```bash
docker compose up --build
```

Setelah container berjalan:
- Buka website: `http://localhost:8000`
- Mengisi data riil di container (jika database baru):
  ```bash
  docker compose exec web uv run python manage.py seed_pcm --clear
  ```
- Membuat superuser baru di container:
  ```bash
  docker compose exec web uv run python manage.py createsuperuser
  ```
- Menghentikan container (data database & media tetap aman tersimpan di volume):
  ```bash
  docker compose down
  ```
- **Mengapa `docker compose down -v` menghapus semua data?**  
  Flag `-v` (`--volumes`) menginstruksikan Docker untuk menghapus seluruh *named volumes* yang terpasang pada service, yaitu `pcm_masaran_postgres_data` (tempat tabel PostgreSQL disimpan) dan `pcm_masaran_media_data` (tempat berkas unggahan gambar & dokumen disimpan). Jika dijalankan dengan `-v`, kedua volume tersebut akan dimusnahkan secara permanen sehingga database kembali kosong bersih pada startup berikutnya.

---

## 🌐 Deployment Produksi

- **Platform Web:** [Render](https://render.com) / [Railway](https://railway.app) / [Vercel](https://vercel.com)
- **Database Produksi:** PostgreSQL di [Supabase](https://supabase.com) / [Neon](https://neon.tech)
- **Alasan Pemilihan Platform & Database:**
  - **Railway / Render:** Mendukung deployment langsung dari `Dockerfile` berbasis `uv` dengan Gunicorn dan WhiteNoise tanpa kompromi serverless timeout.
  - **Neon / Supabase PostgreSQL:** Menyediakan basis data PostgreSQL 17 berkinerja tinggi, kompatibel penuh dengan `psycopg` dan `dj-database-url`, serta memiliki dashboard visual table editor.
- **Strategi File Media Permanen:** Pada platform cloud yang bersifat ephemeral (stateless filesystem), berkas media disimpan secara persisten menggunakan S3-compatible Object Storage (Supabase Storage / Cloudflare R2 / Cloudinary) melalui `django-storages`.

---

## 🔑 Konfigurasi Environment Variable

Berikut adalah daftar variabel lingkungan yang dibutuhkan sistem (tersedia di `.env.example` tanpa nilai rahasia):

| Variabel | Deskripsi | Nilai Contoh (Lokal) | Nilai di Produksi |
|---|---|---|---|
| `SECRET_KEY` | Kunci enkripsi sesi & CSRF Django | `django-insecure-dev-key...` | String acak panjang 50+ karakter unik |
| `DEBUG` | Mode debug Django | `True` | **`False`** (Wajib False) |
| `ALLOWED_HOSTS` | Daftar host/domain yang diizinkan | `localhost,127.0.0.1` | `pcm-masaran.onrender.com,yourdomain.com` |
| `CSRF_TRUSTED_ORIGINS` | Domain aman untuk formulir CSRF | `http://localhost:8000` | `https://pcm-masaran.onrender.com` |
| `DATABASE_URL` | Connection string PostgreSQL | *(Kosong = otomatis SQLite)* | `postgres://user:pass@ep-xyz.neon.tech/neondb?sslmode=require` |
| `PORT` | Port server Gunicorn | `8000` | `8000` (atau disediakan otomatis oleh platform) |

---

## 📜 Keterangan Hak Cipta & Lisensi Akademis

1. **Keterangan Tugas Kuliah:**  
   *Website ini dibuat untuk tugas kuliah Pemrograman Web berbasis Framework (TIF1336), bukan website resmi PCM Masaran.*
2. **Atribusi Logo:**  
   *Logo Muhammadiyah: K. H. Siradj Dahlan, vektor oleh Hibensis, via Wikimedia Commons, lisensi CC BY-SA 4.0.*
3. **Atribusi Konten:**  
   Seluruh data kegiatan, foto, dan informasi profil bersumber dari publikasi resmi Pimpinan Cabang Muhammadiyah Masaran dan PDM Kabupaten Sragen.
