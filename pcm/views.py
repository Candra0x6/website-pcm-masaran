from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from .models import (
    ProfilOrganisasi,
    Pimpinan,
    Ranting,
    AmalUsaha,
    Berita,
    Agenda,
    Dokumen
)
from .forms import KontakForm


MAJELIS_LEMBAGA_LIST = [
    {
        "nama": "Majelis Pembina Kesehatan Umum dan Pelayanan Sosial (MPKU)",
        "singkatan": "MPKU",
        "ketua": "H. Sukiswanto, S.Pd",
        "sekretaris": "Sukarman Kembangan",
        "koordinator": "Drs. H. Taslim Daryanto, M.Pd (Wakil Sekretaris)",
        "kategori": "Majelis",
        "deskripsi": "Mengkoordinasikan pelayanan kesehatan umum PKU Muhammadiyah dan bakti sosial kemasyarakatan se-Kecamatan Masaran."
    },
    {
        "nama": "Majelis Pembinaan Kader – Sumber Daya Insani (MPK-SDI)",
        "singkatan": "MPK-SDI",
        "ketua": "Iksanuddin, S.Ag",
        "sekretaris": "Sajiman, S.Ag",
        "koordinator": "Parlan Sinung Darsono (Wakil Ketua III)",
        "kategori": "Majelis",
        "deskripsi": "Pembibitan kader, Baitul Arqam, dan penguatan ideologi persyarikatan bagi seluruh pimpinan dan guru AUM."
    },
    {
        "nama": "Majelis Pendayagunaan Wakaf",
        "singkatan": "Wakaf",
        "ketua": "Drs. H. Sabar Sholihin",
        "sekretaris": "Endang Ismei",
        "koordinator": "H. Suyatno, S.Sos, M.Si (Wakil Ketua IV)",
        "kategori": "Majelis",
        "deskripsi": "Inventarisasi, sertifikasi tanah wakaf persyarikatan, serta optimalisasi aset untuk kemaslahatan umat."
    },
    {
        "nama": "Majelis Ekonomi dan Kewirausahaan (MEK)",
        "singkatan": "MEK",
        "ketua": "Ari Rudianto, SE",
        "sekretaris": "Supriyono",
        "koordinator": "Dr. H. Suharno, ST, MT (Wakil Ketua VIII)",
        "kategori": "Majelis",
        "deskripsi": "Pengembangan unit usaha produktif, kemitraan pertanian SPPGM Tangen, BMT, dan pembinaan UMKM jamaah."
    },
    {
        "nama": "Majelis Pustaka dan Informasi (MPI)",
        "singkatan": "MPI",
        "ketua": "Jumadi, S.Pd",
        "sekretaris": "Ery Munandar, S.Sos",
        "koordinator": "Dr. H. Basuki Agus Suparno, M.Si (Wakil Ketua VI)",
        "kategori": "Majelis",
        "deskripsi": "Pengelolaan portal web resmi, dakwah siber digital, arsip historis, dan keterbukaan informasi persyarikatan."
    },
    {
        "nama": "Majelis Pendidikan Dasar dan Menengah (Dikdasmen)",
        "singkatan": "Dikdasmen",
        "ketua": "H. Mulyanto, S.Pd, M.Pd",
        "sekretaris": "Arif Sumoro, S.Pd",
        "koordinator": "Dr. Purwadi, M.Pd (Wakil Ketua VII)",
        "kategori": "Majelis",
        "deskripsi": "Membina dan mengelola jaringan sekolah (SMK 10, SMA 3, SMP 2, MTs 3, SD Terpadu, MIM) menuju sekolah unggul."
    },
    {
        "nama": "Majelis Pemberdayaan Masyarakat (MPM)",
        "singkatan": "MPM",
        "ketua": "Eko Priyanto, S.Pd",
        "sekretaris": "Supadi, S.E, S.Pd, M.Pd",
        "koordinator": "Giyamto, S.Pd (Wakil Ketua I)",
        "kategori": "Majelis",
        "deskripsi": "Pendampingan petani gabah, kelompok ternak, nelayan air tawar, dan pemberdayaan ekonomi kaum dhuafa."
    },
    {
        "nama": "Majelis Tabligh, Tarjih, dan Tajdid (MTTT)",
        "singkatan": "Tabligh-Tarjih",
        "ketua": "Sukarno, S.Ag",
        "sekretaris": "H. Nur Salim, S.Ag",
        "koordinator": "Muhammad Marjuki, S.Pd (Wakil Ketua V)",
        "kategori": "Majelis",
        "deskripsi": "Pengkajian fatwa hisab dan tarjih, pembinaan korp muballigh, serta penyelenggaraan Pengajian Ahad Pagi Akbar."
    },
    {
        "nama": "Majelis Lingkungan Hidup (MLH)",
        "singkatan": "MLH",
        "ketua": "H. Juwadi, M.Si",
        "sekretaris": "Sungadi, SH",
        "koordinator": "H. Suyatno, S.Sos, M.Si (Wakil Ketua IV)",
        "kategori": "Majelis",
        "deskripsi": "Edukasi kelestarian alam, mitigasi krisis iklim, pengelolaan sampah masjid, dan penghijauan ranting."
    },
    {
        "nama": "Majelis Hukum HAM dan Bantuan Hukum",
        "singkatan": "Hukum & HAM",
        "ketua": "Joko Sulistyo, S.Pd",
        "sekretaris": "Suparno, SH",
        "koordinator": "Dr. H. Basuki Agus Suparno, M.Si (Wakil Ketua VI)",
        "kategori": "Majelis",
        "deskripsi": "Advokasi legal persyarikatan, pendampingan hukum warga dhuafa, dan penyuluhan kesadaran hukum."
    },
    {
        "nama": "Lembaga Resiliensi Bencana (LRB / MDMC)",
        "singkatan": "MDMC",
        "ketua": "M. Amin Rois",
        "sekretaris": "Nova Zakariya",
        "koordinator": "Muslih, S.Pd (Wakil Bendahara)",
        "kategori": "Lembaga",
        "deskripsi": "Tanggap darurat bencana alam, relawan kebencanaan MDMC, pelatihan mitigasi, dan kesiapsiagaan ranting."
    },
    {
        "nama": "Lembaga Pembinaan Haji dan Umroh (LPHU)",
        "singkatan": "LPHU",
        "ketua": "Drs. H. Teguh",
        "sekretaris": "H. Ramelan, S.Pd, M.Pd",
        "koordinator": "H. Sumarno, S.Th.I (Wakil Ketua II)",
        "kategori": "Lembaga",
        "deskripsi": "Bimbingan manasik haji dan umroh mandiri, silaturahmi alumni jamaah, dan pembinaan kemabruran."
    },
    {
        "nama": "Lembaga Pembinaan dan Pengawasan Keuangan (LPPK)",
        "singkatan": "LPPK",
        "ketua": "Gatot Widiarto, SE",
        "sekretaris": "Arif BJ, S.P",
        "koordinator": "H. Sumarno, S.Th.I (Wakil Ketua II)",
        "kategori": "Lembaga",
        "deskripsi": "Audit internal berkala, standardisasi tata kelola akuntansi keuangan cabang, ranting, dan seluruh AUM."
    },
    {
        "nama": "Lembaga Pengembangan Pesantren Muhammadiyah (LP2M)",
        "singkatan": "LP2M",
        "ketua": "Syamsiar Ahmadi, S.Ag",
        "sekretaris": "Iksan Darajat, S.Pd",
        "koordinator": "Dr. Purwadi, M.Pd (Wakil Ketua VII)",
        "kategori": "Lembaga",
        "deskripsi": "Pengembangan kurikulum kepesantrenan, asrama tahfidz, dan kaderisasi ulama tarjih muda."
    },
    {
        "nama": "Lembaga Pengembangan Cabang Ranting dan Pembinaan Masjid (LPCR-PM)",
        "singkatan": "LPCR-PM",
        "ketua": "Eko Budiyono, S.Pd",
        "sekretaris": "Kaswadi, S.Pd",
        "koordinator": "Muhammad Marjuki, S.Pd (Wakil Ketua V)",
        "kategori": "Lembaga",
        "deskripsi": "Penguatan organisasi 13 PRM se-Kecamatan Masaran, pemakmuran masjid, mushalla, dan jamaah ranting."
    },
    {
        "nama": "Lembaga Hikmah dan Kebijakan Publik (LHKP)",
        "singkatan": "LHKP",
        "ketua": "Eka Widiastono, S.Pd",
        "sekretaris": "Hanan Rustamaji, S.Sn",
        "koordinator": "Dr. H. Suharno, ST, MT (Wakil Ketua VIII)",
        "kategori": "Lembaga",
        "deskripsi": "Kajian kebijakan strategis publik daerah, sinergi Forkopimcam Masaran, dan wawasan kebangsaan."
    },
    {
        "nama": "Lembaga Amil Zakat Infak dan Shodaqoh (Lazismu Masaran)",
        "singkatan": "Lazismu",
        "ketua": "Agus SW, S.Pd",
        "sekretaris": "Irwan Susanto",
        "koordinator": "Giyamto, S.Pd (Wakil Ketua I)",
        "kategori": "Lembaga",
        "deskripsi": "Penghimpunan dan pendistribusian ZISKA untuk beasiswa santri, penanganan kemiskinan, dan layanan ambulans."
    },
    {
        "nama": "Lembaga Seni Budaya & Olahraga, Pembinaan AMM & Ortom (LSBO-AMM)",
        "singkatan": "LSBO-AMM",
        "ketua": "Habiburohman, S.Pd, M.Pd",
        "sekretaris": "M. Rizqon Bayu Aji, S.Pd",
        "koordinator": "Parlan Sinung Darsono (Wakil Ketua III)",
        "kategori": "Lembaga",
        "deskripsi": "Pembinaan ortom (Pemuda Muhammadiyah, Nasyiah, IPM, Tapak Suci, Hizbul Wathan) dan seni budaya Islam."
    }
]


