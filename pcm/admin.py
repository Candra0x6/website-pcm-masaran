from django.contrib import admin
from django.utils.html import format_html
from .models import (
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

admin.site.site_header = "Admin Website PCM Masaran"
admin.site.site_title = "Portal Admin PCM Masaran"
admin.site.index_title = "Manajemen Konten & Organisasi PCM Masaran"


@admin.register(ProfilOrganisasi)
class ProfilOrganisasiAdmin(admin.ModelAdmin):
    list_display = ('nama_singkat', 'telepon', 'email', 'jumlah_anggota_ktam', 'preview_hero')
    fieldsets = (
        ("Identitas Utama", {
            'fields': ('nama', 'nama_singkat', 'tagline', 'gambar_utama')
        }),
        ("Tentang & Sejarah", {
            'fields': ('tentang', 'sejarah')
        }),
        ("Visi & Misi", {
            'fields': ('visi', 'misi')
        }),
        ("Kontak & Statistik", {
            'fields': ('alamat_sekretariat', 'telepon', 'email', 'jumlah_anggota_ktam')
        }),
    )

    def preview_hero(self, obj):
        if obj.gambar_utama:
            return format_html('<img src="{}" style="height: 40px; border-radius: 6px; object-fit: cover;" />', obj.gambar_utama.url)
        return "-"
    preview_hero.short_description = "Hero"

    def has_add_permission(self, request):
        if ProfilOrganisasi.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Pimpinan)
class PimpinanAdmin(admin.ModelAdmin):
    list_display = ('urutan', 'nama', 'jabatan', 'periode', 'preview_foto')
    list_display_links = ('nama',)
    list_editable = ('urutan',)
    search_fields = ('nama', 'jabatan')
    list_filter = ('periode',)
    ordering = ('urutan', 'id')

    def preview_foto(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="height: 40px; width: 40px; border-radius: 50%; object-fit: cover;" />', obj.foto.url)
        return "-"
    preview_foto.short_description = "Foto"


@admin.register(Ranting)
class RantingAdmin(admin.ModelAdmin):
    list_display = ('nama_ranting', 'ketua', 'telepon', 'alamat')
    search_fields = ('nama_ranting', 'ketua', 'alamat')
    ordering = ('nama_ranting',)


@admin.register(AmalUsaha)
class AmalUsahaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'bidang', 'alamat', 'preview_gambar')
    list_filter = ('bidang',)
    search_fields = ('nama', 'deskripsi', 'alamat')
    ordering = ('bidang', 'nama')

    def preview_gambar(self, obj):
        if obj.gambar:
            return format_html('<img src="{}" style="height: 40px; width: 60px; border-radius: 6px; object-fit: cover;" />', obj.gambar.url)
        return "-"
    preview_gambar.short_description = "Gambar"


@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'status_terbit', 'tanggal_terbit', 'preview_sampul')
    list_filter = ('status_terbit', 'tanggal_terbit')
    search_fields = ('judul', 'ringkasan', 'isi')
    prepopulated_fields = {'slug': ('judul',)}
    date_hierarchy = 'tanggal_terbit'
    ordering = ('-tanggal_terbit',)

    def preview_sampul(self, obj):
        if obj.gambar_sampul:
            return format_html('<img src="{}" style="height: 40px; width: 60px; border-radius: 6px; object-fit: cover;" />', obj.gambar_sampul.url)
        return "-"
    preview_sampul.short_description = "Sampul"


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('nama_kegiatan', 'waktu_mulai', 'tempat', 'status_agenda')
    list_filter = ('waktu_mulai',)
    search_fields = ('nama_kegiatan', 'tempat', 'keterangan')
    ordering = ('-waktu_mulai',)

    def status_agenda(self, obj):
        if obj.is_upcoming:
            return format_html('<span style="color: #059669; font-weight: bold;">Akan Datang</span>')
        return format_html('<span style="color: #6b7280;">Selesai</span>')
    status_agenda.short_description = "Status"


@admin.register(Dokumen)
class DokumenAdmin(admin.ModelAdmin):
    list_display = ('judul', 'tanggal_unggah', 'berkas')
    search_fields = ('judul', 'keterangan')
    ordering = ('-tanggal_unggah',)


@admin.register(PesanMasuk)
class PesanMasukAdmin(admin.ModelAdmin):
    list_display = ('waktu_kirim', 'nama', 'email', 'subjek', 'sudah_dibaca')
    list_filter = ('sudah_dibaca', 'waktu_kirim')
    search_fields = ('nama', 'email', 'subjek', 'pesan')
    readonly_fields = ('nama', 'email', 'subjek', 'pesan', 'waktu_kirim')
    ordering = ('-waktu_kirim',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('nama', 'email', 'subjek', 'pesan', 'waktu_kirim')
        return self.readonly_fields


@admin.register(TautanTerkait)
class TautanTerkaitAdmin(admin.ModelAdmin):
    list_display = ('urutan', 'nama', 'url')
    list_display_links = ('nama',)
    list_editable = ('urutan',)
    search_fields = ('nama', 'url')
    ordering = ('urutan', 'nama')
