import os
import shutil
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from pcm.models import (
    ProfilOrganisasi,
    Pimpinan,
    Ranting,
    AmalUsaha,
    Berita,
    Agenda,
    Dokumen,
    TautanTerkait
)


class Command(BaseCommand):
    help = "Mengisi database dengan data riil PCM Masaran beserta aset gambarnya"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Hapus data lama sebelum melakukan seeding'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Memulai proses seeding data riil PCM Masaran..."))

        if options['clear']:
            self.stdout.write("Menghapus data lama...")
            ProfilOrganisasi.objects.all().delete()
            Pimpinan.objects.all().delete()
            Ranting.objects.all().delete()
            AmalUsaha.objects.all().delete()
            Berita.objects.all().delete()
            Agenda.objects.all().delete()
            Dokumen.objects.all().delete()
            TautanTerkait.objects.all().delete()

        media_root = settings.MEDIA_ROOT
        os.makedirs(os.path.join(media_root, 'profil'), exist_ok=True)
        os.makedirs(os.path.join(media_root, 'pimpinan'), exist_ok=True)
        os.makedirs(os.path.join(media_root, 'amal_usaha'), exist_ok=True)
        os.makedirs(os.path.join(media_root, 'berita'), exist_ok=True)
        os.makedirs(os.path.join(media_root, 'dokumen'), exist_ok=True)

        seed_assets = settings.BASE_DIR / 'seed_assets'

        def copy_asset(source_rel, target_rel):
            src = seed_assets / source_rel
            dst = os.path.join(media_root, target_rel)
            if src.exists():
                shutil.copy(src, dst)
                return target_rel
            return ""

        if not ProfilOrganisasi.objects.exists():
            hero_rel = copy_asset('hero/hero_masaran.jpg', 'profil/hero_masaran.jpg')
            misi_text = (
                "Menegakkan Tauhid yang murni berdasarkan Al-Quran dan As-Sunnah.\n"
                "Menyebarluaskan dan memajukan Ajaran Islam yang bersumber pada Al-Quran dan As-Sunnah yang shahihah/maqbulah.\n"
                "Mewujudkan Islam dalam kehidupan pribadi, keluarga, dan masyarakat."
            )
            sejarah_text = (
                "Pimpinan Cabang Muhammadiyah (PCM) Masaran secara resmi berdiri pada tanggal 20 Sya'ban 1354 Hijriyah yang bertepatan dengan 17 November 1935 Masehi, sebagaimana disahkan melalui Surat Keputusan Pimpinan Wilayah Muhammadiyah Jawa Tengah Nomor 066/KEP/II.0/B/2026 tentang Pengesahan Pendirian Cabang Muhammadiyah Masaran Kabupaten Sragen.\n\n"
                "Bermula dari pergerakan dakwah Islam berkemajuan di wilayah Masaran masa pra-kemerdekaan, para perintis persyarikatan mendirikan pusat kajian dan pengajian di desa-desa sekitar Masaran. Selama lebih dari sembilan dekade perjalanan khidmah, PCM Masaran terus bertransformasi menjadi kekuatan pencerah peradaban umat melalui penguatan 13 Pimpinan Ranting Muhammadiyah (PRM) definitif, belasan Amal Usaha Muhammadiyah (AUM) di bidang pendidikan dasar hingga menengah kejuruan, pelayanan kesehatan, gerakan filantropi Lazismu, serta sentra ekonomi produktif.\n\n"
                "Kini dengan berpusat di Gedung Dakwah Muhammadiyah Masaran di jalur strategis Solo–Sragen KM 13, persyarikatan menggerakkan dakwah amar ma'ruf nahi munkar berlandaskan Al-Qur'an dan As-Sunnah ash-Shahihah."
            )
            tentang_text = (
                "Pimpinan Cabang Muhammadiyah (PCM) Masaran adalah organisasi kemasyarakatan Islam berkemajuan yang membina wilayah Kecamatan Masaran, Kabupaten Sragen, Jawa Tengah. Berdiri sejak 17 November 1935 (20 Sya'ban 1354 H), PCM Masaran mengoordinasikan 13 Pimpinan Ranting Muhammadiyah (PRM) desa, puluhan lembaga pendidikan mulai dari TK 'Aisyiyah, MIM, MTs, SMP, SMA, hingga SMK, serta unit kesehatan dan sentra ekonomi keumatan."
            )
            ProfilOrganisasi.objects.create(
                nama="Pimpinan Cabang Muhammadiyah Masaran",
                nama_singkat="PCM Masaran",
                tagline="Mencerahkan Semesta, Memajukan Masaran Berkemajuan",
                tentang=tentang_text,
                sejarah=sejarah_text,
                visi="Terwujudnya masyarakat Islam yang sebenar-benarnya.",
                misi=misi_text,
                alamat_sekretariat="Gedung Dakwah Muhammadiyah Masaran, Jl. Raya Solo - Sragen KM 13, Masaran, Sragen, Jawa Tengah 57282",
                telepon="(0271) 8821032",
                email="pcm.masaran@gmail.com",
                jumlah_anggota_ktam=1250,
                gambar_utama=hero_rel
            )
            self.stdout.write(self.style.SUCCESS("✓ Profil Organisasi berhasil dibuat"))

        if not Pimpinan.objects.exists():
            pimpinan_data = [
                ("H. Siyamto Umardani, S.Ag.", "Ketua Cabang", "2022–2027", 1, "pimpinan/ketua_siyamto.jpg", "pimpinan/ketua_siyamto.jpg"),
                ("Giyamto, S.Pd.", "Wakil Ketua I (MPM & Lazismu)", "2022–2027", 2, "pimpinan/wakil_sucipto.jpg", "pimpinan/wakil_giyamto.jpg"),
                ("H. Sumarno, S.Th.I.", "Wakil Ketua II (LPHU & LPPK)", "2022–2027", 3, "pimpinan/tabligh_sukadi.jpg", "pimpinan/wakil_sumarno.jpg"),
                ("Parlan Sinung Darsono", "Wakil Ketua III (MPK-SDI & LSBO)", "2022–2027", 4, "pimpinan/wakil_sucipto.jpg", "pimpinan/wakil_parlan.jpg"),
                ("H. Suyatno, S.Sos, M.Si.", "Wakil Ketua IV (Wakaf & MLH)", "2022–2027", 5, "pimpinan/bendahara_riris.jpg", "pimpinan/wakil_suyatno.jpg"),
                ("Muhammad Marjuki, S.Pd.", "Wakil Ketua V (Tarjih, Tabligh & LPCR)", "2022–2027", 6, "pimpinan/tabligh_sukadi.jpg", "pimpinan/wakil_marjuki.jpg"),
                ("Dr. H. Basuki Agus Suparno, M.Si.", "Wakil Ketua VI (MPI & Hukum-HAM)", "2022–2027", 7, "pimpinan/dikdasmen_muslih.jpg", "pimpinan/wakil_basuki.jpg"),
                ("Dr. Purwadi, M.Pd.", "Wakil Ketua VII (Dikdasmen & Pesantren)", "2022–2027", 8, "pimpinan/dikdasmen_muslih.jpg", "pimpinan/wakil_purwadi.jpg"),
                ("Dr. H. Suharno, ST. MT.", "Wakil Ketua VIII (Ekonomi & LHKP)", "2022–2027", 9, "pimpinan/bendahara_riris.jpg", "pimpinan/wakil_suharno.jpg"),
                ("Muhammad Effendi, S.Psi.", "Sekretaris Cabang", "2022–2027", 10, "pimpinan/sekretaris_efendi.jpg", "pimpinan/sekretaris_efendi.jpg"),
                ("Drs. H. Taslim Daryanto, M.Pd.", "Wakil Sekretaris (MPKU & Sosial)", "2022–2027", 11, "pimpinan/sekretaris_efendi.jpg", "pimpinan/wsek_taslim.jpg"),
                ("Dwi Daryanto, S.Pd.I.", "Bendahara Cabang", "2022–2027", 12, "pimpinan/bendahara_riris.jpg", "pimpinan/bendahara_dwi.jpg"),
                ("Muslih, S.Pd.", "Wakil Bendahara (Resiliensi Bencana)", "2022–2027", 13, "pimpinan/dikdasmen_muslih.jpg", "pimpinan/wbend_muslih.jpg"),
                ("Drs. H. Sutarno, MM", "Penasehat PCM Masaran", "2022–2027", 14, "pimpinan/ketua_siyamto.jpg", "pimpinan/penasehat_sutarno.jpg"),
                ("Ir. H. Suroto", "Penasehat PCM Masaran", "2022–2027", 15, "pimpinan/ketua_siyamto.jpg", "pimpinan/penasehat_suroto.jpg"),
            ]
            for nama, jabatan, periode, urutan, src_rel, dst_rel in pimpinan_data:
                foto_rel = copy_asset(src_rel, dst_rel)
                Pimpinan.objects.create(
                    nama=nama,
                    jabatan=jabatan,
                    periode=periode,
                    urutan=urutan,
                    foto=foto_rel
                )
            self.stdout.write(self.style.SUCCESS(f"✓ {len(pimpinan_data)} Pimpinan berhasil dibuat"))

        if not Ranting.objects.exists():
            ranting_data = [
                ("Dawungan", "Sunardi, S.Pd.I", "Dukuh Dawungan RT 02, Desa Dawungan, Masaran", ""),
                ("Gebang", "H. Sukamto", "Dukuh Gebang RT 05, Desa Gebang, Masaran", ""),
                ("Jati", "Supriyanto, S.Pd.", "Dukuh Jati RT 01, Desa Jati, Masaran", ""),
                ("Jirapan", "Drs. H. Wardoyo", "Kompleks Ponpes/Masjid Al-Manar, Desa Jirapan, Masaran", ""),
                ("Karangmalang", "H. Mulyono", "Dukuh Karangmalang RT 03, Desa Karangmalang, Masaran", ""),
                ("Kliwonan", "H. Budi Santoso", "Jl. Batik Kliwonan RT 08, Desa Kliwonan, Masaran", "(0271) 8821102"),
                ("Krebet", "Agus Widodo", "Kompleks Masjid Mujahidin, Desa Krebet, Masaran", ""),
                ("Krikilan", "Drs. H. Bambang", "Dukuh Krikilan RT 06, Desa Krikilan, Masaran", ""),
                ("Masaran", "H. Suratno, S.Pd.", "Kompleks Masjid Baiturrahman, Desa Masaran", "(0271) 8821035"),
                ("Pilang", "Drs. Joko Purnomo", "Dukuh Pilang RT 04, Desa Pilang, Masaran", ""),
                ("Pringanom", "Ustadz Rohmadi", "Dukuh Pringanom RT 02, Desa Pringanom, Masaran", ""),
                ("Sepat", "H. Ahmad Fauzi", "Kompleks Mushola Al-Huda, Desa Sepat, Masaran", ""),
                ("Sidodadi", "Ustadz Suparman", "Kompleks MIM Sidodadi, Desa Sidodadi, Masaran", ""),
            ]
            for nama, ketua, alamat, telp in ranting_data:
                Ranting.objects.create(
                    nama_ranting=nama,
                    ketua=ketua,
                    alamat=alamat,
                    telepon=telp
                )
            self.stdout.write(self.style.SUCCESS(f"✓ {len(ranting_data)} Pimpinan Ranting berhasil dibuat"))

        if not AmalUsaha.objects.exists():
            aum_data = [
                ("SMK Muhammadiyah 10 Masaran", "pendidikan", "Sekolah Menengah Kejuruan Pusat Keunggulan dengan program keahlian Teknik Kendaraan Ringan dan Teknik Komputer Jaringan.", "Jl. Raya Masaran - Pungkruk KM 2, Masaran, Sragen", "amal_usaha/aum_pendidikan_smk.jpg", "amal_usaha/aum_pendidikan_smk.jpg"),
                ("SMA Muhammadiyah 3 Masaran", "pendidikan", "Sekolah Menengah Atas berbasis nilai Islam holistik, riset sains, dan pembinaan kader bangsa.", "Kompleks Pendidikan Muhammadiyah, Masaran, Sragen", "amal_usaha/aum_pendidikan_smk.jpg", "amal_usaha/aum_pendidikan_sma.jpg"),
                ("SMP Muhammadiyah 2 Masaran", "pendidikan", "Sekolah Menengah Pertama unggulan berprestasi akademik dan kepesantrenan (lokasi Musycab ke-48).", "Jl. Raya Solo - Sragen KM 12, Masaran, Sragen", "amal_usaha/aum_pendidikan_smk.jpg", "amal_usaha/aum_pendidikan_smp.jpg"),
                ("MTs Muhammadiyah 3 Masaran", "pendidikan", "Madrasah Tsanawiyah terpadu berwawasan global dengan kurikulum Kemenag dan tahfidz Al-Qur'an.", "Dukuh Kliwonan RT 08, Desa Kliwonan, Masaran", "amal_usaha/aum_pendidikan_smk.jpg", "amal_usaha/aum_pendidikan_mts.jpg"),
                ("SD Muhammadiyah Terpadu Masaran", "pendidikan", "Sekolah Dasar Islam terpadu dengan pembelajaran aktif, tahfidz juz amma, dan pembiasaan adab Islami.", "Kompleks Gedung Dakwah PCM Masaran, Sragen", "amal_usaha/aum_pendidikan_smk.jpg", "amal_usaha/aum_pendidikan_sd.jpg"),
                ("MIM Sidodadi Masaran", "pendidikan", "Madrasah Ibtidaiyah Muhammadiyah Sidodadi membina generasi Qur'ani di wilayah ranting Sidodadi.", "Kompleks Perguruan Muhammadiyah Sidodadi, Masaran, Sragen", "amal_usaha/aum_pendidikan_smk.jpg", "amal_usaha/aum_pendidikan_mim_sidodadi.jpg"),
                ("MIM Kliwonan Masaran", "pendidikan", "Madrasah Ibtidaiyah Muhammadiyah Kliwonan dengan program keagamaan, sains madrasah, dan bahasa Arab.", "Jl. Batik Kliwonan RT 08, Desa Kliwonan, Masaran, Sragen", "amal_usaha/aum_pendidikan_smk.jpg", "amal_usaha/aum_pendidikan_mim_kliwonan.jpg"),
                ("MIM Pilang Masaran", "pendidikan", "Madrasah Ibtidaiyah Muhammadiyah Pilang berfokus pada pendidikan akhlakul karimah dan literasi dasar.", "Dukuh Pilang RT 04, Desa Pilang, Masaran, Sragen", "amal_usaha/aum_pendidikan_smk.jpg", "amal_usaha/aum_pendidikan_mim_pilang.jpg"),
                ("Jaringan 11 TK 'Aisyiyah Bustanul Athfal Masaran", "pendidikan", "Jaringan 11 unit PAUD dan TK 'Aisyiyah Bustanul Athfal (TK ABA) binaan PCA Masaran tersebar di 11 ranting desa se-Kecamatan Masaran.", "Tersebar di 11 Ranting Desa se-Kecamatan Masaran", "amal_usaha/aum_pendidikan_smk.jpg", "amal_usaha/aum_tk_aba.jpg"),
                ("Sentra Pengolahan Pertanian Gabah Muhammadiyah (SPPGM) Tangen", "ekonomi", "Unit usaha produktif agrobisnis persyarikatan pengolahan gabah dan ketahanan pangan mandiri PCM Masaran di Tangen.", "Kawasan Sentra Pangan PCM Masaran, Tangen, Sragen", "amal_usaha/aum_ekonomi.jpg", "amal_usaha/aum_sppgm.jpg"),
                ("Klinik Pratama PKU Muhammadiyah Masaran", "kesehatan", "Pusat pelayanan kesehatan rawat jalan 24 jam, persalinan, khitanan, dan poliklinik umum masyarakat.", "Jl. Raya Solo - Sragen KM 13.5, Masaran, Sragen", "amal_usaha/aum_pku_kesehatan.jpg", "amal_usaha/aum_pku_kesehatan.jpg"),
                ("Kantor Layanan Lazismu Masaran", "sosial", "Lembaga amil zakat, infak, dan sedekah terpercaya untuk program pemberdayaan mustahiq dan beasiswa sang surya.", "Gedung Dakwah PCM Masaran Lt. 1, Jl. Raya Solo - Sragen KM 13", "amal_usaha/aum_lazismu.jpg", "amal_usaha/aum_lazismu.jpg"),
                ("Toko Surya & BMT Muhammadiyah Masaran", "ekonomi", "Unit usaha ritel kebutuhan warga dan lembaga keuangan mikro syariah penggerak ekonomi usaha kecil umat.", "Kompleks Pertokoan PCM Masaran, Jl. Raya Solo - Sragen KM 13", "amal_usaha/aum_ekonomi.jpg", "amal_usaha/aum_bmt.jpg"),
                ("Padepokan Tapak Suci Pimda 058 Cabang Masaran", "sosial", "Pusat pelatihan bela diri pencak silat prestasi dan kaderisasi generasi muda persyarikatan.", "Gedung Olahraga PCM Masaran", "amal_usaha/aum_tapak_suci.jpg", "amal_usaha/aum_tapak_suci.jpg"),
            ]
            for nama, bidang, deskripsi, alamat, src_rel, dst_rel in aum_data:
                gbr_rel = copy_asset(src_rel, dst_rel)
                AmalUsaha.objects.create(
                    nama=nama,
                    bidang=bidang,
                    deskripsi=deskripsi,
                    alamat=alamat,
                    gambar=gbr_rel
                )
            self.stdout.write(self.style.SUCCESS(f"✓ {len(aum_data)} Amal Usaha berhasil dibuat"))

        if not Berita.objects.exists():
            now = timezone.now()
            berita_data = [
                (
                    "Rapat Kerja Cabang (Rakercab) PCM Masaran Sukses Menetapkan Program Prioritas 2026",
                    "Musyawarah kerja pimpinan pleno bersama majelis dan ortom menetapkan digitalisasi dakwah dan penguatan ranting sebagai target kerja utama.",
                    "Masaran, Sragen — Pimpinan Cabang Muhammadiyah (PCM) Masaran menyelenggarakan Rapat Kerja Cabang (Rakercab) dengan dihadiri segenap pimpinan harian, ketua majelis, perwakilan ortom, serta pimpinan ranting se-Kecamatan Masaran.\n\nDalam sambutannya, Ketua PCM Masaran H. Siyamto Umardani, S.Ag., menegaskan pentingnya sinergi antara persyarikatan dan amal usaha. 'Kita berkomitmen mengoptimalkan peran dakwah pencerahan di masyarakat bawah melalui penguatan pembinaan masjid dan ranting,' ungkap beliau.\n\nRakercab menghasilkan sejumlah konsensus strategis, di antaranya percepatan sertifikasi tanah wakaf, digitalisasi sistem informasi persyarikatan, serta revitalisasi Lazismu.",
                    "berita/berita_rakercab.jpg",
                    "berita/berita_rakercab.jpg",
                    now - timedelta(days=2),
                    "terbit"
                ),
                (
                    "Ribuan Warga Padati Jalan Sehat Akbar Milad Muhammadiyah Ke-113 di Masaran",
                    "Peringatan Milad Muhammadiyah ke-113 di Cabang Masaran berlangsung semarak dengan diikuti ribuan peserta dari berbagai elemen masyarakat.",
                    "Masaran, Sragen — Suasana hangat dan penuh keceriaan menyelimuti Jalan Raya Solo-Sragen saat ribuan peserta mengikuti Jalan Sehat Milad Muhammadiyah ke-113 tingkat Cabang Masaran.\n\nAcara dibuka langsung oleh jajaran PDM Sragen dan Pimpinan Cabang Masaran. Hadir siswa-siswi dari TK ABA, SD/MI Muhammadiyah, SMP/MTs, hingga SMA/SMK se-Masaran. Ratusan doorprize menarik dibagikan untuk menyemarakkan kegiatan silaturahmi akbar ini.",
                    "berita/berita_jalan_sehat.jpg",
                    "berita/berita_jalan_sehat.jpg",
                    now - timedelta(days=5),
                    "terbit"
                ),
                (
                    "Kajian Ahad Pagi Gedung Dakwah Masaran Ulas Fikih Muamalah dan Kebangsaan",
                    "Kajian rutin Ahad pagi di Gedung Dakwah PCM Masaran terus menjadi magnet pencerahan bagi ribuan jamaah dari pelosok desa.",
                    "Masaran — Pengajian Ahad Pagi yang diselenggarakan oleh Majelis Tabligh PCM Masaran kembali dipadati jamaah. Pembicara mengingatkan jamaah mengenai pentingnya menjaga ketauhidan yang kokoh di tengah arus modernitas.\n\nKajian rutin ini berlangsung setiap pekan mulai pukul 06.00 hingga 07.30 WIB dan disiarkan secara langsung melalui kanal YouTube resmi Muhammadiyah Masaran.",
                    "berita/berita_pengajian_ahad.jpg",
                    "berita/berita_pengajian_ahad.jpg",
                    now - timedelta(days=9),
                    "terbit"
                ),
                (
                    "Musyawarah Ranting PRM Kliwonan Tetapkan Kepengurusan Baru Periode Muktamar",
                    "Pimpinan Ranting Muhammadiyah Kliwonan sukses menyelenggarakan Musyran dengan suasana guyub dan menghasilkan kepengurusan yang solid.",
                    "Kliwonan, Masaran — Musyawarah Ranting (Musyran) Muhammadiyah dan 'Aisyiyah Kliwonan berlangsung di Balai Pertemuan Ranting. Acara ini merupakan wujud konsolidasi organisasi di tingkat akar rumput untuk menggerakkan dakwah berbasis jamaah desa.",
                    "berita/berita_musyran_kliwonan.jpg",
                    "berita/berita_musyran_kliwonan.jpg",
                    now - timedelta(days=14),
                    "terbit"
                ),
                (
                    "Atlet Tapak Suci Masaran Sabet Juara Umum Kejurda TSPM Pimda 058 Sragen",
                    "Pesilat muda Tapak Suci binaan PCM Masaran menunjukkan ketangguhan dengan meraih medali emas dalam Kejuaraan Daerah Seni dan Tanding.",
                    "Sragen — Kontingen pesilat Tapak Suci Putera Muhammadiyah Cabang Masaran berhasil mencatatkan prestasi gemilang dalam Kejurda 2026. Pembina Tapak Suci Masaran menyampaikan rasa syukur dan apresiasi atas dedikasi para atlet muda yang gigih berlatih.",
                    "berita/berita_tapak_suci.jpg",
                    "berita/berita_tapak_suci.jpg",
                    now - timedelta(days=20),
                    "terbit"
                ),
                (
                    "Musyran PRM Sidodadi Kuatkan Gerakan Jamaah dan Pengelolaan Wakaf Produktif",
                    "PRM Sidodadi menggelar Musyawarah Ranting ke-48 untuk memperkuat amal usaha dan penataan aset persyarikatan di desanya.",
                    "Sidodadi, Masaran — Bertempat di kompleks MIM Sidodadi, Musyawarah Ranting berjalan khidmat dan demokratis. Agenda difokuskan pada penguatan dakwah kultural dan pemanfaatan wakaf produktif untuk kemaslahatan warga sekitar.",
                    "berita/berita_musyran_sidodadi.jpg",
                    "berita/berita_musyran_sidodadi.jpg",
                    now - timedelta(days=28),
                    "terbit"
                ),
                (
                    "Kunjungan Silaturahmi PCM Masaran ke PRM Labuhan Paciran Pererat Studi Dakwah",
                    "Rombongan pengurus PCM Masaran mengadakan studi komparasi pemberdayaan masyarakat dan ranting percontohan di Jawa Timur.",
                    "Masaran — Jajaran pimpinan pleno PCM Masaran mengadakan lawatan studi banding dakwah ke PRM Labuhan, Paciran, Lamongan. Kunjungan ini dimaksudkan untuk mengadopsi model pemberdayaan ranting mandiri dan pengelolaan baitul mal di tingkat cabang.",
                    "berita/berita_silaturahmi_prm.jpg",
                    "berita/berita_silaturahmi_prm.jpg",
                    now - timedelta(days=35),
                    "terbit"
                ),
                (
                    "Dokumentasi Musyawarah Cabang (Musycab) Ke-48 PCM dan PCA Masaran",
                    "Kilas balik Musycab ke-48 yang telah sukses memilih 11 formatur terpilih serta menyusun Garis-Garis Besar Program Cabang.",
                    "Masaran — Musycab ke-48 PCM Masaran telah terlaksana dengan lancar dan penuh ukhuwah. Kepengurusan baru periode 2022–2027 dikukuhkan secara resmi oleh PDM Sragen melalui SK No. 032/KEP/III.0/D/2023.",
                    "berita/berita_musycab.jpg",
                    "berita/berita_musycab.jpg",
                    now - timedelta(days=45),
                    "terbit"
                ),
                (
                    "[DRAF RAHASIA] Rencana Pembangunan Pusat Dakwah Baru 2027",
                    "Rancangan draf internal pimpinan yang belum dipublikasikan kepada khalayak umum.",
                    "Isi dokumen draf ini bersifat rahasia dan internal pimpinan PCM Masaran.",
                    "berita/berita_rakercab.jpg",
                    "berita/berita_rakercab_draf.jpg",
                    now - timedelta(days=1),
                    "draf"
                ),
            ]
            for judul, ringkasan, isi, src_rel, dst_rel, tgl, status in berita_data:
                gbr_rel = copy_asset(src_rel, dst_rel)
                Berita.objects.create(
                    judul=judul,
                    ringkasan=ringkasan,
                    isi=isi,
                    gambar_sampul=gbr_rel,
                    tanggal_terbit=tgl,
                    status_terbit=status
                )
            self.stdout.write(self.style.SUCCESS(f"✓ {len(berita_data)} Berita berhasil dibuat (termasuk 1 draf)"))

        if not Agenda.objects.exists():
            now = timezone.now()
            agenda_data = [
                ("Pengajian Ahad Pagi Akbar PCM Masaran", now + timedelta(days=3, hours=6), "Gedung Dakwah Muhammadiyah Masaran", "Pengajian rutin Ahad pagi bersama jajaran PDM Sragen dan seluruh warga persyarikatan se-Kecamatan Masaran."),
                ("Kajian Majelis Dikdasmen & Pembinaan Guru AUM", now + timedelta(days=8, hours=8), "Aula SMK Muhammadiyah 10 Masaran", "Pembinaan ideologi Al-Islam dan Kemuhammadiyahan untuk seluruh pendidik dan tenaga kependidikan."),
                ("Rapat Koordinasi LPCR PCM Masaran Bersama 13 PRM", now + timedelta(days=14, hours=19), "Ruang Rapat Pleno Gedung Dakwah Masaran", "Monitoring program kerja ranting dan evaluasi keaktifan jamaah masjid."),
                ("Pemeriksaan Kesehatan Gratis & Donor Darah Lazismu", now + timedelta(days=21, hours=8), "Klinik Pratama PKU Muhammadiyah Masaran", "Bakti sosial pelayanan kesehatan bagi lansia dan dhuafa di wilayah Masaran."),
                ("Kajian Iftitah Ramadhan 1445 H dan Sosialisasi Hisab", now - timedelta(days=20, hours=10), "Gedung Dakwah Muhammadiyah Masaran", "Sosialisasi penetapan awal Ramadhan sesuai Maklumat PP Muhammadiyah."),
                ("Resepsi Milad Muhammadiyah Ke-113 Tingkat Cabang", now - timedelta(days=40, hours=7), "Lapangan Desa Masaran", "Pentas seni santri, bazar UMKM, dan tabligh akbar milad persyarikatan."),
            ]
            for nama, waktu, tempat, ket in agenda_data:
                Agenda.objects.create(
                    nama_kegiatan=nama,
                    waktu_mulai=waktu,
                    tempat=tempat,
                    keterangan=ket
                )
            self.stdout.write(self.style.SUCCESS(f"✓ {len(agenda_data)} Agenda kegiatan berhasil dibuat"))

        if not Dokumen.objects.exists():
            doc_data = [
                ("SK PWM Jawa Tengah No. 066/KEP/II.0/B/2026 - Piagam Pengesahan Pendirian PCM Masaran 1935", "Piagam resmi pengesahan pendirian Pimpinan Cabang Muhammadiyah Masaran tertanggal 17 November 1935 M (20 Sya'ban 1354 H) oleh Pimpinan Wilayah Muhammadiyah Jawa Tengah.", "dokumen/sk_pengesahan_pendirian_pcm_masaran_1935.pdf", "dokumen/sk_pengesahan_pendirian_pcm_masaran_1935.pdf"),
                ("SK PDM Sragen No. 032/KEP/III.0/D/2023 - Penetapan Hasil Musycab ke-48", "Surat Keputusan PDM Sragen tentang penetapan 13 Anggota Pleno / Formatur PCM Masaran Periode Muktamar ke-48 (2022–2027).", "dokumen/sk_032_pdm_sragen_pengurus_pcm_masaran_2022_2027.pdf", "dokumen/sk_032_pdm_sragen_pengurus_pcm_masaran_2022_2027.pdf"),
                ("Struktur Pengurus Paripurna PCM Masaran Periode 2022–2027", "Bagan struktur organisasi lengkap meliputi Penasehat, 13 Pimpinan Pleno Koordinator, serta 18 Majelis dan Lembaga Pembantu Pimpinan.", "dokumen/struktur_pengurus_pcm_masaran_2022_2027_paripurna.pdf", "dokumen/struktur_pengurus_pcm_masaran_2022_2027_paripurna.pdf"),
                ("Pedoman Penyelenggaraan Ranting Muhammadiyah (LPCR)", "Panduan baku tata kelola keorganisasian, administrasi surat-menyurat, dan pembinaan jamaah tingkat ranting.", "dokumen/panduan_organisasi_ranting.pdf", "dokumen/panduan_organisasi_ranting.pdf"),
            ]
            for judul, ket, src_rel, dst_rel in doc_data:
                berkas_rel = copy_asset(src_rel, dst_rel)
                Dokumen.objects.create(
                    judul=judul,
                    keterangan=ket,
                    berkas=berkas_rel
                )
            self.stdout.write(self.style.SUCCESS(f"✓ {len(doc_data)} Dokumen unduhan berhasil dibuat"))

        if not TautanTerkait.objects.exists():
            tautan_data = [
                ("Pimpinan Daerah Muhammadiyah (PDM) Sragen", "https://muhammadiyahsragen.or.id", 1),
                ("Pimpinan Wilayah Muhammadiyah (PWM) Jawa Tengah", "https://pwmjateng.com", 2),
                ("Pimpinan Pusat (PP) Muhammadiyah", "https://muhammadiyah.or.id", 3),
                ("Portal Berita Suara Muhammadiyah", "https://suaramuhammadiyah.id", 4),
                ("Lembaga Amil Zakat Lazismu Jawa Tengah", "https://lazismujateng.org", 5),
            ]
            for nama, url, urutan in tautan_data:
                TautanTerkait.objects.create(
                    nama=nama,
                    url=url,
                    urutan=urutan
                )
            self.stdout.write(self.style.SUCCESS(f"✓ {len(tautan_data)} Tautan Persyarikatan berhasil dibuat"))

        from django.contrib.auth.models import User
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@pcm-masaran.or.id", "adminpcm2026")
            self.stdout.write(self.style.SUCCESS("✓ Superuser demo 'admin' (password: adminpcm2026) berhasil dibuat"))
        else:
            admin_user = User.objects.get(username="admin")
            admin_user.set_password("adminpcm2026")
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("✓ Superuser demo 'admin' password dipastikan 'adminpcm2026'"))

        self.stdout.write(self.style.SUCCESS("\n🎉 Seluruh data riil PCM Masaran berhasil diisi ke database!"))