def beranda_view(request):
    now = timezone.now()
    profil = ProfilOrganisasi.objects.first()
    
    total_ranting = Ranting.objects.count()
    total_amal_usaha = AmalUsaha.objects.count()
    total_ktam = profil.jumlah_anggota_ktam if profil else 1250

    berita_terbaru = Berita.objects.published().order_by('-tanggal_terbit')[:3]
    agenda_mendatang = Agenda.objects.filter(waktu_mulai__gte=now).order_by('waktu_mulai')[:3]

    aum_pendidikan = AmalUsaha.objects.filter(bidang='pendidikan', gambar__isnull=False).first()
    aum_kesehatan = AmalUsaha.objects.filter(bidang='kesehatan', gambar__isnull=False).first()
    aum_sosial = AmalUsaha.objects.filter(bidang='sosial', gambar__isnull=False).first()
    aum_ekonomi = AmalUsaha.objects.filter(bidang='ekonomi', gambar__isnull=False).first()
    amal_usaha_unggulan = [a for a in [aum_pendidikan, aum_kesehatan, aum_sosial, aum_ekonomi] if a]

    context = {
        'total_ranting': total_ranting,
        'total_amal_usaha': total_amal_usaha,
        'total_ktam': total_ktam,
        'berita_terbaru': berita_terbaru,
        'agenda_mendatang': agenda_mendatang,
        'amal_usaha_unggulan': amal_usaha_unggulan,
        'aum_pendidikan': aum_pendidikan,
        'aum_kesehatan': aum_kesehatan,
        'aum_sosial': aum_sosial,
        'aum_ekonomi': aum_ekonomi,
    }
    return render(request, 'pcm/beranda.html', context)


