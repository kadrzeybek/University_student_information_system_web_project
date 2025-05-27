from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='instructor_profile'),
    path('my-courses/', views.courses_view, name='instructor_my_courses'),
    path('course-program/', views.course_program_view, name='instructor_course_program'),
    path('grades/', views.grades_view, name='instructor_grades'),
    path('homepage/', views.homepage_view, name='instructor_homepage'),
    path('announcement/create/', views.announcement_create, name='instructor_announcement_create'),
    path('grade-entry/<int:course_id>/', views.grades_view, name='instructor_grade_entry'),
]
