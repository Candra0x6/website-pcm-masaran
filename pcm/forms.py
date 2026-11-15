from django import forms
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

    def clean_pesan(self):
        pesan = self.cleaned_data.get('pesan', '').strip()
        if len(pesan) < 10:
            raise forms.ValidationError("Pesan terlalu pendek. Mohon berikan minimal 10 karakter.")
        return pesan
