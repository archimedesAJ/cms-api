from django.db import models

# Create your models here.
class SundaySchool(models.Model):
    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female'),
    ]

    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    birthday = models.DateField()
    guardian_contact = models.CharField(max_length=11)
    image = models.ImageField(upload_to='photos/sunday_school_photo/', blank=True)
    location = models.CharField(max_length=100)


    def __str__(self):
        return self.full_name