TUJUAN_BERDIRI_MUHAMMADIYAH = {
    'nama_pendiri': 'K.H. Ahmad Dahlan (Muhammad Darwis)',
    'masa_hidup': '1868 – 1923 M',
    'tanggal_hijriyah': '8 Dzulhijjah 1330 H',
    'tanggal_masehi': '18 November 1912 M',
    'tempat_berdiri': 'Kampung Kauman, Yogyakarta',
    'ayat_al_quran': 'وَلْتَكُن مِّنكُمْ أُمَّةٌۭ يَدْعُونَ إِلَى ٱلْخَيْرِ وَيَأْمُرُونَ بِٱلْمَعْرُوفِ وَيَنْهَوْنَ عَنِ ٱلْمُنكَرِ ۚ وَأُو۟لَـٰٓئِكَ هُمُ ٱلْمُفْلِحُونَ',
    'surat': 'Surat Ali \'Imran Ayat 104',
    'arti_ayat': 'Dan hendaklah ada di antara kamu segolongan umat yang menyeru kepada kebajikan, menyuruh kepada yang ma\'ruf dan mencegah dari yang munkar; merekalah orang-orang yang beruntung.',
    'maksud_dan_tujuan': 'Menegakkan dan menjunjung tinggi Agama Islam sehingga terwujud masyarakat Islam yang sebenar-benarnya.',
    'dasar_hukum_ad': 'Anggaran Dasar Muhammadiyah Bab III Pasal 4 Ayat 1',
    'latar_belakang': 'K.H. Ahmad Dahlan mendirikan persyarikatan Muhammadiyah dilandasi oleh kegelisahan mendalam atas keterbelakangan pendidikan umat Islam, maraknya amalan takhayul, bid\'ah, dan khurafat (TBC) yang mencemari kemurnian akidah, serta keprihatinan atas nasib kaum miskin dan anak-anak yatim yang terabaikan. Beliau menerjemahkan pemahaman teologis Surat Al-Ma\'un ke dalam praksis gerakan sosial modern melalui pendirian sekolah, rumah sakit (PKO), dan rumah yatim.',
    'foto_pendiri': 'https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=800&q=80',
    'tiga_pilar_gerakan': [
        {
            'judul': 'Gerakan Islam',
            'penjelasan': 'Gerakan yang beraqidah Islam, bersumber pada Al-Qur\'an dan As-Sunnah ash-Shahihah sebagai pedoman mutlak dalam seluruh aspek kehidupan.',
        },
        {
            'judul': 'Gerakan Dakwah Amar Ma\'ruf Nahi Munkar',
            'penjelasan': 'Mengajak kepada kebaikan dan mencegah kemungkaran yang ditujukan kepada perorangan maupun masyarakat luas secara persuasif dan bijaksana.',
        },
        {
            'judul': 'Gerakan Tajdid (Pembaruan)',
            'penjelasan': 'Melakukan purifikasi pemurnian akidah-ibadah dari syirik dan khurafat, serta dinamisasi pembaruan dalam muamalah dan ilmu pengetahuan.',
        },
    ],
}

PHIWM_DATA = {
    'judul': 'Pedoman Hidup Islami Warga Muhammadiyah (PHIWM)',
    'keputusan': 'Keputusan Muktamar Muhammadiyah ke-44 Tahun 2000 di Jakarta',
    'pengertian': 'PHIWM adalah pedoman nilai, norma, dan etika Islami yang menjadi rujukan moral bagi seluruh pimpinan, anggota, dan simpatisan Muhammadiyah dalam mengamalkan ajaran Islam secara kaffah guna mewujudkan keteladanan mulia (uswah hasanah).',
    'foto_buku': 'https://images.unsplash.com/photo-1532012164546-f432f2e3777a?auto=format&fit=crop&w=800&q=80',
    'dimensi_kehidupan': [
        {
            'nomor': '01',
            'kategori': 'Kehidupan Pribadi',
            'poin': 'Akidah, Ibadah, Akhlaq, & Mu\'amalah',
            'deskripsi': 'Warga Muhammadiyah wajib memurnikan tauhid dari syirik, beribadah tekun sesuai tuntunan Rasulullah SAW, memiliki kejujuran (shiddiq), amanah, dan mencari rezeki secara halal serta menjauhi riba.',
        },
        {
            'nomor': '02',
            'kategori': 'Kehidupan dalam Keluarga',
            'poin': 'Keluarga Sakinah Mawaddah Warahmah',
            'deskripsi': 'Mewujudkan rumah tangga Islami yang tentram, membina anak-anak dengan pendidikan tauhid dan akhlak sejak dini, membagi peran suami-istri secara adil dan penuh kasih sayang.',
        },
        {
            'nomor': '03',
            'kategori': 'Kehidupan Bermasyarakat',
            'poin': 'Kesantunan Sosial & Kerukunan',
            'deskripsi': 'Menjadi pelopor kedamaian antar-tetangga, mengedepankan tepa selira dan empati sosial, gemar menolong yang lemah (spirit Al-Ma\'un), serta menjaga kebersihan dan kelestarian lingkungan.',
        },
        {
            'nomor': '04',
            'kategori': 'Kehidupan Berorganisasi',
            'poin': 'Amanah, Keikhlasan, & Musyawarah',
            'deskripsi': 'Menjalankan amanah persyarikatan dengan ikhlas lillahi ta\'ala, mengutamakan musyawarah mufakat, loyal terhadap keputusan organisasi, dan tidak mencari keuntungan materi pribadi di persyarikatan.',
        },
        {
            'nomor': '05',
            'kategori': 'Kehidupan Mengelola Amal Usaha (AUM)',
            'poin': 'Profesionalisme & Misi Dakwah',
            'deskripsi': 'Menjadikan AUM sebagai media dakwah nyata dan wahana kaderisasi, menerapkan tata kelola yang transparan, akuntabel, serta memberikan pelayanan terbaik kepada masyarakat luas.',
        },
        {
            'nomor': '06',
            'kategori': 'Kehidupan Berbangsa & Bernegara',
            'poin': 'Darul \'Ahdi Wasy-Syahadah',
            'deskripsi': 'Memandang NKRI sebagai konsensus nasional (Darul \'Ahdi) dan gelanggang pembuktian pengabdian (Darul Syahadah). Menolak korupsi, taat hukum yang adil, dan berkontribusi nyata bagi kemajuan bangsa.',
        },
    ],
}

