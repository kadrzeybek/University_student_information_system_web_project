from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='instructor_profile'),
    path('my-courses/', views.courses_view, name='instructor_my_courses'),
    path('course-program/', views.course_program_view, name='instructor_course_program'),
    path('grades/', views.grades_view, name='instructor_grades'),
]
