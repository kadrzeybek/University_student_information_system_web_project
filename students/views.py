from django.shortcuts import render, redirect
from .models import Students, Enrollments, Grades
from common.models import Schedules, Announcements

def registration_view(request):
    """
    Displays student registration and personal information.
    
    Retrieves student data from the database and renders it in the registration
    template. Includes personal details and academic information.
    """
    # Retrieve student data with related department and faculty information
    student = Students.objects.filter(student_id=request.session['student_id']).select_related("department__faculty").first()

    # Render template with comprehensive student details
    return render(request,'students/registration.html', context = {
        'student_id': student.student_id,          # Student identification number
        'first_name': student.first_name,          # Student's given name
        'last_name': student.last_name,            # Student's surname
        'date_of_birth': student.date_of_birth,    # Student's birth date
        'email': student.email,                    # Contact email address
        'phone_number': student.phone_number,      # Contact phone number
        'identity_no': student.identity_no,        # National/government ID number
        'class_level': student.class_level,        # Current year/grade level
        'status': student.status,                  # Enrollment status (active, etc.)
        'department': student.department.department_name,  # Academic department
        'faculty': student.department.faculty.faculty_name # Faculty/school name
    })

def my_courses_view(request):
    """
    Displays all courses that a student is currently enrolled in.
    
    Retrieves enrollment data with course details and passes it to the template.
    """
    # Get all enrollments for the current student with related course information
    enrollments = Enrollments.objects.filter(student_id=request.session['student_id']).select_related('course')

    # Render template with enrollment data
    return render(request, 'students/my_courses.html', context={
        'enrollments': enrollments  # List of course enrollments with course details
    })

def homepage_view(request):
    """
    Renders the student dashboard homepage with key academic information.
    
    Includes personal details, course counts, GPA calculation, enrollment status,
    and recent announcements from enrolled courses.
    """
    student_id = request.session['student_id']
    
    # Retrieve basic student information
    student = Students.objects.filter(student_id=student_id).first()
    
    # Get all courses the student is enrolled in
    enrollments = Enrollments.objects.filter(
        student_id=student_id
    )
    course_ids = enrollments.values_list('course_id', flat=True)  # Extract just the course IDs
    course_count = enrollments.count()  # Calculate total number of courses
    
    # Retrieve grade information for GPA calculation
    grades = Grades.objects.filter(
        enrollment__student_id=student_id
    ).select_related('enrollment__course')
    
    # Calculate GPA on a 4.0 scale
    total_credit = 0
    weighted_sum = 0
    
    for grade in grades:
        if grade.midterm is not None and grade.final is not None:
            course = grade.enrollment.course
            course_credit = getattr(course, 'credit', 1)  # Default to 1 if credit field missing
            
            # Calculate weighted average: 40% midterm + 60% final
            course_grade = grade.midterm * 0.4 + grade.final * 0.6
            
            # Convert from 100-point scale to 4.0 scale
            gpa_point = course_grade / 25
            
            # Add to running totals for weighted GPA calculation
            total_credit += course_credit
            weighted_sum += course_credit * gpa_point
    
    # Calculate final GPA, rounded to 2 decimal places
    gpa = round(weighted_sum / total_credit, 2) if total_credit > 0 else 0
    
    # Get announcements from all courses the student is taking
    announcements = Announcements.objects.filter(
        course_id__in=course_ids
    ).select_related('course', 'instructor').order_by('-created_at')
    
    # Render the dashboard with all calculated and retrieved information
    return render(request, 'students/homepage.html', {
        'student': student,               # Student personal information
        'course_count': course_count,     # Number of enrolled courses
        'gpa': gpa,                       # Calculated GPA on 4.0 scale
        'semester': student.class_level,  # Current academic term/year
        'announcements': announcements,   # Course-related announcements
        'status': student.status          # Current enrollment status
    })

