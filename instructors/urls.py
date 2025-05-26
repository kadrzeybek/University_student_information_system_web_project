from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('my_courses/', views.courses_view, name='my_courses')
]
