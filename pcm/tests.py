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

        self.profil = ProfilOrganisasi.objects.create(
            nama="Pimpinan Cabang Muhammadiyah Masaran",
            nama_singkat="PCM Masaran",
            tagline="Mencerahkan Semesta, Memajukan Masaran",
            tentang="Tentang PCM Masaran di Sragen.",
            sejarah="Sejarah berdiri sejak 17 November 1935 M.",
            visi="Terwujudnya masyarakat Islam yang sebenar-benarnya.",
            misi="Menegakkan Tauhid yang murni.\nMenyebarluaskan Ajaran Islam.\nMewujudkan Islam dalam kehidupan.",
            alamat_sekretariat="Gedung Dakwah Muhammadiyah Masaran",
            telepon="(0271) 8821032",
            email="pcm.masaran@gmail.com",
            jumlah_anggota_ktam=1250,
        )

        self.pimpinan = Pimpinan.objects.create(
            nama="H. Siyamto Umardani, S.Ag.",
            jabatan="Ketua Cabang",
            periode="2022–2027",
            urutan=1
        )

        self.ranting = Ranting.objects.create(
            nama_ranting="Masaran",
            ketua="H. Suratno",
            alamat="Kompleks Masjid Baiturrahman",
            telepon="(0271) 8821035"
        )

        self.amal_usaha = AmalUsaha.objects.create(
            nama="SMK Muhammadiyah 10 Masaran",
            bidang="pendidikan",
            deskripsi="SMK Pusat Keunggulan",
            alamat="Jl. Raya Masaran"
        )

        self.berita_terbit = Berita.objects.create(
            judul="Kajian Ahad Pagi Akbar Masaran",
            ringkasan="Ringkasan kajian akbar.",
            isi="Isi lengkap artikel pengajian di Gedung Dakwah.",
            tanggal_terbit=self.now - timedelta(days=1),
            status_terbit="terbit"
        )

        self.berita_draf = Berita.objects.create(
            judul="Rencana Kegiatan Rahasia Internal",
            ringkasan="Ringkasan draf rahasia.",
            isi="Isi artikel draf yang belum terbit.",
            tanggal_terbit=self.now - timedelta(days=1),
            status_terbit="draf"
        )

        self.berita_future = Berita.objects.create(
            judul="Berita di Masa Depan 2030",
            ringkasan="Ringkasan masa depan.",
            isi="Isi berita masa depan.",
            tanggal_terbit=self.now + timedelta(days=10),
            status_terbit="terbit"
        )

        self.agenda_mendatang = Agenda.objects.create(
            nama_kegiatan="Pengajian Ahad Pagi Pekan Depan",
            waktu_mulai=self.now + timedelta(days=3),
            tempat="Gedung Dakwah Masaran"
        )

        self.tautan = TautanTerkait.objects.create(
            nama="PDM Sragen",
            url="https://muhammadiyahsragen.or.id",
            urutan=1
        )

    def test_semua_halaman_publik_200(self):
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
        url_terbit = reverse('pcm:berita_detail', kwargs={'slug': self.berita_terbit.slug})
        resp_terbit = self.client.get(url_terbit)
        self.assertEqual(resp_terbit.status_code, 200)

        url_draf = reverse('pcm:berita_detail', kwargs={'slug': self.berita_draf.slug})
        resp_draf = self.client.get(url_draf)
        self.assertEqual(resp_draf.status_code, 404)

        url_future = reverse('pcm:berita_detail', kwargs={'slug': self.berita_future.slug})
        resp_future = self.client.get(url_future)
        self.assertEqual(resp_future.status_code, 404)

    def test_formulir_kontak_menyimpan_pesan(self):
        data = {
            'nama': 'Ahmad Dahlan',
            'email': 'ahmad@example.com',
            'subjek': 'Kerjasama Pengajian Ranting',
            'pesan': 'Assalamu alaikum, kami ingin mengajukan jadwal penceramah untuk ranting kami.',
        }
        url_kontak = reverse('pcm:kontak')
        response = self.client.post(url_kontak, data=data, follow=True)
        self.assertEqual(response.status_code, 200)

        pesan = PesanMasuk.objects.filter(email='ahmad@example.com').first()
        self.assertIsNotNone(pesan)
        self.assertEqual(pesan.nama, 'Ahmad Dahlan')
        self.assertEqual(pesan.subjek, 'Kerjasama Pengajian Ranting')

    def test_profil_organisasi_singleton(self):
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
        published_qs = Berita.objects.published()
        self.assertIn(self.berita_terbit, published_qs)
        self.assertNotIn(self.berita_draf, published_qs)
        self.assertNotIn(self.berita_future, published_qs)

    def test_unduhan_search_filter(self):
        Dokumen.objects.create(
            judul="Surat Keputusan PWM Jateng No 066",
            keterangan="Piagam Pendirian Resmi PCM Masaran",
            berkas="dokumen/test_doc.pdf"
        )
        url = reverse('pcm:unduhan') + "?q=066"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Surat Keputusan PWM Jateng No 066")

        url_empty = reverse('pcm:unduhan') + "?q=dokumen_tidak_ada_xyz"
        response_empty = self.client.get(url_empty)
        self.assertEqual(response_empty.status_code, 200)
        self.assertNotContains(response_empty, "Surat Keputusan PWM Jateng No 066")

    def test_agenda_upcoming_vs_past(self):
        url = reverse('pcm:agenda')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('agenda_akan_datang', response.context)
        self.assertIn('agenda_terlaksana', response.context)
        self.assertIn(self.agenda_mendatang, response.context['agenda_akan_datang'])

    def test_ranting_str_representation_and_ordering(self):
        r1 = Ranting.objects.create(
            nama_ranting="Dawungan",
            ketua="Ketua Dawungan",
            alamat="Desa Dawungan"
        )
        r2 = Ranting.objects.create(
            nama_ranting="Pilang",
            ketua="Ketua Pilang",
            alamat="Desa Pilang"
        )
        self.assertEqual(str(r1), "Dawungan")
        self.assertEqual(str(r2), "Pilang")
        rantings = list(Ranting.objects.values_list('nama_ranting', flat=True))
        self.assertEqual(rantings, sorted(rantings))

    def test_amal_usaha_str_and_bidang_choices(self):
        au = AmalUsaha.objects.create(
            nama="Klinik PKU Muhammadiyah Masaran",
            bidang="kesehatan",
            deskripsi="Pelayanan kesehatan masyarakat",
            alamat="Masaran"
        )
        self.assertEqual(str(au), "Klinik PKU Muhammadiyah Masaran (Kesehatan)")
        valid_keys = [k for k, _ in AmalUsaha.BIDANG_CHOICES]
        self.assertIn(au.bidang, valid_keys)

    def test_kontak_form_invalid_email_and_empty_fields(self):
        url_kontak = reverse('pcm:kontak')
        data_invalid = {
            'nama': 'Pengirim Test',
            'email': 'bukan-email-valid',
            'subjek': 'Judul',
            'pesan': 'Isi pesan test',
        }
        response = self.client.post(url_kontak, data=data_invalid)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(PesanMasuk.objects.filter(nama='Pengirim Test').exists())

    def test_dokumen_clean_and_pesan_masuk_defaults(self):
        doc = Dokumen(
            judul="Dokumen Uji Coba Ukuran Normal",
            keterangan="Keterangan uji coba",
            berkas="dokumen/sample.pdf"
        )
        doc.clean()
        self.assertEqual(doc.judul, "Dokumen Uji Coba Ukuran Normal")

        pesan = PesanMasuk.objects.create(
            nama="Uji Coba Default",
            email="uji@example.com",
            subjek="Subjek Uji",
            pesan="Isi pesan uji"
        )
        self.assertFalse(pesan.sudah_dibaca)
        pesan.sudah_dibaca = True
        pesan.save()
        self.assertTrue(PesanMasuk.objects.get(pk=pesan.pk).sudah_dibaca)
