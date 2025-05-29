from django.core.management.base import BaseCommand
from students.models import Students, Enrollments
from instructors.models import Instructors
from common.models import Departments, Faculties, Courses, Classrooms
from accounts.models import Users
from django.contrib.auth.hashers import make_password
from datetime import date, time
import random

# Schedule modeli için import ekleyin
from common.models import Schedules  # veya doğru dosya yolunu belirtin

FIRST_NAMES = [
    "John", "Emily", "Michael", "Sarah", "David", "Jessica", "Daniel", "Ashley", "Matthew", "Amanda",
    "James", "Jennifer", "Andrew", "Hannah", "Joseph", "Lauren", "Christopher", "Megan", "Joshua", "Rachel",
    "Brian", "Samantha", "Kevin", "Olivia", "Ryan", "Sophia", "Brandon", "Grace", "Justin", "Chloe",
    "Ethan", "Natalie", "Benjamin", "Victoria", "Samuel", "Lily", "Alexander", "Ava", "William", "Ella"
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Martinez", "Hernandez",
    "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee",
    "Clark", "Lewis", "Walker", "Hall", "Allen", "Young", "King", "Wright", "Scott", "Green",
    "Baker", "AdAMS", "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell"
]

DEPARTMENTS = [
    {
        "name": "Software Engineering",
        "short": "SE",
        "student_count": 40,
        "instructor_count": 5,
        "courses": [
            "Database Systems", "Algorithms", "Operating Systems", "Software Engineering",
            "Web Programming", "Mobile Development", "Data Structures", "Machine Learning"
        ]
    },
    {
        "name": "Mechanical Engineering",
        "short": "ME",
        "student_count": 24,
        "instructor_count": 4,
        "courses": [
            "Thermodynamics", "Fluid Mechanics", "Dynamics", "Statics",
            "Heat Transfer", "Manufacturing Processes", "Machine Design"
        ]
    },
    {
        "name": "Electrical and Electronics Engineering",
        "short": "EEE",
        "student_count": 20,
        "instructor_count": 4,
        "courses": [
            "Circuit Analysis", "Electromagnetics", "Digital Systems", "Control Systems",
            "Microprocessors", "Power Electronics", "Signals and Systems"
        ]
    },
    {
        "name": "Industrial Engineering",
        "short": "IE",
        "student_count": 24,
        "instructor_count": 4,
        "courses": [
            "Operations Research", "Production Planning", "Quality Control", "Supply Chain Management",
            "Human Factors Engineering", "Simulation", "Project Management"
        ]
    }
]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
HOURS = [
    (time(8, 30), time(10, 20)),
    (time(10, 30), time(12, 20)),
    (time(13, 0), time(14, 50)),
    (time(15, 0), time(16, 50)),
    (time(17, 0), time(18, 50))
]

class Command(BaseCommand):
    help = "Seeds the database with sample students, instructors, courses, and enrollments for multiple departments."

    def handle(self, *args, **kwargs):
        # Temizleme (isteğe bağlı)
        Students.objects.all().delete()
        Instructors.objects.all().delete()
        Courses.objects.all().delete()
        Enrollments.objects.all().delete()
        Users.objects.all().delete()
        Departments.objects.all().delete()
        Faculties.objects.all().delete()
        Classrooms.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))