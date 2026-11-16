from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse


class ProfilOrganisasi(models.Model):
    nama = models.CharField(max_length=200, default="Pimpinan Cabang Muhammadiyah Masaran")
    nama_singkat = models.CharField(max_length=50, default="PCM Masaran")
    tagline = models.CharField(
        max_length=255,
        default="Mencerahkan Semesta, Memajukan Masaran Berkemajuan"
    )
    tentang = models.TextField(help_text="Deskripsi ringkas profil PCM Masaran")
    sejarah = models.TextField(help_text="Sejarah berdirinya dan perkembangan PCM Masaran")
    visi = models.TextField(help_text="Visi PCM Masaran")
    misi = models.TextField(help_text="Satu misi per baris (akan ditampilkan sebagai daftar bernomor)")
    alamat_sekretariat = models.TextField(help_text="Alamat lengkap gedung dakwah / sekretariat resmi")
    telepon = models.CharField(max_length=30, help_text="Nomor kontak resmi sekretariat")
    email = models.EmailField(default="pcm.masaran@gmail.com")
    jumlah_anggota_ktam = models.PositiveIntegerField(
        default=1250,
        help_text="Perkiraan jumlah anggota ber-KTAM di Cabang Masaran"
    )
    gambar_utama = models.ImageField(
        upload_to='profil/',
        help_text="Gambar utama / Hero image untuk beranda"
    )

    class Meta:
        verbose_name = "Profil Organisasi"
        verbose_name_plural = "Profil Organisasi"

    def __str__(self):
        return self.nama

    def clean(self):
        super().clean()
        if not self.pk and ProfilOrganisasi.objects.exists():
            raise ValidationError("Hanya boleh ada satu baris profil organisasi di sistem.")
        if self.telepon and len(self.telepon.strip()) < 5:
            raise ValidationError({'telepon': "Nomor telepon organisasi tidak valid."})

    def get_misi_list(self):
        if not self.misi:
            return []
        return [line.strip() for line in self.misi.splitlines() if line.strip()]


class Pimpinan(models.Model):
    nama = models.CharField(max_length=150)
    jabatan = models.CharField(max_length=150)
    periode = models.CharField(max_length=50, default="2022–2027")
    foto = models.ImageField(upload_to='pimpinan/', blank=True, null=True)
    urutan = models.PositiveIntegerField(
        default=0,
        help_text="Urutan tampil kartu pimpinan (angka terkecil tampil lebih dulu)"
    )

    class Meta:
        verbose_name = "Pimpinan"
        verbose_name_plural = "Pimpinan"
        ordering = ['urutan', 'id']

    def __str__(self):
        return f"{self.nama} - {self.jabatan}"


class Ranting(models.Model):
    nama_ranting = models.CharField(max_length=150)
    ketua = models.CharField(max_length=150)
    alamat = models.TextField()
    telepon = models.CharField(
        max_length=30,
        blank=True,
        help_text="Opsional, hanya kontak resmi kantor/masjid ranting"
    )

    class Meta:
        verbose_name = "Ranting"
        verbose_name_plural = "Ranting"
        ordering = ['nama_ranting']

    def __str__(self):
        return self.nama_ranting


class AmalUsaha(models.Model):
    BIDANG_CHOICES = [
        ('pendidikan', 'Pendidikan'),
        ('kesehatan', 'Kesehatan'),
        ('sosial', 'Sosial'),
        ('ekonomi', 'Ekonomi'),
    ]

    nama = models.CharField(max_length=200)
    bidang = models.CharField(max_length=30, choices=BIDANG_CHOICES)
    deskripsi = models.TextField()
    alamat = models.TextField()
    gambar = models.ImageField(upload_to='amal_usaha/', blank=True, null=True)

    class Meta:
        verbose_name = "Amal Usaha"
        verbose_name_plural = "Amal Usaha"
        ordering = ['bidang', 'nama']

    def __str__(self):
        return f"{self.nama} ({self.get_bidang_display()})"


class BeritaQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status_terbit='terbit', tanggal_terbit__lte=timezone.now())


