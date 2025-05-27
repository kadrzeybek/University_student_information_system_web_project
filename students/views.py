from django.shortcuts import render
from .models import Students, Enrollments, Grades
from common.models import Schedules, Announcements

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
    student_id = request.session['student_id']
    
    # Öğrenci bilgilerini çek
    student = Students.objects.filter(student_id=student_id).first()
    
    # Öğrencinin aldığı dersler
    enrollments = Enrollments.objects.filter(
        student_id=student_id
    )
    course_ids = enrollments.values_list('course_id', flat=True)
    course_count = enrollments.count()  # Ders sayısı
    
    # Notları çekme ve GPA hesaplama
    grades = Grades.objects.filter(
        enrollment__student_id=student_id
    ).select_related('enrollment__course')
    
    # GPA hesaplama (4.0 ölçeğinde)
    total_credit = 0
    weighted_sum = 0
    
    for grade in grades:
        if grade.midterm is not None and grade.final is not None:
            course = grade.enrollment.course
            course_credit = getattr(course, 'credit', 1)  # Kredi alanı yoksa 1 varsay
            
            # Ağırlıklı ortalama: %40 midterm, %60 final (100 üzerinden)
            course_grade = grade.midterm * 0.4 + grade.final * 0.6
            
            # 100'lük sistemden 4.0'lık sisteme basit dönüşüm
            gpa_point = course_grade / 25
            
            total_credit += course_credit
            weighted_sum += course_credit * gpa_point
    
    gpa = round(weighted_sum / total_credit, 2) if total_credit > 0 else 0
    
    # Bu derslere ait duyurular
    announcements = Announcements.objects.filter(
        course_id__in=course_ids
    ).select_related('course', 'instructor').order_by('-created_at')
    
    return render(request, 'students/homepage.html', {
        'student': student,
        'course_count': course_count,
        'gpa': gpa,
        'semester': student.class_level,  # Öğrencinin dönemi/sınıf seviyesi
        'announcements': announcements
    })

def grades_view(request):
    grades = Grades.objects.filter(
        enrollment__student_id=request.session['student_id']
    ).select_related('enrollment__course')

    # Her ders için midterm ve final ayrı sütun olarak alınır
    course_grades = {}
    for grade in grades:
        course = grade.enrollment.course
        course_key = course.course_code
        if course_key not in course_grades:
            course_grades[course_key] = {
                'course_name': course.course_name,
                'midterm': grade.midterm,
                'final': grade.final,
                'average': None,
                'letter': None,  # Letter grade (harf notu) eklendi
            }

    # Ortalama ve harf notunu hesapla
    for course in course_grades.values():
        if course['midterm'] is not None and course['final'] is not None:
            average = round(course['midterm'] * 0.4 + course['final'] * 0.6, 2)
            course['average'] = average
            course['letter'] = get_letter_grade(average)  # Harf notu hesaplama

    return render(request, 'students/grades.html', context={
        'course_grades': course_grades.values(),
    })

# Harf notu hesaplama fonksiyonu
def get_letter_grade(score):
    if score >= 90:
        return "AA"
    elif score >= 85:
        return "BA"
    elif score >= 80:
        return "BB"
    elif score >= 75:
        return "CB"
    elif score >= 70:
        return "CC"
    elif score >= 60:
        return "DC"
    elif score >= 50:
        return "DD"
    elif score >= 40:
        return "FD"
    else:
        return "FF"

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