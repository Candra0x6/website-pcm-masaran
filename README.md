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
| 1 | **Kurniawan Candra Mahardika** | **L200240210** | *Lead Fullstack, Core Backend & DevOps* | Inisialisasi arsitektur uv & Django 6.x, arsitektur database & core models (`ProfilOrganisasi`, `Pimpinan`, `Dokumen`, `TautanTerkait`), context processor navigasi global, singleton pattern organisasi, query optimizer (`select_related`/`prefetch_related`), WhiteNoise & security headers, Dockerfile & Compose, management command `seed_pcm`, orkestrasi motion design Waabi (Lenis + GSAP), deployment setup, dan GitHub Actions CI. |
| 2 | **afiiisky** | **L200240222** | *Frontend & UI Designer* | Desain sistem antarmuka responsif mengadopsi estetika Waabi, template inheritance `base.html`, dropdown hover flyout navigasi 4 menu, halaman beranda, profil, dan pimpinan. |
| 3 | **Latifah12-ui** | **L200240170** | *Feature Developer (Warta & Agenda)* | Model Berita & Agenda, custom queryset/manager `published()`, fitur slug otomatis unik, pagination (6 per halaman), pencarian berita, filter agenda mendatang/lampau. |
| 4 | **nazh21** | **L200240221** | *Backend Developer & QA* | Model Ranting & Amal Usaha, validasi ukuran berkas unduhan dokumen, custom actions & badge admin panel, opsi dry-run seeder, dan pengujian unit testing (`pcm/tests.py`). |

### 🔄 Alur Kerja & Workflow Kolaborasi Anggota

Untuk menjamin kualitas kode berskala enterprise dan distribusi kontribusi yang terukur, alur kerja dibagi ke dalam 5 fase kolaborasi:

#### 1. Workflow Anggota 1 (Lead Fullstack, Core Backend & DevOps):
- **Arsitektur & Core Backend:**
  - Inisialisasi stack modern dengan `uv` (Fast Python Package Manager) dan Django 6.x.
  - Perancangan arsitektur database relasional untuk 9 model, termasuk model singleton `ProfilOrganisasi` (pola single-row constraint).
  - Implementasi model inti backend: `ProfilOrganisasi`, `Pimpinan`, `Dokumen`, dan `TautanTerkait`.
  - Pembangunan Global Context Processor (`pcm.context_processors.pcm_globals`) agar data organisasi, nomor kontak, serta tautan eksternal terdistribusi ke seluruh template tanpa duplicate database queries.
  - Optimasi query backend (`select_related` & `prefetch_related`) untuk mencegah masalah N+1 queries pada view Beranda dan Amal Usaha.
- **Pipeline Data & Seeder:**
  - Pembuatan custom Django management command `seed_pcm` (`manage.py seed_pcm --download-images`).
  - Mekanisme pipeline unduh aset foto riil (Gedung Dakwah Masaran, struktur majelis, logo resmi) ke direktori `media/` dengan penanganan graceful fallback saat offline.
- **Motion & Visual Engineering:**
  - Orkestrasi sistem interaksi interaktif bergaya Waabi: Lenis Momentum Scroll, GSAP ScrollTrigger, Pinned Diorama Showcase 4 Pilar, serta dropdown navigasi 4 menu beranimasi smooth.
  - Integrasi Street View 360° & Google Maps Street interaktif dengan geolokasi presisi Gedung Dakwah PCM Masaran.
- **Containerization & CI/CD DevOps:**
  - Penyusunan `Dockerfile` multi-stage berbasis `python:3.12-slim` dengan keamanan user non-root.
  - Orkestrasi `compose.yaml` untuk pengujian kontainer lokal.
  - Setup konfigurasi WhiteNoise serving static files dan pipeline GitHub Actions CI otomatis.

#### 2. Workflow Anggota 2 — afiiisky (Frontend & UI Designer):
- Desain antarmuka publik berbasis Tailwind CSS mengadopsi estetika minimalis modern Waabi.
- Implementasi template inheritance `base.html` lengkap dengan header dinamis, footer resmi dengan lisensi CC BY-SA 4.0, dan mobile navigation drawer.
- Penyusunan halaman publik Beranda (`beranda.html`), Profil & Sejarah (`profil.html`), dan Pimpinan (`pimpinan.html`).

