from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
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


def profil_view(request):
    profil = ProfilOrganisasi.objects.first()
    misi_list = profil.get_misi_list() if profil else []

    context = {
        'profil': profil,
        'misi_list': misi_list,
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


def ranting_view(request):
    ranting_list = Ranting.objects.all().order_by('nama_ranting')
    context = {
        'ranting_list': ranting_list,
        'total_ranting': ranting_list.count(),
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

    paginator = Paginator(berita_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'pcm/berita_list.html', context)


def berita_detail_view(request, slug):
    berita = get_object_or_404(Berita.objects.published(), slug=slug)
    berita_terkait = Berita.objects.published().exclude(pk=berita.pk).order_by('-tanggal_terbit')[:3]

    context = {
        'berita': berita,
        'berita_terkait': berita_terkait,
    }
    return render(request, 'pcm/berita_detail.html', context)


def agenda_view(request):
    now = timezone.now()
    agenda_akan_datang = Agenda.objects.filter(waktu_mulai__gte=now).order_by('waktu_mulai')
    agenda_terlaksana = Agenda.objects.filter(waktu_mulai__lt=now).order_by('-waktu_mulai')

    context = {
        'agenda_akan_datang': agenda_akan_datang,
        'agenda_terlaksana': agenda_terlaksana,
    }
    return render(request, 'pcm/agenda.html', context)


def unduhan_view(request):
    dokumen_list = Dokumen.objects.all().order_by('-tanggal_unggah')
    context = {
        'dokumen_list': dokumen_list,
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