DOKUMEN_DASAR_MUHAMMADIYAH = [
    {
        'singkatan': 'MADM',
        'nama': 'Muqaddimah Anggaran Dasar Muhammadiyah',
        'tahun': '1945 – 1950 M',
        'tokoh': 'Ki Bagus Hadikusumo bersama tokoh pimpinan lainnya',
        'inti_pokok': 'Memuat 7 pokok pikiran fundamental yang menjadi landasan filosofis persyarikatan, menegaskan tauhid sebagai asas hidup manusia, urgensi hidup bermasyarakat, syariat Islam sebagai satu-satunya hukum kebenaran, perlunya organisasi sebagai wasilah dakwah, dan cita-cita mewujudkan masyarakat Islam yang sebenar-benarnya.',
        'tag': 'Ruh Ideologi & Asas Persyarikatan',
        'warna': 'brand',
    },
    {
        'singkatan': 'Kepribadian',
        'nama': 'Kepribadian Muhammadiyah',
        'tahun': 'Muktamar ke-35 Jakarta (1962 M)',
        'tokoh': 'K.H. Faqih Usman dkk.',
        'inti_pokok': 'Merumuskan jati diri hakiki persyarikatan dan pedoman sikap gerak warga. Menegaskan 10 sifat utama Muhammadiyah: beramal dan berjuang untuk perdamaian dan kesejahteraan, memperbanyak kawan, lapang dada, mengindahkan hukum negara, amar ma\'ruf nahi munkar, serta aktif bekerjasama dengan golongan Islam manapun.',
        'tag': 'Jati Diri & Kharakter Gerak',
        'warna': 'emerald',
    },
    {
        'singkatan': 'MKCHM',
        'nama': 'Matan Keyakinan dan Cita-cita Hidup Muhammadiyah',
        'tahun': 'Tanwir Ponorogo (1969 M)',
        'tokoh': 'Pimpinan Pusat Muhammadiyah',
        'inti_pokok': 'Sistematisasi ideologi persyarikatan yang memuat konsepsi aqidah murni, pandangan komprehensif tentang ajaran Islam (aqidah, ibadah, akhlak, dan muamalat dunyawiyah), fungsi Muhammadiyah di Indonesia, serta cita-cita masyarakat adil makmur yang diridhai Allah SWT berlandaskan nilai-nilai profetik.',
        'tag': 'Pedoman Sistemik Ideologi',
        'warna': 'purple',
    },
    {
        'singkatan': 'Khittah',
        'nama': 'Khittah Perjuangan Muhammadiyah',
        'tahun': 'Khittah Denpasar (2002 M), Surabaya (1978 M)',
        'tokoh': 'Muktamar & Sidang Tanwir',
        'inti_pokok': 'Pedoman garis kebijakan dakwah dan panduan posisi strategis Muhammadiyah dalam merespons dinamika kehidupan sosial-politik. Menegaskan bahwa Muhammadiyah tidak berafiliasi dan tidak terikat dengan partai politik manapun, serta menjalankan politik keadaban (high politics) berbasis moralitas kebangsaan.',
        'tag': 'Garis Kebijakan Dakwah & Politik',
        'warna': 'blue',
    },
]


def profil_view(request):
    profil = ProfilOrganisasi.objects.first()
    misi_list = profil.get_misi_list() if profil else []

    context = {
        'profil': profil,
        'misi_list': misi_list,
        'tujuan_muhammadiyah': TUJUAN_BERDIRI_MUHAMMADIYAH,
        'phiwm': PHIWM_DATA,
        'dokumen_dasar_list': DOKUMEN_DASAR_MUHAMMADIYAH,
    }
    return render(request, 'pcm/profil.html', context)


def pimpinan_view(request):
    pimpinan_list = Pimpinan.objects.all().order_by('urutan', 'id')
    penasehat_list = [p for p in pimpinan_list if 'penasehat' in p.jabatan.lower()]
    pleno_list = [p for p in pimpinan_list if 'penasehat' not in p.jabatan.lower()]

    context = {
        'pimpinan_list': pimpinan_list,
        'penasehat_list': penasehat_list,
        'pleno_list': pleno_list,
        'majelis_lembaga_list': MAJELIS_LEMBAGA_LIST,
        'total_majelis_lembaga': len(MAJELIS_LEMBAGA_LIST),
    }
    return render(request, 'pcm/pimpinan.html', context)


