from .models import (
    ProfilOrganisasi,
    TautanTerkait,
    Berita,
    Agenda,
    Dokumen,
    PesanMasuk,
    Ranting,
    AmalUsaha
)


def pcm_global_context(request):
    profil = ProfilOrganisasi.objects.first()
    tautan = TautanTerkait.objects.all().order_by('urutan', 'nama')
    
    medsos = {
        'youtube': 'https://youtube.com/@muhammadiyahmasaran?si=8CD5WXhPZsoJsJdN',
        'facebook': 'https://www.facebook.com/profile.php?id=61553634994772',
        'tiktok': 'https://tiktok.com/@muhammadiyahmasar',
        'instagram': 'https://www.instagram.com/pcm.masaran?igsh=MW0ybG1tamJtbndlZQ==',
        'threads': 'https://www.threads.com/@pcm.masaran',
        'x': 'https://x.com/PcmMasaran',
        'email': 'pcm.masaran@gmail.com',
    }

    admin_stats = {
        'total_berita': Berita.objects.count(),
        'total_agenda': Agenda.objects.count(),
        'total_dokumen': Dokumen.objects.count(),
        'total_pesan': PesanMasuk.objects.count(),
        'pesan_belum_dibaca': PesanMasuk.objects.filter(sudah_dibaca=False).count(),
        'total_ranting': Ranting.objects.count(),
        'total_amal_usaha': AmalUsaha.objects.count(),
    }

    return {
        'profil_organisasi': profil,
        'tautan_terkait': tautan,
        'medsos_links': medsos,
        'admin_stats': admin_stats,
    }
