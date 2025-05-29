from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Instructors
from common.models import Courses, Schedules, Announcements
from django.utils import timezone
from django.db.models import Count
from students.models import Enrollments, Grades
from django.http import Http404

def profile_view(request):
    # Get instructor from database with its department and faculty
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
        'courses': Courses.objects.filter(instructor_id=request.session['instructor_id'])
    })

def courses_view(request):
    instructor_id = request.session['instructor_id']
    
    # Get course information with student count
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

    # Create a empty table
    flat_table = {}
    for hour_start, hour_end in hours:
        for day in days:
            flat_key = f"{hour_start}-{hour_end}-{day}"
            flat_table[flat_key] = ""

    # Insert table data
    for schedule in schedules:
        start_time = schedule.start_time
        end_time = schedule.end_time
        
        # Saatleri sayısal değerlere dönüştür (örn. "08:00" -> 8.0)
        start_hour = float(start_time.split(':')[0]) + float(start_time.split(':')[1])/60
        end_hour = float(end_time.split(':')[0]) + float(end_time.split(':')[1])/60
        
        # Dersin tüm süresini kapsayan hücreleri işaretle
        for start, end in hours:
            hour_start_val = float(start.split(':')[0]) + float(start.split(':')[1])/60
            hour_end_val = float(end.split(':')[0]) + float(end.split(':')[1])/60
            
            # Bu saat dilimi ders süresinin içindeyse ders bilgisini ekle
            if hour_start_val >= start_hour and hour_start_val < end_hour:
                flat_key = f"{start}-{end}-{schedule.day_of_week}"
                
                # İlk saat diliminde tam bilgi, diğerlerinde "continued" ekle
                if hour_start_val == start_hour:
                    flat_table[flat_key] = (
                        f"{schedule.course.course_code} - {schedule.course.course_name}<br>"
                        f"<small>{schedule.classroom.room_number}</small><br>"
                    )
                else:
                    flat_table[flat_key] = (
                        f"{schedule.course.course_code} - {schedule.course.course_name}<br>"
                        f"<small>{schedule.classroom.room_number}</small><br>"
                    )

    return render(request, 'instructors/course_program.html', {
        'flat_table': flat_table,
        'hours': hours,
        'days': days,
        'courses': Courses.objects.filter(instructor_id=request.session['instructor_id'])
    })

def grades_view(request, course_id=None):
    instructor_id = request.session['instructor_id']
    courses = Courses.objects.filter(instructor_id=instructor_id)
    
    if course_id is None and courses.exists():
        course_id = courses.first().course_id

    try:
        course = Courses.objects.get(course_id=course_id, instructor_id=instructor_id)
    except Courses.DoesNotExist:
        raise Http404("You do not have access to this course or course could not be founded.")

    enrollments = Enrollments.objects.filter(course_id=course_id).select_related('student')

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
        incorrect_records = 0

        for enrollment_id, values in request.POST.items():
            if enrollment_id.startswith('midterm_') or enrollment_id.startswith('final_'):
                parts = enrollment_id.split('_')
                field_type = parts[0]
                enroll_id = int(parts[1])

                try:
                    grade = Grades.objects.get(enrollment_id=enroll_id)
                    if field_type == 'midterm' and values:
                        grade.midterm = int(values)
                    elif field_type == 'final' and values:
                        grade.final = int(values)
                    grade.save()
                except (Grades.DoesNotExist, ValueError):
                    incorrect_records += 1

        if incorrect_records:
            messages.warning(request, f"{incorrect_records} Record could not be updated.")
        else:
            messages.success(request, "Grades saved successfully.")
        
        return redirect('instructor_grade_entry', course_id=course_id)

    return render(request, 'instructors/grades.html', {
        'course': course,
        'courses': courses,
        'students_data': students_data
    })


def announcement_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        course_id = request.POST.get('course')
        
        # Get course and its instructor data
        course = Courses.objects.get(course_id=course_id)
        instructor_id = request.session.get('instructor_id')
        
        # Create a new announcement
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

def homepage_view(request):
    instructor = Instructors.objects.filter(instructor_id=request.session['instructor_id']).first()
    courses = Courses.objects.filter(instructor_id=instructor.instructor_id)
    course_count = courses.count()
    
    # Finding distinct student count
    course_ids = courses.values_list('course_id', flat=True)
    student_count = Enrollments.objects.filter(
        course_id__in=course_ids
    ).values('student_id').distinct().count()
    
    # Get last 5 announcements
    announcements = Announcements.objects.filter(
        instructor_id=instructor.instructor_id
    ).select_related('course').order_by('-created_at')[:5]
    
    return render(request, 'instructors/homepage.html', {
        'first_name': instructor.first_name,
        'last_name': instructor.last_name,
        'title': instructor.title,
        'course_count': course_count,
        'student_count': student_count,
        'courses': courses,
        'announcements': announcements
    })