from django.db import models

class Instructors(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True)
    email = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=30, default="Unknown")
    office = models.CharField(max_length=20, default="No Office Available")
    department = models.ForeignKey('common.Departments', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Instructors'
