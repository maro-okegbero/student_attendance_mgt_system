import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .utils import generate_reference_number
from cloudinary.models import CloudinaryField


def update_filename(instance, filename):
    path = "faces/"
    print(instance.first_name, "Firstname", instance.mat_number, "mat", filename)
    format = instance.first_name + instance.mat_number + filename
    return os.path.join(path, format)


# add otp for lecturers to use in the case when the facial recognition does not work
class User(AbstractUser):
    """
    The user model
    """

    class Gender(models.TextChoices):
        Male = "Male"
        Female = "Female"

    class Title(models.TextChoices):
        Mrs = "Mrs"
        Mr = "Mr"
        Dr_Mrs = "Dr(Mrs)"
        Dr = "Dr"
        Prof = "Prof"
        Prof_Mrs = "Prof(Mrs)"

    phone_number = models.CharField(null=True, blank=True, unique=True, max_length=14)
    gender = models.CharField(max_length=100, blank=True, null=True, choices=Gender.choices)
    title = models.CharField(max_length=100, blank=False, null=True, choices=Title.choices)
    staff_id = models.CharField(max_length=6, blank=True, null=True, default=generate_reference_number())
    mat_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to=update_filename)
    student = models.BooleanField(default=True)
    is_student = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name


class Course(models.Model):
    """
    model for
    """
    title = models.CharField(max_length=200, blank=True, unique=True)
    course_code = models.CharField(max_length=200, blank=True, unique=True)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    students = models.ManyToManyField(User, related_name="students_registered_for_the_course")

    def __str__(self):
        return self.title


class AttendanceRecord(models.Model):
    """
    Attendance model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=False)
    login = models.DateTimeField(null=False, blank=True)
    logout = models.DateTimeField(null=False, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)
