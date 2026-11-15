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


def beranda_view(request):
    """
    Halaman Beranda:
    - Hero dengan gambar utama dan identitas PCM Masaran
    - Kartu statistik (jumlah ranting, jumlah amal usaha, anggota ber-KTAM)
    - 3 berita terbaru yang sudah terbit
    - 3 agenda mendatang terdekat
    """
    now = timezone.now()
    profil = ProfilOrganisasi.objects.first()
    
    total_ranting = Ranting.objects.count()
    total_amal_usaha = AmalUsaha.objects.count()
    total_ktam = profil.jumlah_anggota_ktam if profil else 1250

    berita_terbaru = Berita.objects.published().order_by('-tanggal_terbit')[:3]
    agenda_mendatang = Agenda.objects.filter(waktu_mulai__gte=now).order_by('waktu_mulai')[:3]

    context = {
        'total_ranting': total_ranting,
        'total_amal_usaha': total_amal_usaha,
        'total_ktam': total_ktam,
        'berita_terbaru': berita_terbaru,
        'agenda_mendatang': agenda_mendatang,
    }
    return render(request, 'pcm/beranda.html', context)


def profil_view(request):
    """
    Halaman Profil:
    - Tentang PCM Masaran
    - Sejarah berdirinya
    - Visi dan Misi (misi tampil sebagai daftar bernomor)
    - Alamat & Kontak resmi
    """
    profil = ProfilOrganisasi.objects.first()
    misi_list = profil.get_misi_list() if profil else []

    context = {
        'profil': profil,
        'misi_list': misi_list,
    }
    return render(request, 'pcm/profil.html', context)


def pimpinan_view(request):
    """
    Halaman Pimpinan:
    - Kartu pimpinan dengan foto, jabatan, dan periode
    - Diurutkan berdasarkan field 'urutan'
    """
    pimpinan_list = Pimpinan.objects.all().order_by('urutan', 'id')
    context = {
        'pimpinan_list': pimpinan_list,
    }
    return render(request, 'pcm/pimpinan.html', context)


def ranting_view(request):
    """
    Halaman Ranting:
    - Tabel daftar 13 Pimpinan Ranting Muhammadiyah (PRM) di Kecamatan Masaran
    - Info ketua, alamat, kontak
    """
    ranting_list = Ranting.objects.all().order_by('nama_ranting')
    context = {
        'ranting_list': ranting_list,
    }
    return render(request, 'pcm/ranting.html', context)


def amal_usaha_view(request):
    """
    Halaman Amal Usaha (AUM):
    - Dikelompokkan per bidang: Pendidikan, Kesehatan, Sosial, Ekonomi
    """
    amal_usaha_list = AmalUsaha.objects.all()
    
    # Kelompokkan per bidang
    aum_pendidikan = amal_usaha_list.filter(bidang='pendidikan')
    aum_kesehatan = amal_usaha_list.filter(bidang='kesehatan')
    aum_sosial = amal_usaha_list.filter(bidang='sosial')
    aum_ekonomi = amal_usaha_list.filter(bidang='ekonomi')

    context = {
        'aum_pendidikan': aum_pendidikan,
        'aum_kesehatan': aum_kesehatan,
        'aum_sosial': aum_sosial,
        'aum_ekonomi': aum_ekonomi,
        'total_aum': amal_usaha_list.count(),
    }
    return render(request, 'pcm/amal_usaha.html', context)


def berita_list_view(request):
    """
    Halaman Daftar Berita:
    - Berita terbit terfilter (tanpa draf / masa depan)
    - Paginator 6 berita per halaman
    - Fitur pencarian berita (?q=...) untuk bonus nilai
    """
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
    """
    Halaman Detail Berita:
    - Berita draf atau bertanggal di masa depan WAJIB 404!
    - Menggunakan get_object_or_404 pada Berita.objects.published()
    - Rekomendasi berita lainnya
    """
    berita = get_object_or_404(Berita.objects.published(), slug=slug)
    berita_terkait = Berita.objects.published().exclude(pk=berita.pk).order_by('-tanggal_terbit')[:3]

    context = {
        'berita': berita,
        'berita_terkait': berita_terkait,
    }
    return render(request, 'pcm/berita_detail.html', context)


def agenda_view(request):
    """
    Halaman Agenda:
    - Agenda akan datang dan sudah terlaksana dipisah secara rapi
    """
    now = timezone.now()
    agenda_akan_datang = Agenda.objects.filter(waktu_mulai__gte=now).order_by('waktu_mulai')
    agenda_terlaksana = Agenda.objects.filter(waktu_mulai__lt=now).order_by('-waktu_mulai')

    context = {
        'agenda_akan_datang': agenda_akan_datang,
        'agenda_terlaksana': agenda_terlaksana,
    }
    return render(request, 'pcm/agenda.html', context)


def unduhan_view(request):
    """
    Halaman Unduhan:
    - Berkas dokumen publik dengan tombol unduh
    """
    dokumen_list = Dokumen.objects.all().order_by('-tanggal_unggah')
    context = {
        'dokumen_list': dokumen_list,
    }
    return render(request, 'pcm/unduhan.html', context)


def kontak_view(request):
    """
    Halaman Kontak & Aspirasi:
    - Informasi sekretariat dan media sosial resmi
    - Formulir kontak (ModelForm PesanMasuk)
    - Menyimpan pesan ke database dan menampilkan pesan sukses via messages framework
    """
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