#### 3. Workflow Anggota 3 — Latifah12-ui (Feature Developer - Warta & Agenda):
- Pembangunan model data `Berita` (dengan auto-slug unik) dan `Agenda` (dengan tanggal mulai/selesai).
- Implementasi Custom Manager & QuerySet `BeritaManager.published()` dan `AgendaManager.mendatang()`.
- Pembuatan view warta (`berita_list_view`, `berita_detail_view`) dengan pagination 6 artikel per halaman dan pencarian keyword.
- Pembuatan view agenda (`agenda_list_view`) dengan segmentasi agenda mendatang vs riwayat agenda lampau.

#### 4. Workflow Anggota 4 — nazh21 (Backend Developer & QA):
- Pembangunan model data `Ranting` (13 PRM definitif) dan `AmalUsaha` (kategori pendidikan, kesehatan, sosial, ekonomi).
- Implementasi validasi ukuran berkas unduhan dokumen (`Dokumen.clean`) dengan pembatasan ukuran maksimal 25 MB.
- Kustomisasi panel Django Admin (`admin.py`): badge warna bidang amal usaha, paginasi & pencarian ranting, tampilan ukuran berkas dokumen, serta bulk actions status baca pesan masuk.
- Penambahan opsi `--dry-run` pada Django management command `seed_pcm` untuk simulasi seeding aman.
- Penyusunan rangkaian pengujian unit testing komprehensif (`pcm/tests.py`) mencakup representasi string, validasi form, pengurutan model, dan status dokumen.

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
| **Piagam Pendirian Resmi (1935)** | SK PWM Jawa Tengah No. `066/KEP/II.0/B/2026` | 15 November 2026 | Dokumen historis resmi pengesahan pendirian PCM Masaran pada 17 November 1935 M (20 Sya'ban 1354 H) |
| **Struktur Pimpinan Pleno Musycab 48** | SK PDM Sragen No. `032/KEP/III.0/D/2023` via Portal PDM Sragen | 15 November 2026 | Penetapan 13 Anggota Pleno / Formatur Musycab ke-48 periode 2022–2027 |
| **Struktur Paripurna (18 Majelis & Lembaga)** | Berkas Resmi Struktur Pengurus PCM Masaran 2022–2027 Paripurna | 15 November 2026 | Susunan 2 Penasehat, 13 Pimpinan Koordinator, serta 18 Majelis/Lembaga |
| **Daftar 13 Ranting Desa (PRM)** | Arsip Musyawarah Cabang ke-48 & Data Wilayah Kecamatan Masaran | 15 November 2026 | 13 desa definitif: Dawungan, Gebang, Jati, Jirapan, Karangmalang, Kliwonan, Krebet, Krikilan, Masaran, Pilang, Pringanom, Sepat, Sidodadi |
| **Data Amal Usaha (AUM Pendidikan, Kesehatan, Sosial, Ekonomi)** | Majelis Dikdasmen PCM Masaran & Direktori AUM Sragen | 15 November 2026 | SMK 10, SMA 3, SMP 2, MTs 3, SD Terpadu, 3 MIM, 11 TK ABA 'Aisyiyah, SPPGM Tangen, PKU, Lazismu, BMT |
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

## 🌐 Deployment Produksi & Tautan Live

- **🌐 Production Cloud Server (Vercel):** [https://website-pcm-masaran.vercel.app](https://website-pcm-masaran.vercel.app)
- **⚡ Backup Public Tunnel (Cloudflare):** [https://circus-wines-endorsed-kick.trycloudflare.com](https://circus-wines-endorsed-kick.trycloudflare.com)
- **📦 GitHub Repository:** [https://github.com/Candra0x6/website-pcm-masaran](https://github.com/Candra0x6/website-pcm-masaran)
- **Platform Web:** [Vercel](https://vercel.com) / [Render](https://render.com) / [Railway](https://railway.app) (Serverless & Docker Gunicorn + WhiteNoise)
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
