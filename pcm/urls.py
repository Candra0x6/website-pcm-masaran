from django.urls import path
from . import views

app_name = 'pcm'

urlpatterns = [
    path('', views.beranda_view, name='beranda'),
    path('profil/', views.profil_view, name='profil'),
    path('pimpinan/', views.pimpinan_view, name='pimpinan'),
    path('ranting/', views.ranting_view, name='ranting'),
    path('amal-usaha/', views.amal_usaha_view, name='amal_usaha'),
    path('berita/', views.berita_list_view, name='berita_list'),
    path('berita/<slug:slug>/', views.berita_detail_view, name='berita_detail'),
    path('agenda/', views.agenda_view, name='agenda'),
    path('unduhan/', views.unduhan_view, name='unduhan'),
    path('kontak/', views.kontak_view, name='kontak'),
    path('api/health/', views.api_health_check_view, name='api_health_check'),
    path('sitemap.xml', views.sitemap_xml_view, name='sitemap_xml'),
]