def grades_view(request):
    """
    Displays all course grades for the student.
    
    Retrieves grades data, calculates weighted averages, and determines
    letter grades for each course.
    """
    # Get all grades for the current student with related course information
    grades = Grades.objects.filter(
        enrollment__student_id=request.session['student_id']
    ).select_related('enrollment__course')

    # Create a dictionary to hold grade information by course
    course_grades = {}
    for grade in grades:
        course = grade.enrollment.course
        course_key = course.course_code
        if course_key not in course_grades:
            course_grades[course_key] = {
                'course_name': course.course_name,  # Course title
                'midterm': grade.midterm,           # Midterm exam score
                'final': grade.final,               # Final exam score
                'average': None,                    # Placeholder for weighted average
                'letter': None,                     # Placeholder for letter grade
            }

    # Calculate weighted average and letter grade for each course
    for course in course_grades.values():
        if course['midterm'] is not None and course['final'] is not None:
            # Calculate weighted average (40% midterm, 60% final)
            average = round(course['midterm'] * 0.4 + course['final'] * 0.6, 2)
            course['average'] = average
            course['letter'] = get_letter_grade(average)  # Convert to letter grade

    # Render template with processed grade information
    return render(request, 'students/grades.html', context={
        'course_grades': course_grades.values(),  # List of course grade dictionaries
    })

def get_letter_grade(score):
    """
    Converts a numerical score to a letter grade.
    
    Args:
        score (float): The numerical score (0-100)
        
    Returns:
        str: The corresponding letter grade (AA to FF)
    """
    # Convert numerical score to standard letter grade
    if score >= 90:
        return "AA"      # Excellent (4.0)
    elif score >= 85:
        return "BA"      # Very Good (3.5)
    elif score >= 80:
        return "BB"      # Good (3.0)
    elif score >= 75:
        return "CB"      # Above Average (2.5)
    elif score >= 70:
        return "CC"      # Average (2.0)
    elif score >= 60:
        return "DC"      # Below Average (1.5)
    elif score >= 50:
        return "DD"      # Poor (1.0)
    elif score >= 40:
        return "FD"      # Very Poor (0.5)
    else:
        return "FF"      # Fail (0.0)

def course_program_view(request):
    """
    Displays the student's weekly course schedule as a timetable.
    
    Retrieves schedule information and organizes it into a day/time grid.
    """
    # Get all scheduled classes for courses the student is enrolled in
    schedules = Schedules.objects.filter(
        course__enrollments__student_id=request.session['student_id']
    ).select_related('course', 'classroom')

    # Define time slots and days for the schedule grid
    hours = [
        ("08:00", "09:00"), ("09:00", "10:00"), ("10:00", "11:00"),
        ("11:00", "12:00"), ("12:00", "13:00"), ("13:00", "14:00"),
        ("14:00", "15:00"), ("15:00", "16:00"), ("16:00", "17:00"),
        ("17:00", "18:00"), ("19:00", "20:00"), ("20:00", "21:00"),
        ("21:00", "22:00"), ("22:00", "23:00"), ("23:00", "24:00"),
    ]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Create an empty grid with all time slots and days
    flat_table = {}
    for hour_start, hour_end in hours:
        for day in days:
            flat_key = f"{hour_start}-{hour_end}-{day}"
            flat_table[flat_key] = ""  # Empty cell by default

    # Populate the grid with course schedule information
    for schedule in schedules:
        for start, end in hours:
            if str(schedule.start_time)[:5] == start:
                # Create a unique key for this time slot and day
                flat_key = f"{start}-{end}-{schedule.day_of_week}"
                # Add formatted course and classroom information
                flat_table[flat_key] = (
                    f"{schedule.course.course_code} - {schedule.course.course_name}<br>"
                    f"<small>{schedule.classroom.room_number}</small>"
                )

    # Render the template with the populated schedule grid
    return render(request, 'students/course_program.html', {
        'flat_table': flat_table,  # Grid of scheduled courses
        'hours': hours,            # Time slot definitions
        'days': days,              # Days of the week
    })