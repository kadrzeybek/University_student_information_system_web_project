from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('enroll/', views.enroll_view, name='enrollment'),
    path('homepage/', views.homepage_view, name='homepage'),
]