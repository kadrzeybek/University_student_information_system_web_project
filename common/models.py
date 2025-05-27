from django.db import models
from django.utils import timezone


class Faculties(models.Model):
    faculty_id = models.AutoField(primary_key=True)
    faculty_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Faculties'

class Departments(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=50)
    faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Departments'
    
class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=75)
    credits = models.IntegerField()
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    instructor = models.ForeignKey('instructors.Instructors', on_delete=models.CASCADE)
    semester = models.CharField(max_length=25, default="Unknown")
    course_code = models.CharField(max_length=10, default="Unknown")

    class Meta:
        db_table = 'Courses'
    
class Classrooms(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=20)
    building_name = models.CharField(max_length=30)
    capacity = models.IntegerField()

    class Meta:
        db_table = 'Classrooms'

class Schedules(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=15)
    start_time = models.CharField(max_length=10, default="Unknown")
    end_time = models.CharField(max_length=10, default="Unknown")

    class Meta:
        db_table = 'Schedules'

class Announcements(models.Model):
    announcement_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    message = models.TextField()
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    instructor = models.ForeignKey('instructors.Instructors', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'Announcements'
        ordering = ['-created_at']