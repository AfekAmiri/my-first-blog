from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.base, name='base'),
    path('wiki/', views.wiki_page, name='wiki'),
    path('accueil/', views.accueil_page, name='accueil'),
    path('accueil/accueil_action/', views.accueil_action, name='accueil_action'),
    path('accueil/nourrir/', views.nourrir, name='nourrir'),
    path('accueil/divertir/', views.divertir, name='divertir'),
    path('accueil/soigner/', views.soigner, name='soigner'),
    path('accueil/capturer/', views.capturer, name='capturer'),
    path('pokemon/<str:nom>/', views.pokemon_detail, name='pokemon_detail'),
    path('pokemon/<str:nom>/?<str:message>', views.pokemon_detail, name='pokemon_detail_mes'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)