RANTING_DETAILS = {
    'Dawungan': {
        'nama_desa': 'Desa Dawungan',
        'julukan': 'Lumbung Pangan & Pertanian Berkah',
        'masjid_utama': 'Masjid Al-Hidayah Dawungan',
        'alamat_masjid': 'Dukuh Dawungan RT 02, Desa Dawungan, Kec. Masaran',
        'profil_desa': 'Desa agraris produktif di kawasan timur Masaran dengan hamparan persawahan subur. Jamaah Muhammadiyah memelopori gerakan Lumbung Zakat Pertanian melalui Lazismu dan pengajian akbar keliling antar-dukuh.',
        'program_unggulan': 'Lumbung Zakat Pertanian, Pengajian Malam Jumat, & TPA Mandiri',
        'jumlah_masjid': 6,
        'jumlah_jamaah': '850+ Jamaah',
        'tag_kategori': 'Pertanian & Filantropi',
        'badge_color': 'emerald',
        'gambar': 'https://images.unsplash.com/photo-1590076215667-875d4ef2d7ee?auto=format&fit=crop&w=800&q=80',
    },
    'Gebang': {
        'nama_desa': 'Desa Gebang',
        'julukan': 'Kaderisasi Pemuda & Dakwah Komunitas',
        'masjid_utama': 'Masjid Darussalam Gebang',
        'alamat_masjid': 'Dukuh Gebang RT 05, Desa Gebang, Kec. Masaran',
        'profil_desa': 'Desa yang berbatasan langsung dengan poros Sragen-Karanganyar. Memiliki basis angkatan muda persyarikatan (Pemuda Muhammadiyah & Nasyiatul Aisyiyah) yang progresif dalam kegiatan tabligh dan pemberdayaan santri usia produktif.',
        'program_unggulan': 'Kajian Tematik Pemuda, Majelis Taklim Ibu-Ibu, & Posdaya',
        'jumlah_masjid': 5,
        'jumlah_jamaah': '720+ Jamaah',
        'tag_kategori': 'Kepemudaan & Dakwah',
        'badge_color': 'blue',
        'gambar': 'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=800&q=80',
    },
    'Jati': {
        'nama_desa': 'Desa Jati',
        'julukan': 'Sentra Gotong Royong & Pengajian Subuh',
        'masjid_utama': 'Masjid At-Taqwa Jati',
        'alamat_masjid': 'Dukuh Jati RT 01, Desa Jati, Kec. Masaran',
        'profil_desa': 'Kawasan pedesaan guyub dengan tradisi kebersamaan warga persyarikatan yang kokoh. Terkenal dengan gerakan Subuh Berjamaah rutin dan santunan infak sedekah untuk warga jompo dan duafa.',
        'program_unggulan': 'Gerakan Subuh Berkah, Santunan Sembako Duafa, & TPA Al-Qur\'an',
        'jumlah_masjid': 7,
        'jumlah_jamaah': '900+ Jamaah',
        'tag_kategori': 'Gerakan Sosial & Subuh',
        'badge_color': 'amber',
        'gambar': 'https://images.unsplash.com/photo-1564769625905-50e93615e769?auto=format&fit=crop&w=800&q=80',
    },
    'Jirapan': {
        'nama_desa': 'Desa Jirapan',
        'julukan': 'Pusat Pesantren & Kader Ulama Muhammadiyah',
        'masjid_utama': 'Masjid Besar Al-Manar Jirapan',
        'alamat_masjid': 'Kompleks Pondok Pesantren Al-Manar, Desa Jirapan, Kec. Masaran',
        'profil_desa': 'Kawasan pendidikan Islam percontohan di Sragen. Menjadi rumah bagi Pondok Pesantren Muhammadiyah Al-Manar yang mencetak ratusan santri penghafal Al-Qur\'an dan kader mubaligh muda siap terjun ke masyarakat.',
        'program_unggulan': 'Pondok Pesantren Tahfidz, Tabligh Akbar Selapanan, & Kursus Bahasa Arab',
        'jumlah_masjid': 9,
        'jumlah_jamaah': '1.400+ Santri & Warga',
        'tag_kategori': 'Pendidikan Pesantren & Ulama',
        'badge_color': 'purple',
        'gambar': 'https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?auto=format&fit=crop&w=800&q=80',
    },
    'Karangmalang': {
        'nama_desa': 'Desa Karangmalang',
        'julukan': 'Layanan Kesehatan Jamaah & Bina Keluarga Sakinah',
        'masjid_utama': 'Masjid Al-Barokah Karangmalang',
        'alamat_masjid': 'Dukuh Karangmalang RT 03, Desa Karangmalang, Kec. Masaran',
        'profil_desa': 'Desa dengan kegiatan Aisyiyah yang sangat dinamis, membina pos kesehatan terpadu dan pembinaan keluarga sakinah. Jamaah aktif mengelola kas sosial masjid untuk biaya pengobatan warga kurang mampu.',
        'program_unggulan': 'Posyandu Lansia Aisyiyah, Kas Peduli Kesehatan, & Bimbingan Pra-Nikah',
        'jumlah_masjid': 5,
        'jumlah_jamaah': '680+ Jamaah',
        'tag_kategori': 'Kesehatan & Keluarga Sakinah',
        'badge_color': 'teal',
        'gambar': 'https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?auto=format&fit=crop&w=800&q=80',
    },
    'Kliwonan': {
        'nama_desa': 'Desa Wisata Batik Kliwonan',
        'julukan': 'Desa Wisata Batik & Etos Saudagar Muslim',
        'masjid_utama': 'Masjid Al-Muttaqin Kliwonan',
        'alamat_masjid': 'Jl. Sentra Batik Kliwonan RT 08, Desa Kliwonan, Kec. Masaran',
        'profil_desa': 'Sentra industri kreatif batik Sragen yang mendunia. Warga persyarikatan di Kliwonan memadukan etos kerja saudagar Muslim KH Ahmad Dahlan dengan kedermawanan waqaf dan pembinaan tenaga kerja konveksi ramah syariah.',
        'program_unggulan': 'Majelis Taklim Saudagar Batik, Waqaf Usaha Produktif, & TPA Anak Pengrajin',
        'jumlah_masjid': 8,
        'jumlah_jamaah': '1.250+ Jamaah',
        'tag_kategori': 'Wisata Batik & Ekonomi Syariah',
        'badge_color': 'indigo',
        'gambar': 'https://images.unsplash.com/photo-1519817650390-64a93db51149?auto=format&fit=crop&w=800&q=80',
    },
    'Krebet': {
        'nama_desa': 'Desa Krebet',
        'julukan': 'Markas Pandu Hizbul Wathan & Bela Diri Tapak Suci',
        'masjid_utama': 'Masjid Mujahidin Krebet',
        'alamat_masjid': 'Kompleks Masjid Mujahidin, Desa Krebet, Kec. Masaran',
        'profil_desa': 'Basis pergerakan fisik dan mental kader persyarikatan. Menjadi episentrum latihan kepanduan Hizbul Wathan (HW) dan seni bela diri Tapak Suci Putera Muhammadiyah Cabang Masaran.',
        'program_unggulan': 'Latihan Rutin Tapak Suci, Diklat Pandu HW, & Gerakan Masjid Makmur',
        'jumlah_masjid': 6,
        'jumlah_jamaah': '820+ Jamaah',
        'tag_kategori': 'Kepanduan & Bela Diri',
        'badge_color': 'rose',
        'gambar': 'https://images.unsplash.com/photo-1579783902614-a3fb3927b675?auto=format&fit=crop&w=800&q=80',
    },
    'Krikilan': {
        'nama_desa': 'Desa Krikilan',
        'julukan': 'Penguatan Akidah & Pembinaan Muallaf',
        'masjid_utama': 'Masjid Baitul Izzah Krikilan',
        'alamat_masjid': 'Dukuh Krikilan RT 06, Desa Krikilan, Kec. Masaran',
        'profil_desa': 'Desa dengan keragaman latar belakang masyarakat. Muhammadiyah Ranting Krikilan memfokuskan dakwah pada bimbingan akidah murni, pengajian tafsir hadits, dan pendampingan muallaf desa.',
        'program_unggulan': 'Kajian Ushul Tsalatsah, Bimbingan Ibadah Praktis, & Santunan Muallaf',
        'jumlah_masjid': 5,
        'jumlah_jamaah': '640+ Jamaah',
        'tag_kategori': 'Pembinaan Akidah & Muallaf',
        'badge_color': 'sky',
        'gambar': 'https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?auto=format&fit=crop&w=800&q=80',
    },
    'Masaran': {
        'nama_desa': 'Desa Masaran (Pusat Kecamatan)',
        'julukan': 'Episentrum Dakwah & Masjid Besar Baiturrahman',
        'masjid_utama': 'Masjid Besar Baiturrahman Masaran',
        'alamat_masjid': 'Jl. Raya Solo-Sragen KM 12, Desa Masaran, Kec. Masaran',
        'profil_desa': 'Pusat peradaban dan koordinasi dakwah Muhammadiyah se-Kecamatan Masaran. Kompleks Masjid Besar Baiturrahman menaungi pusat kegiatan tabligh akbar akbar, perayaan Idul Fitri/Adha kecamatan, dan kantor layanan Lazismu.',
        'program_unggulan': 'Kajian Akbar Ahad Pagi, Layanan Ambulans Gratis 24 Jam, & Baitul Mal',
        'jumlah_masjid': 12,
        'jumlah_jamaah': '2.100+ Jamaah',
        'tag_kategori': 'Pusat Cabang & Masjid Besar',
        'badge_color': 'emerald',
        'gambar': 'https://images.unsplash.com/photo-1564769625905-50e93615e769?auto=format&fit=crop&w=800&q=80',
    },
    'Pilang': {
        'nama_desa': 'Desa Sentra Batik Pilang',
        'julukan': 'Klaster Pengrajin Batik Tulis & Filantropi Wakaf',
        'masjid_utama': 'Masjid Al-Ikhlas Pilang',
        'alamat_masjid': 'Dukuh Pilang RT 04, Desa Pilang, Kec. Masaran',
        'profil_desa': 'Pusat legendaris seni batik Sragen dengan ratusan perajin mandiri. PCM dan PRM Pilang mengelola waqaf tanah dan bangunan untuk mendukung sarana ibadah dan beasiswa santri berprestasi.',
        'program_unggulan': 'Beasiswa Anak Pengrajin Batik, Tabungan Kurban Berjamaah, & Remaja Masjid',
        'jumlah_masjid': 8,
        'jumlah_jamaah': '1.100+ Jamaah',
        'tag_kategori': 'Warisan Budaya & Filantropi',
        'badge_color': 'amber',
        'gambar': 'https://images.unsplash.com/photo-1590076215667-875d4ef2d7ee?auto=format&fit=crop&w=800&q=80',
    },
    'Pringanom': {
        'nama_desa': 'Desa Pringanom',
        'julukan': 'Gerakan Filantropi Jimpitan Beras & Dakwah Akar Rumput',
        'masjid_utama': 'Masjid Nurul Huda Pringanom',
        'alamat_masjid': 'Dukuh Pringanom RT 02, Desa Pringanom, Kec. Masaran',
        'profil_desa': 'Kawasan agraris yang terkenal dengan inovasi Gerakan Sedekah Beras Jimpitan binaan Aisyiyah. Setiap panen, jamaah menyisihkan beras untuk disalurkan ke dapur santri dan janda tua dhuafa.',
        'program_unggulan': 'Sedekah Beras Jimpitan, Pengajian Kuliah Subuh, & TPA Balita',
        'jumlah_masjid': 6,
        'jumlah_jamaah': '790+ Jamaah',
        'tag_kategori': 'Ketahanan Pangan & Sosial',
        'badge_color': 'green',
        'gambar': 'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=800&q=80',
    },
    'Sepat': {
        'nama_desa': 'Desa Sepat',
        'julukan': 'Gerakan Masjid Bersih & Pelayanan Jenazah Syar\'i',
        'masjid_utama': 'Musholla & Masjid Al-Huda Sepat',
        'alamat_masjid': 'Kompleks Masjid Al-Huda, Desa Sepat, Kec. Masaran',
        'profil_desa': 'Desa dengan kultur kebersihan dan kekeluargaan yang tinggi. Korps Pemuda Ranting rutin menggelar bakti resik masjid serentak dan pelatihan pemulasaraan jenazah sesuai sunnah Rasulullah SAW.',
        'program_unggulan': 'Bakti Resik Masjid Serentak, Pelatihan Tajhiz Jenazah, & TPA Al-Kautsar',
        'jumlah_masjid': 5,
        'jumlah_jamaah': '670+ Jamaah',
        'tag_kategori': 'Tajhiz Jenazah & Kebersihan',
        'badge_color': 'cyan',
        'gambar': 'https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?auto=format&fit=crop&w=800&q=80',
    },
    'Sidodadi': {
        'nama_desa': 'Desa Sidodadi',
        'julukan': 'Pusat Pendidikan Dasar Madrasah Ibtidaiyah',
        'masjid_utama': 'Masjid Baitussalam Sidodadi',
        'alamat_masjid': 'Kompleks MIM Sidodadi, Desa Sidodadi, Kec. Masaran',
        'profil_desa': 'Basis pembinaan generasi penerus persyarikatan sejak dini. Keberadaan Madrasah Ibtidaiyah Muhammadiyah (MIM) Sidodadi menjadi katalisator pengajian wali murid dan gerakan cinta Al-Qur\'an.',
        'program_unggulan': 'Bina Madrasah MIM Unggulan, Tahfidz Juz Amma Anak, & Pengajian Parenting',
        'jumlah_masjid': 6,
        'jumlah_jamaah': '860+ Jamaah & Siswa',
        'tag_kategori': 'Pendidikan Madrasah & TPA',
        'badge_color': 'orange',
        'gambar': 'https://images.unsplash.com/photo-1519817650390-64a93db51149?auto=format&fit=crop&w=800&q=80',
    },
}


