from django.shortcuts import render
from .models import Instructors
from common.models import Courses, Schedules

def profile_view(request):
    instructor = Instructors.objects.filter(instructor_id=request.session['instructor_id']).select_related("department__faculty").first()

    return render(request,'instructors/profile.html', context = {
        'first_name': instructor.first_name,
        'last_name': instructor.last_name,
        'date_of_birth': instructor.date_of_birth,
        'email': instructor.email,
        'phone_number': instructor.phone_number,
        'title': instructor.title,
        'office': instructor.office,
        'department': instructor.department.department_name,
        'faculty': instructor.department.faculty.faculty_name,
        })

def courses_view(request):
    courses = Courses.objects.filter(instructor_id=request.session['instructor_id'])

    return render(request,'instructors/my_courses.html', context={
        'courses': courses
    })

def course_program_view(request):
    schedules = Schedules.objects.filter(
        course__instructor_id=request.session['instructor_id']
    ).select_related('course', 'classroom')
    
    hours = [
        ("08:00", "09:00"), ("09:00", "10:00"), ("10:00", "11:00"),
        ("11:00", "12:00"), ("12:00", "13:00"), ("13:00", "14:00"),
        ("14:00", "15:00"), ("15:00", "16:00"), ("16:00", "17:00"),
        ("17:00", "18:00"), ("19:00", "20:00"), ("20:00", "21:00"),
        ("21:00", "22:00"), ("22:00", "23:00"), ("23:00", "24:00"),
    ]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Düz tablo yapısı oluştur
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
    return render(request, 'instructors/course_program.html', {
        'flat_table': flat_table,
        'hours': hours,
        'days': days,
    })