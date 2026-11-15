from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from pcm.models import (
    ProfilOrganisasi,
    Pimpinan,
    Ranting,
    AmalUsaha,
    Berita,
    Agenda,
    Dokumen,
    PesanMasuk,
    TautanTerkait
)


class PCMWebsiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.now = timezone.now()

        # 1. Profil Organisasi
        self.profil = ProfilOrganisasi.objects.create(
            nama="Pimpinan Cabang Muhammadiyah Masaran",
            nama_singkat="PCM Masaran",
            tagline="Mencerahkan Semesta, Memajukan Masaran",
            tentang="Tentang PCM Masaran di Sragen.",
            sejarah="Sejarah berdiri sejak 1960.",
            visi="Visi masyarakat Islam sebenar-benarnya.",
            misi="Misi 1\nMisi 2\nMisi 3",
            alamat_sekretariat="Gedung Dakwah Muhammadiyah Masaran",
            telepon="(0271) 8821032",
            email="pcm.masaran@gmail.com",
            jumlah_anggota_ktam=1250,
        )

        # 2. Pimpinan
        self.pimpinan = Pimpinan.objects.create(
            nama="H. Siyamto Umardani, S.Ag.",
            jabatan="Ketua Cabang",
            periode="2022–2027",
            urutan=1
        )

        # 3. Ranting
        self.ranting = Ranting.objects.create(
            nama_ranting="Masaran",
            ketua="H. Suratno",
            alamat="Kompleks Masjid Baiturrahman",
            telepon="(0271) 8821035"
        )

        # 4. Amal Usaha
        self.amal_usaha = AmalUsaha.objects.create(
            nama="SMK Muhammadiyah 10 Masaran",
            bidang="pendidikan",
            deskripsi="SMK Pusat Keunggulan",
            alamat="Jl. Raya Masaran"
        )

        # 5. Berita Terbit
        self.berita_terbit = Berita.objects.create(
            judul="Kajian Ahad Pagi Akbar Masaran",
            ringkasan="Ringkasan kajian akbar.",
            isi="Isi lengkap artikel pengajian di Gedung Dakwah.",
            tanggal_terbit=self.now - timedelta(days=1),
            status_terbit="terbit"
        )

        # 6. Berita Draf
        self.berita_draf = Berita.objects.create(
            judul="Rencana Kegiatan Rahasia Internal",
            ringkasan="Ringkasan draf rahasia.",
            isi="Isi artikel draf yang belum terbit.",
            tanggal_terbit=self.now - timedelta(days=1),
            status_terbit="draf"
        )

        # 7. Berita Masa Depan
        self.berita_future = Berita.objects.create(
            judul="Berita di Masa Depan 2030",
            ringkasan="Ringkasan masa depan.",
            isi="Isi berita masa depan.",
            tanggal_terbit=self.now + timedelta(days=10),
            status_terbit="terbit"
        )

        # 8. Agenda
        self.agenda_mendatang = Agenda.objects.create(
            nama_kegiatan="Pengajian Ahad Pagi Pekan Depan",
            waktu_mulai=self.now + timedelta(days=3),
            tempat="Gedung Dakwah Masaran"
        )

        # 9. Tautan
        self.tautan = TautanTerkait.objects.create(
            nama="PDM Sragen",
            url="https://muhammadiyahsragen.or.id",
            urutan=1
        )

    def test_semua_halaman_publik_200(self):
        """Uji 1: Semua halaman publik dapat diakses dengan HTTP Status 200."""
        urls = [
            reverse('pcm:beranda'),
            reverse('pcm:profil'),
            reverse('pcm:pimpinan'),
            reverse('pcm:ranting'),
            reverse('pcm:amal_usaha'),
            reverse('pcm:berita_list'),
            reverse('pcm:agenda'),
            reverse('pcm:unduhan'),
            reverse('pcm:kontak'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                f"URL {url} gagal diakses, status code: {response.status_code}"
            )

    def test_berita_terbit_200_and_draf_404(self):
        """Uji 2: Berita terbit mengembalikan 200, berita draf atau bertanggal di masa depan WAJIB 404."""
        # Berita terbit -> 200
        url_terbit = reverse('pcm:berita_detail', kwargs={'slug': self.berita_terbit.slug})
        resp_terbit = self.client.get(url_terbit)
        self.assertEqual(resp_terbit.status_code, 200)

        # Berita draf -> 404
        url_draf = reverse('pcm:berita_detail', kwargs={'slug': self.berita_draf.slug})
        resp_draf = self.client.get(url_draf)
        self.assertEqual(resp_draf.status_code, 404)

        # Berita masa depan -> 404
        url_future = reverse('pcm:berita_detail', kwargs={'slug': self.berita_future.slug})
        resp_future = self.client.get(url_future)
        self.assertEqual(resp_future.status_code, 404)

    def test_formulir_kontak_menyimpan_pesan(self):
        """Uji 3: Formulir kontak publik menyimpan pesan ke database dan menampilkan pesan sukses."""
        data = {
            'nama': 'Ahmad Dahlan',
            'email': 'ahmad@example.com',
            'subjek': 'Kerjasama Pengajian Ranting',
            'pesan': 'Assalamu alaikum, kami ingin mengajukan jadwal penceramah untuk ranting kami.',
        }
        url_kontak = reverse('pcm:kontak')
        response = self.client.post(url_kontak, data=data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Pastikan data tersimpan di tabel PesanMasuk
        pesan = PesanMasuk.objects.filter(email='ahmad@example.com').first()
        self.assertIsNotNone(pesan)
        self.assertEqual(pesan.nama, 'Ahmad Dahlan')
        self.assertEqual(pesan.subjek, 'Kerjasama Pengajian Ranting')

    def test_profil_organisasi_singleton(self):
        """Uji 4: Profil Organisasi hanya boleh ada 1 baris di database (singleton check)."""
        duplikat = ProfilOrganisasi(
            nama="Profil Duplikat PCM",
            nama_singkat="Duplikat",
            tagline="Tagline",
            tentang="Tentang",
            sejarah="Sejarah",
            visi="Visi",
            misi="Misi",
            alamat_sekretariat="Alamat",
            telepon="123",
            email="duplikat@test.com",
            jumlah_anggota_ktam=100
        )
        with self.assertRaises(ValidationError):
            duplikat.clean()

    def test_berita_auto_slug_uniqueness(self):
        """Uji 5: Pembuatan berita dengan judul identik otomatis menghasilkan slug unik tanpa tabrakan."""
        b1 = Berita.objects.create(
            judul="Pengajian Akbar Milad Masaran",
            ringkasan="Ringkasan 1",
            isi="Isi 1",
            status_terbit="terbit"
        )
        b2 = Berita.objects.create(
            judul="Pengajian Akbar Milad Masaran",
            ringkasan="Ringkasan 2",
            isi="Isi 2",
            status_terbit="terbit"
        )
        self.assertNotEqual(b1.slug, b2.slug)
        self.assertTrue(b2.slug.startswith("pengajian-akbar-milad-masaran-"))

    def test_berita_custom_manager_published(self):
        """Uji 6: Custom manager Berita.objects.published() hanya memfilter berita terbit & tidak masa depan."""
        published_qs = Berita.objects.published()
        self.assertIn(self.berita_terbit, published_qs)
        self.assertNotIn(self.berita_draf, published_qs)
        self.assertNotIn(self.berita_future, published_qs)
