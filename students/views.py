from django.shortcuts import render
from .models import Students, Enrollments
from common.models import Schedules

def registration_view(request):
    student = Students.objects.filter(student_id=request.session['student_id']).select_related("department__faculty").first()

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
        'department': student.department.department_name,
        'faculty': student.department.faculty.faculty_name
        })

def my_courses_view(request):
    enrollments = Enrollments.objects.filter(student_id=request.session['student_id']).select_related('course')

    return render(request, 'students/my_courses.html', context={
        'enrollments': enrollments
    })

def homepage_view(request):
    return render(request, 'students/homepage.html')


def grades_view(request):
    return render(request, 'students/grades.html', context={
    })

def course_program_view(request):
    schedules = Schedules.objects.filter(
        course__enrollments__student_id=request.session['student_id']
    ).select_related('course', 'classroom')

    hours = [
        ("08:00", "09:00"), ("09:00", "10:00"), ("10:00", "11:00"),
        ("11:00", "12:00"), ("12:00", "13:00"), ("13:00", "14:00"),
        ("14:00", "15:00"), ("15:00", "16:00"), ("16:00", "17:00"),
        ("17:00", "18:00"), ("19:00", "20:00"), ("20:00", "21:00"),
        ("21:00", "22:00"), ("22:00", "23:00"), ("23:00", "24:00"),
    ]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Düz bir tablo yapısı oluştur
    flat_table = {}
    for hour_start, hour_end in hours:
        for day in days:
            flat_key = f"{hour_start}-{hour_end}-{day}"
            flat_table[flat_key] = ""

    # Ders bilgilerini ekle
    for schedule in schedules:
        for start, end in hours:
            if str(schedule.start_time)[:5] == start:
                flat_key = f"{start}-{end}-{schedule.day_of_week}"
                flat_table[flat_key] = (
                    f"{schedule.course.course_code} - {schedule.course.course_name}<br>"
                    f"<small>{schedule.classroom.room_number}</small>"
                )

    # Template'e gönder
    return render(request, 'students/course_program.html', {
        'flat_table': flat_table,
        'hours': hours,
        'days': days,
    })