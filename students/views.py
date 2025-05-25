from django.shortcuts import render
from .models import Students, Enrollments
from common.models import Schedules

def registration_view(request):
    student = Students.objects.filter(student_id=request.session['user_id']).first()
    department = student.department if student else None
    faculty = department.faculty if department else None

    return render(request,'students/registration.html', context = {
        'student_id': student.student_id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'date_of_birth': student.date_of_birth,
        'email': student.email,
        'phone_number': student.phone_number,
        'identity_no': student.identity_no,
        'class_level': student.class_level,
        'status': student.status,
        'department': department.department_name,
        'faculty': faculty.faculty_name,
        })

def my_courses_view(request):
    enrollments = Enrollments.objects.filter(student_id=request.session['user_id']).select_related('course')

    return render(request, 'students/my_courses.html', context={
        'enrollments': enrollments
    })

def homepage_view(request):
    return render(request, 'students/homepage.html')


def grades_view(request):
    return render(request, 'students/grades.html', context={
    })

def course_program_view(request):
    enrollments = Enrollments.objects.filter(student_id=request.session['user_id'])
    schedules = []
    for enrollment in enrollments :
        schedules.append(Schedules.objects.filter(course_id=enrollment.course_id).select_related('course','classroom').first())
    for schedule in schedules :
        print()   



    return render(request, 'students/course_program.html', context={
        'schedules': schedules
    })