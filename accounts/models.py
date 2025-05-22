from django.db import models

class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    student = models.OneToOneField('students.Students', on_delete=models.CASCADE, null=True, blank=True)
    instructor = models.OneToOneField('instructors.Instructors', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'Users'

