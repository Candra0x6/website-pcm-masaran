from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Berita


class LatestBeritaFeed(Feed):
    title = "Warta & Kabar PCM Masaran"
    link = "/berita/"
    description = "Pembaruan warta, kegiatan dakwah, dan informasi resmi dari Pimpinan Cabang Muhammadiyah Masaran."

    def items(self):
        return Berita.objects.published().order_by('-tanggal_terbit')[:20]

    def item_title(self, item):
        return item.judul

    def item_description(self, item):
        return item.ringkasan

    def item_pubdate(self, item):
        return item.tanggal_terbit

    def item_link(self, item):
        return item.get_absolute_url()
