from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from accounts.models import Users
from students.models import Students
from instructors.models import Instructors
from common.models import Departments, Faculties, Courses, Classrooms

class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):
        # Fakülte ekle
        faculty, _ = Faculties.objects.get_or_create(faculty_name="Mühendislik Fakültesi")

        # Bölümler ekle
        department1, _ = Departments.objects.get_or_create(department_name="Yazılım Mühendisliği", faculty=faculty)
        department2, _ = Departments.objects.get_or_create(department_name="Elektrik-Elektronik Mühendisliği", faculty=faculty)
        department3, _ = Departments.objects.get_or_create(department_name="Makine Mühendisliği", faculty=faculty)

        # Derslik ekle
        # classroom, _ = Classrooms.objects.get_or_create(
        #     room_number="A101",
        #     building_name="Mühendislik Binası",
        #     capacity=60
        # )

        # Eğitmen ekle
        instructor = Instructors.objects.create(
            first_name="Mehmet",
            last_name="Yılmaz",
            email="mehmet.yilmaz@example.com",
            phone_number="05551234567",
            department=department1
        )

        # # Ders ekle
        # course, _ = Courses.objects.get_or_create(
        #     course_name="Veritabanı Sistemleri",
        #     credits=4,
        #     department=department1,
        #     instructor=instructor
        # )

        # Öğrenci ekle
        student = Students.objects.create(
            first_name="Salih Muharrem",
            last_name="Kütükte",
            date_of_birth="2000-11-11",
            email="salihMuharrem@example.com",
            phone_number="05321234567",
            identity_no="11111111111",
            class_level="3",
            status="Aktif",
            department=department1
        )

        # Kullanıcı ekle (öğrenci)
        Users.objects.create(
            user_id=1,
            username="salih",
            password_hash=make_password("123456"),
            role="student",
            student=student
        )

        # Kullanıcı ekle (eğitmen)
        Users.objects.create(
            user_id=2,
            username="mehmet",
            password_hash=make_password("654321"),
            role="instructor",
            instructor=instructor
        )

        self.stdout.write(self.style.SUCCESS("Veritabanı başarıyla dolduruldu!"))