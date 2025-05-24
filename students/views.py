from django.shortcuts import render
from .models import Students, Enrollments


def profile_view(request):
    student = Students.objects.filter(student_id=request.session['user_id']).first()
    department = student.department if student else None
    faculty = department.faculty if department else None
    
    return render(request,'students/profile.html', context = {
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

def enroll_view(request):
    enrollments = Enrollments.objects.filter(student_id=request.session['user_id']).select_related('course')

    return render(request, 'students/enrollment.html', context={
        'enrollments': enrollments
    })

def homepage_view(request):
    return render(request, 'students/homepage.html')