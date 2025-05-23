from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profil_view, name='profil'),
]