def ranting_view(request):
    ranting_qs = list(Ranting.objects.all().order_by('nama_ranting'))
    total_masjid_count = 0
    for r in ranting_qs:
        meta = RANTING_DETAILS.get(r.nama_ranting, {})
        r.nama_desa = meta.get('nama_desa', f'Desa {r.nama_ranting}')
        r.julukan = meta.get('julukan', 'Basis Jamaah Persyarikatan')
        r.masjid_utama = meta.get('masjid_utama', f'Masjid {r.nama_ranting}')
        r.alamat_masjid = meta.get('alamat_masjid', r.alamat)
        r.profil_desa = meta.get('profil_desa', 'Pimpinan Ranting Muhammadiyah aktif membina jamaah pengajian, mengelola masjid dan mushalla, serta menggerakkan dakwah sosial.')
        r.program_unggulan = meta.get('program_unggulan', 'Pengajian Rutin & TPA')
        r.jumlah_masjid = meta.get('jumlah_masjid', 5)
        r.jumlah_jamaah = meta.get('jumlah_jamaah', '600+ Jamaah')
        r.tag_kategori = meta.get('tag_kategori', 'Dakwah & Ibadah')
        r.badge_color = meta.get('badge_color', 'emerald')
        r.gambar = meta.get('gambar', 'https://images.unsplash.com/photo-1564769625905-50e93615e769?auto=format&fit=crop&w=800&q=80')
        total_masjid_count += r.jumlah_masjid

    context = {
        'ranting_list': ranting_qs,
        'total_ranting': len(ranting_qs),
        'total_masjid': total_masjid_count if total_masjid_count > 0 else 88,
    }
    return render(request, 'pcm/ranting.html', context)


