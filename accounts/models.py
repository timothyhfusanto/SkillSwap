from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from django.contrib.auth.models import Group, Permission


class User(AbstractUser):
    ACADEMIC_YEAR = (
        (1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')
    )
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(null=False, blank=False)
    academicYear = models.IntegerField(null=False, blank=False, choices=ACADEMIC_YEAR, default=1)
    major = models.CharField(max_length=100, null=True)
    phoneNum = models.IntegerField(null=False, blank=False)
    image = models.ImageField(upload_to="profile", default='profile/no-image.jpeg')
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'name', 'age', 'academicYear', 'phoneNum', 'major']

    def __str__(self):
        return self.username

    def user_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