class BeritaManager(models.Manager):
    def get_queryset(self):
        return BeritaQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Berita(models.Model):
    STATUS_CHOICES = [
        ('draf', 'Draf'),
        ('terbit', 'Terbit'),
    ]

    judul = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text="Dibuat otomatis dari judul jika dikosongkan"
    )
    ringkasan = models.TextField(help_text="Ringkasan singkat berita untuk kartu beranda/daftar")
    isi = models.TextField(help_text="Isi lengkap artikel berita")
    gambar_sampul = models.ImageField(upload_to='berita/', blank=True, null=True)
    tanggal_terbit = models.DateTimeField(default=timezone.now)
    status_terbit = models.CharField(max_length=20, choices=STATUS_CHOICES, default='terbit')

    objects = BeritaManager()

    class Meta:
        verbose_name = "Berita"
        verbose_name_plural = "Berita"
        ordering = ['-tanggal_terbit']

    def __str__(self):
        return self.judul

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.judul) or "berita"
            slug = base_slug
            counter = 1
            while Berita.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pcm:berita_detail', kwargs={'slug': self.slug})

    @property
    def jumlah_kata(self):
        return len(self.isi.split()) if self.isi else 0

    @property
    def estimasi_waktu_baca(self):
        kata = self.jumlah_kata
        menit = max(1, round(kata / 180)) if kata > 0 else 1
        return f"{menit} menit baca"


class Agenda(models.Model):
    nama_kegiatan = models.CharField(max_length=250)
    waktu_mulai = models.DateTimeField()
    tempat = models.CharField(max_length=250)
    keterangan = models.TextField(blank=True)

    class Meta:
        verbose_name = "Agenda"
        verbose_name_plural = "Agenda"
        ordering = ['waktu_mulai']

    def __str__(self):
        return self.nama_kegiatan

    @property
    def is_upcoming(self):
        return self.waktu_mulai >= timezone.now()

    @property
    def sisa_hari(self):
        delta = self.waktu_mulai.date() - timezone.now().date()
        if delta.days == 0:
            return "Hari ini"
        elif delta.days == 1:
            return "Besok"
        elif delta.days > 1:
            return f"{delta.days} hari lagi"
        return "Telah lewat"

    @property
    def google_calendar_url(self):
        from urllib.parse import quote
        waktu_str = self.waktu_mulai.strftime('%Y%m%dT%H%M%SZ')
        return f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={quote(self.nama_kegiatan)}&location={quote(self.tempat)}&details={quote(self.keterangan or '')}&dates={waktu_str}/{waktu_str}"


class Dokumen(models.Model):
    judul = models.CharField(max_length=250)
    keterangan = models.TextField(blank=True)
    berkas = models.FileField(upload_to='dokumen/')
    tanggal_unggah = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dokumen"
        verbose_name_plural = "Dokumen"
        ordering = ['-tanggal_unggah']

    def __str__(self):
        return self.judul

    def clean(self):
        super().clean()
        if self.berkas:
            try:
                max_size = 25 * 1024 * 1024
                if self.berkas.size > max_size:
                    raise ValidationError("Ukuran berkas melebihi batas maksimal 25 MB.")
            except (FileNotFoundError, OSError, ValueError):
                pass


class PesanMasuk(models.Model):
    nama = models.CharField(max_length=150)
    email = models.EmailField()
    subjek = models.CharField(max_length=200)
    pesan = models.TextField()
    waktu_kirim = models.DateTimeField(auto_now_add=True)
    sudah_dibaca = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Pesan Masuk"
        verbose_name_plural = "Pesan Masuk"
        ordering = ['-waktu_kirim']

    def __str__(self):
        return f"[{self.waktu_kirim.strftime('%d/%m/%Y %H:%M')}] {self.nama}: {self.subjek}"


class TautanTerkait(models.Model):
    nama = models.CharField(max_length=150)
    url = models.URLField()
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Tautan Terkait"
        verbose_name_plural = "Tautan Terkait"
        ordering = ['urutan', 'nama']

    def __str__(self):
        return self.nama

    def clean(self):
        super().clean()
        if self.url and not (self.url.startswith('http://') or self.url.startswith('https://')):
            raise ValidationError({'url': "Format URL harus diawali dengan http:// atau https://"})
