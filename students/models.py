from django.db import models


class Students(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    department = models.ForeignKey('common.Departments', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Students'

class Enrollments(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    course = models.ForeignKey('common.Courses', on_delete=models.CASCADE)
    enrollment_date = models.DateField()

    class Meta:
        db_table = 'Enrollments'

class Grades(models.Model):
    grade_id = models.AutoField(primary_key=True)
    enrollment = models.ForeignKey(Enrollments, on_delete=models.CASCADE)
    grade_value = models.CharField(max_length=255)

    class Meta:
        db_table = 'Grades'

    