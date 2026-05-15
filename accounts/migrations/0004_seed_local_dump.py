from __future__ import annotations

from ast import literal_eval
from datetime import date, datetime, timezone as datetime_timezone
import re
from pathlib import Path

from django.conf import settings
from django.db import migrations


INSERT_RE = re.compile(r"^INSERT INTO `(?P<table>[^`]+)` VALUES (?P<values>.+);$")

TABLE_CONFIG = {
    "Faculties": {
        "model": ("common", "Faculties"),
        "fields": ["faculty_id", "faculty_name"],
        "source_order": [0, 1],
    },
    "Departments": {
        "model": ("common", "Departments"),
        "fields": ["department_id", "department_name", "faculty_id"],
        "source_order": [0, 1, 2],
    },
    "Classrooms": {
        "model": ("common", "Classrooms"),
        "fields": ["classroom_id", "room_number", "building_name", "capacity"],
        "source_order": [0, 1, 2, 3],
    },
    "Instructors": {
        "model": ("instructors", "Instructors"),
        "fields": [
            "instructor_id",
            "first_name",
            "last_name",
            "date_of_birth",
            "email",
            "phone_number",
            "title",
            "office",
            "department_id",
        ],
        "source_order": [0, 1, 2, 6, 3, 4, 8, 7, 5],
    },
    "Courses": {
        "model": ("common", "Courses"),
        "fields": [
            "course_id",
            "course_name",
            "credits",
            "department_id",
            "instructor_id",
            "semester",
            "course_code",
        ],
        "source_order": [0, 1, 4, 6, 5, 3, 2],
    },
    "Students": {
        "model": ("students", "Students"),
        "fields": [
            "student_id",
            "first_name",
            "last_name",
            "date_of_birth",
            "email",
            "phone_number",
            "identity_no",
            "class_level",
            "status",
            "student_number",
            "department_id",
        ],
        "source_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9],
    },
    "Schedules": {
        "model": ("common", "Schedules"),
        "fields": [
            "schedule_id",
            "course_id",
            "classroom_id",
            "day_of_week",
            "start_time",
            "end_time",
        ],
        "source_order": [0, 5, 4, 1, 2, 3],
    },
    "Announcements": {
        "model": ("common", "Announcements"),
        "fields": [
            "announcement_id",
            "title",
            "message",
            "course_id",
            "instructor_id",
            "created_at",
        ],
        "source_order": [0, 1, 2, 4, 5, 3],
    },
    "Enrollments": {
        "model": ("students", "Enrollments"),
        "fields": ["enrollment_id", "student_id", "course_id", "enrollment_date"],
        "source_order": [0, 3, 2, 1],
    },
    "Grades": {
        "model": ("students", "Grades"),
        "fields": ["grade_id", "enrollment_id", "midterm", "final"],
        "source_order": [0, 1, 3, 2],
    },
    "Users": {
        "model": ("accounts", "Users"),
        "fields": ["user_id", "username", "password_hash", "role", "student_id", "instructor_id"],
        "source_order": [0, 1, 2, 3, 5, 4],
    },
}


def _split_rows(values_text: str):
    rows = []
    depth = 0
    in_string = False
    start_index = None

    for index, character in enumerate(values_text):
        if character == "'":
            if index == 0 or values_text[index - 1] != "\\":
                in_string = not in_string
        elif character == "(" and not in_string:
            if depth == 0:
                start_index = index
            depth += 1
        elif character == ")" and not in_string:
            depth -= 1
            if depth == 0 and start_index is not None:
                rows.append(values_text[start_index:index + 1])

    return rows


def _parse_row(row_text: str):
    return literal_eval(row_text.replace("NULL", "None"))


def _coerce_value(field_name: str, value):
    if value is None:
        return None

    if field_name in {"date_of_birth", "enrollment_date"}:
        return date.fromisoformat(value)

    if field_name == "created_at":
        return datetime.fromisoformat(value).replace(tzinfo=datetime_timezone.utc)

    return value


def _seed_table(apps, table_name: str, rows):
    config = TABLE_CONFIG[table_name]
    model_app_label, model_name = config["model"]
    model = apps.get_model(model_app_label, model_name)
    field_names = config["fields"]
    source_order = config["source_order"]

    instances = []
    for row in rows:
        mapped_values = {}
        for field_name, source_index in zip(field_names, source_order):
            mapped_values[field_name] = _coerce_value(field_name, row[source_index])
        instances.append(model(**mapped_values))

    model.objects.bulk_create(instances, batch_size=500, ignore_conflicts=True)


def load_dump_data(apps, schema_editor):
    dump_path = Path(settings.BASE_DIR) / "Dump20260515.sql"
    if not dump_path.exists():
        raise RuntimeError(f"SQL dump not found: {dump_path}")

    parsed_rows = {table_name: [] for table_name in TABLE_CONFIG}

    with dump_path.open("r", encoding="utf-8") as dump_file:
        for line in dump_file:
            match = INSERT_RE.match(line.strip())
            if not match:
                continue

            table_name = match.group("table")
            if table_name not in TABLE_CONFIG:
                continue

            values_text = match.group("values")
            for row_text in _split_rows(values_text):
                parsed_rows[table_name].append(_parse_row(row_text))

    for table_name in [
        "Faculties",
        "Departments",
        "Instructors",
        "Classrooms",
        "Courses",
        "Students",
        "Schedules",
        "Announcements",
        "Enrollments",
        "Grades",
        "Users",
    ]:
        _seed_table(apps, table_name, parsed_rows[table_name])


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_users_user_id"),
        ("common", "0008_announcements"),
        ("instructors", "0002_instructors_date_of_birth_instructors_office_and_more"),
        ("students", "0008_students_student_number"),
    ]

    operations = [
        migrations.RunPython(load_dump_data, migrations.RunPython.noop),
    ]