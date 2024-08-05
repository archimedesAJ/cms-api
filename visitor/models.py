from django.db import models

# Create your models here.
class Visitor(models.Model):
    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female'),
    ]

    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    date_visited = models.DateTimeField(auto_now_add=True)
    contact_no = models.CharField(max_length=11)
    location = models.CharField(max_length=100)


    def __str__(self):
        return self.full_name