from .models import ProfilOrganisasi, TautanTerkait


def pcm_global_context(request):
    """
    Context processor global untuk menyediakan:
    1. profil_organisasi (Profil PCM Masaran)
    2. tautan_terkait (Tautan Persyarikatan di footer)
    3. medsos_links (Akun resmi media sosial PCM Masaran)
    ke semua template tanpa perlu query manual di setiap view.
    """
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

    return {
        'profil_organisasi': profil,
        'tautan_terkait': tautan,
        'medsos_links': medsos,
    }
