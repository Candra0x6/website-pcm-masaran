from django import forms
from django.utils.html import strip_tags
from .models import PesanMasuk


class KontakForm(forms.ModelForm):
    class Meta:
        model = PesanMasuk
        fields = ['nama', 'email', 'subjek', 'pesan']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 rounded-xl bg-neutral-50 border border-neutral-200 text-neutral-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-transparent transition text-sm',
                'placeholder': 'Nama lengkap Anda',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-5 py-4 rounded-xl bg-neutral-50 border border-neutral-200 text-neutral-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-transparent transition text-sm',
                'placeholder': 'alamat.email@domain.com',
                'required': True,
            }),
            'subjek': forms.TextInput(attrs={
                'class': 'w-full px-5 py-4 rounded-xl bg-neutral-50 border border-neutral-200 text-neutral-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-transparent transition text-sm',
                'placeholder': 'Perihal / Subjek pesan',
                'required': True,
            }),
            'pesan': forms.Textarea(attrs={
                'class': 'w-full px-5 py-4 rounded-xl bg-neutral-50 border border-neutral-200 text-neutral-900 focus:bg-white focus:outline-none focus:ring-2 focus:ring-emerald-600 focus:border-transparent transition text-sm resize-y',
                'placeholder': 'Tuliskan pesan, aspirasi, atau pertanyaan Anda di sini...',
                'rows': 5,
                'required': True,
            }),
        }

    def clean_nama(self):
        nama = strip_tags(self.cleaned_data.get('nama', '')).strip()
        if len(nama) < 3:
            raise forms.ValidationError("Nama lengkap minimal 3 karakter.")
        return nama

    def clean_subjek(self):
        subjek = strip_tags(self.cleaned_data.get('subjek', '')).strip()
        if len(subjek) < 4:
            raise forms.ValidationError("Subjek pesan minimal 4 karakter.")
        return subjek

    def clean_pesan(self):
        pesan = strip_tags(self.cleaned_data.get('pesan', '')).strip()
        if len(pesan) < 10:
            raise forms.ValidationError("Pesan terlalu pendek. Mohon berikan minimal 10 karakter.")
        return pesan
