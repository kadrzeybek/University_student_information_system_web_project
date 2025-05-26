from django.shortcuts import render
from .models import Instructors
from common.models import Courses

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