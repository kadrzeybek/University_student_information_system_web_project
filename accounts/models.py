from django.db import models

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=15)

    student = models.OneToOneField('students.Students', on_delete=models.CASCADE, null=True, blank=True)
    instructor = models.OneToOneField('instructors.Instructors', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return f"user_id: {self.user_id}, username: {self.username}\npassword_hash: {self.password_hash}\nrole: {self.role}"