def amal_usaha_view(request):
    amal_usaha_list = AmalUsaha.objects.all().order_by('nama')
    
    aum_pendidikan = amal_usaha_list.filter(bidang='pendidikan')
    aum_kesehatan = amal_usaha_list.filter(bidang='kesehatan')
    aum_sosial = amal_usaha_list.filter(bidang='sosial')
    aum_ekonomi = amal_usaha_list.filter(bidang='ekonomi')

    context = {
        'amal_usaha_list': amal_usaha_list,
        'aum_pendidikan': aum_pendidikan,
        'aum_kesehatan': aum_kesehatan,
        'aum_sosial': aum_sosial,
        'aum_ekonomi': aum_ekonomi,
        'total_aum': amal_usaha_list.count(),
    }
    return render(request, 'pcm/amal_usaha.html', context)


def berita_list_view(request):
    query = request.GET.get('q', '').strip()
    berita_qs = Berita.objects.published()

    if query:
        berita_qs = berita_qs.filter(
            Q(judul__icontains=query) |
            Q(ringkasan__icontains=query) |
            Q(isi__icontains=query)
        )

    query_count = berita_qs.count() if query else None

    paginator = Paginator(berita_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'query_count': query_count,
    }
    return render(request, 'pcm/berita_list.html', context)


