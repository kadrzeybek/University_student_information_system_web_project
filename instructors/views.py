from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Instructors
from common.models import Courses, Schedules, Announcements
from django.utils import timezone
from django.db.models import Count, OuterRef, Subquery
from students.models import Enrollments, Grades
from django.http import Http404

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
    instructor_id = request.session['instructor_id']
    
    # Tek sorguda kursları ve öğrenci sayılarını çek
    courses = Courses.objects.filter(
        instructor_id=instructor_id
    ).annotate(
        student_count=Count('enrollments')
    ).order_by('course_code')
    
    return render(request, 'instructors/my_courses.html', {
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

def grades_view(request, course_id=None):
    instructor_id = request.session['instructor_id']
    courses = Courses.objects.filter(instructor_id=instructor_id)
    
    # Eğer course_id belirtilmemişse ilk kursu seç
    if course_id is None and courses.exists():
        course_id = courses.first().course_id
    
    # Kurs kontrolü
    try:
        course = Courses.objects.get(course_id=course_id, instructor_id=instructor_id)
    except Courses.DoesNotExist:
        raise Http404("Bu kursa erişim izniniz yok veya kurs bulunamadı.")
        
    # Öğrenci kayıtlarını ve notlarını getir
    enrollments = Enrollments.objects.filter(
        course_id=course_id
    ).select_related('student')
    
    # Her kayıt için not bilgilerini al veya oluştur
    students_data = []
    for enrollment in enrollments:
        grade, created = Grades.objects.get_or_create(enrollment=enrollment)
        students_data.append({
            'enrollment_id': enrollment.enrollment_id,
            'student_id': enrollment.student.student_id,
            'student_name': f"{enrollment.student.first_name} {enrollment.student.last_name}",
            'midterm': grade.midterm,
            'final': grade.final
        })
    
    if request.method == 'POST':
        # Form verilerini işle
        for enrollment_id, values in request.POST.items():
            if enrollment_id.startswith('midterm_') or enrollment_id.startswith('final_'):
                parts = enrollment_id.split('_')
                field_type = parts[0]  # 'midterm' veya 'final'
                enroll_id = int(parts[1])
                
                try:
                    grade = Grades.objects.get(enrollment_id=enroll_id)
                    if field_type == 'midterm' and values:
                        grade.midterm = int(values)
                    elif field_type == 'final' and values:
                        grade.final = int(values)
                    grade.save()
                except (Grades.DoesNotExist, ValueError):
                    pass
        
        messages.success(request, "Notlar başarıyla kaydedildi.")
        return redirect('instructor_grade_entry', course_id=course_id)
    
    return render(request, 'instructors/grades.html', {
        'course': course,
        'courses': courses,  # Sidebar için gerekli
        'students_data': students_data
    })

def announcement_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        course_id = request.POST.get('course')
        
        # Kurs ve instructor bilgilerini al
        course = Courses.objects.get(course_id=course_id)
        instructor_id = request.session.get('instructor_id')
        
        # Announcement oluştur
        announcement = Announcements(
            title=title,
            message=message,
            course=course,
            instructor_id=instructor_id,
            created_at=timezone.now()
        )
        announcement.save()
        
        messages.success(request, 'Announcement created successfully!')
        return redirect('instructor_homepage')
    
    # GET isteği için kursları getir
    courses = Courses.objects.filter(instructor_id=request.session['instructor_id'])
    return render(request, 'instructors/create_announcement.html', {'courses': courses})

def homepage_view(request):
    instructor_id = request.session['instructor_id']
    courses = Courses.objects.filter(instructor_id=instructor_id)
    course_count = courses.count()
    
    # Benzersiz öğrenci sayısını bulma
    from students.models import Enrollments
    course_ids = courses.values_list('course_id', flat=True)
    
    # distinct('student_id') ile tekrarlı öğrencileri filtreleme
    student_count = Enrollments.objects.filter(
        course_id__in=course_ids
    ).values('student_id').distinct().count()
    
    # Duyuruları getir
    announcements = Announcements.objects.filter(
        instructor_id=instructor_id
    ).select_related('course').order_by('-created_at')[:5]
    
    return render(request, 'instructors/homepage.html', {
        'course_count': course_count,
        'student_count': student_count,
        'courses': courses,
        'announcements': announcements
    })