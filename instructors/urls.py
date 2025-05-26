from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='instructor_profile'),
    path('my-courses/', views.courses_view, name='instructor_my_courses')
]
