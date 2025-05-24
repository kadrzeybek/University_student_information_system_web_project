from django.core.management.base import BaseCommand
from students.models import Students, Enrollments
from instructors.models import Instructors
from common.models import Departments, Faculties, Courses, Classrooms
from datetime import date

class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):
        # Var olan ilk fakülte ve departmanı kullan
        faculty = Faculties.objects.first()
        department1 = Departments.objects.filter(department_name="Yazılım Mühendisliği", faculty=faculty).first()

        # Derslik ekle veya varsa kullan
        classroom, _ = Classrooms.objects.get_or_create(
            room_number="A101",
            building_name="Mühendislik Binası",
            capacity=60
        )

        # Var olan ilk instructor'ı kullan
        instructor = Instructors.objects.filter(department=department1).first()

        # Ders ekle veya varsa kullan
        course, _ = Courses.objects.get_or_create(
            course_name="Veritabanı Sistemleri",
            credits=4,
            department=department1,
            instructor=instructor
        )

        # Var olan ilk öğrenciyi kullan
        student = Students.objects.filter(department=department1).first()

        # Öğrenciye enrollment ekle
        if student:
            Enrollments.objects.get_or_create(
                student=student,
                course=course,
                defaults={'enrollment_date': date.today()}
            )

        self.stdout.write(self.style.SUCCESS("Veritabanı başarıyla dolduruldu!"))