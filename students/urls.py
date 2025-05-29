from django.urls import path
from . import views

urlpatterns = [
    path('homepage/', views.homepage_view, name='student_homepage'),
    path('grades/', views.grades_view, name='student_grades'),
    path('registration/', views.registration_view, name='student_registration'),
    path('course-program/', views.course_program_view, name='student_course_program'),
    path('my-courses/', views.my_courses_view, name='student_my_courses'),
]