def berita_detail_view(request, slug):
    berita = get_object_or_404(Berita.objects.published(), slug=slug)
    words = [w for w in berita.judul.split() if len(w) > 3][:3]
    related_qs = Berita.objects.published().exclude(pk=berita.pk)
    if words:
        title_q = Q()
        for w in words:
            title_q |= Q(judul__icontains=w) | Q(ringkasan__icontains=w)
        matched = list(related_qs.filter(title_q).order_by('-tanggal_terbit')[:3])
        if len(matched) < 3:
            existing_ids = [m.pk for m in matched] + [berita.pk]
            fallback = list(Berita.objects.published().exclude(pk__in=existing_ids).order_by('-tanggal_terbit')[:(3 - len(matched))])
            berita_terkait = matched + fallback
        else:
            berita_terkait = matched
    else:
        berita_terkait = list(related_qs.order_by('-tanggal_terbit')[:3])

    context = {
        'berita': berita,
        'berita_terkait': berita_terkait,
    }
    return render(request, 'pcm/berita_detail.html', context)


def agenda_view(request):
    now = timezone.now()
    query = request.GET.get('q', '').strip()
    agenda_akan_datang = Agenda.objects.filter(waktu_mulai__gte=now).order_by('waktu_mulai')
    agenda_terlaksana = Agenda.objects.filter(waktu_mulai__lt=now).order_by('-waktu_mulai')

    if query:
        agenda_akan_datang = agenda_akan_datang.filter(
            Q(nama_kegiatan__icontains=query) | Q(tempat__icontains=query) | Q(keterangan__icontains=query)
        )
        agenda_terlaksana = agenda_terlaksana.filter(
            Q(nama_kegiatan__icontains=query) | Q(tempat__icontains=query) | Q(keterangan__icontains=query)
        )

    context = {
        'agenda_akan_datang': agenda_akan_datang,
        'agenda_terlaksana': agenda_terlaksana,
        'query': query,
    }
    return render(request, 'pcm/agenda.html', context)


def agenda_ics_view(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    dt_str = agenda.waktu_mulai.strftime('%Y%m%dT%H%M%SZ')
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//PCM Masaran//Agenda//ID",
        "BEGIN:VEVENT",
        f"SUMMARY:{agenda.nama_kegiatan}",
        f"LOCATION:{agenda.tempat}",
        f"DESCRIPTION:{agenda.keterangan}",
        f"DTSTART:{dt_str}",
        f"DTEND:{dt_str}",
        "END:VEVENT",
        "END:VCALENDAR",
    ]
    response = HttpResponse("\r\n".join(lines), content_type="text/calendar; charset=utf-8")
    response['Content-Disposition'] = f'attachment; filename="agenda-{agenda.pk}.ics"'
    return response


def unduhan_view(request):
    query = request.GET.get('q', '').strip()
    dokumen_list = Dokumen.objects.all().order_by('-tanggal_unggah')
    if query:
        dokumen_list = dokumen_list.filter(
            Q(judul__icontains=query) | Q(keterangan__icontains=query)
        )
    context = {
        'dokumen_list': dokumen_list,
        'query': query,
    }
    return render(request, 'pcm/unduhan.html', context)


def kontak_view(request):
    if request.method == 'POST':
        form = KontakForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Terima kasih! Pesan dan aspirasi Anda telah berhasil dikirimkan ke sekretariat PCM Masaran."
            )
            return redirect('pcm:kontak')
        else:
            messages.error(
                request,
                "Mohon periksa kembali formulir Anda. Pastikan semua field terisi dengan benar."
            )
    else:
        form = KontakForm()

    context = {
        'form': form,
    }
    return render(request, 'pcm/kontak.html', context)


def api_health_check_view(request):
    db_status = "ok"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as e:
        db_status = str(e)
    return JsonResponse({
        "status": "healthy" if db_status == "ok" else "unhealthy",
        "database": db_status,
        "timestamp": timezone.now().isoformat(),
        "service": "website-pcm-masaran",
        "version": "1.0.0"
    })


def sitemap_xml_view(request):
    base_url = request.build_absolute_uri('/')[:-1]
    static_routes = [
        '',
        '/profil/',
        '/pimpinan/',
        '/ranting/',
        '/amal-usaha/',
        '/berita/',
        '/agenda/',
        '/unduhan/',
        '/kontak/',
    ]
    xml_items = []
    for route in static_routes:
        xml_items.append(
            f"<url><loc>{base_url}{route}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>"
        )
    for b in Berita.objects.published():
        url = request.build_absolute_uri(b.get_absolute_url())
        lastmod = b.tanggal_terbit.strftime('%Y-%m-%d')
        xml_items.append(
            f"<url><loc>{url}</loc><lastmod>{lastmod}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>"
        )
    content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(xml_items) + "\n</urlset>"
    return HttpResponse(content, content_type='application/xml')


def robots_txt_view(request):
    sitemap_url = request.build_absolute_uri(reverse('pcm:sitemap_xml'))
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "",
        f"Sitemap: {sitemap_url}"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def api_statistik_view(request):
    profil = ProfilOrganisasi.objects.first()
    bidang_filter = request.GET.get('bidang', '').strip().lower()
    aum_counts = {}
    for code, _ in AmalUsaha.BIDANG_CHOICES:
        if not bidang_filter or bidang_filter == code:
            aum_counts[code] = AmalUsaha.objects.filter(bidang=code).count()
    return JsonResponse({
        "ranting_count": Ranting.objects.count(),
        "amal_usaha_count": sum(aum_counts.values()) if bidang_filter else AmalUsaha.objects.count(),
        "amal_usaha_per_bidang": aum_counts,
        "berita_count": Berita.objects.published().count(),
        "agenda_mendatang_count": Agenda.objects.filter(waktu_mulai__gte=timezone.now()).count(),
        "dokumen_count": Dokumen.objects.count(),
        "anggota_ktam": profil.jumlah_anggota_ktam if profil else 0,
        "filter_bidang": bidang_filter or None,
    })


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500_view(request):
    return render(request, '500.html', status=500)
