from django.db import models

class Instructors(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    department = models.ForeignKey('common.Departments', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Instructors'
