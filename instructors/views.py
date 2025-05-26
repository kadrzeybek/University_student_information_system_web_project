from django.shortcuts import render
from .models import Instructors

def profile_view(request):
    instructor = Instructors.objects.filter(instructor_id=request.session['instructor_id']).first()
    department = instructor.department if instructor else None
    faculty = department.faculty if department else None
    print(instructor.first_name)

    return render(request,'instructors/profile.html', context = {
        'first_name': instructor.first_name,
        'last_name': instructor.last_name,
        'date_of_birth': instructor.date_of_birth,
        'email': instructor.email,
        'phone_number': instructor.phone_number,
        'title': instructor.title,
        'office': instructor.office,
        'department': department.department_name,
        'faculty': faculty.faculty_name,
        })

def courses_view(request):
    return render(request,'instructors/my_courses.html')