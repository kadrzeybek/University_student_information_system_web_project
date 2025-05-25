from django.urls import path
from . import views

urlpatterns = [
    path('homepage/', views.homepage_view, name='homepage'),
    path('grades/', views.grades_view, name='grades'),
    path('registration/', views.registration_view, name='registration'),
    path('course-program/', views.course_program_view, name='course_program'),
    path('my-courses/', views.my_courses_view, name='my_courses'),
    #path('logout/', views.logout_view, name='logout'),
]