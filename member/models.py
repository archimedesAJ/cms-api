from django.db import models
import random
import string

# Create your models here.
class Member(models.Model):
    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female'),
    ]
    
    member_no = models.CharField(max_length=8, unique=True, editable=False)
    title = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    birthday = models.DateField()
    contact_no = models.CharField(max_length=11)
    image = models.ImageField(upload_to='photos/members_photo/', blank=True, null=True)
    location = models.CharField(max_length=100)
    committee = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=20)


    def save(self, *args, **kwargs):
        if not self.member_no:
            self.member_no = self.generate_member_number()
        super().save(*args, **kwargs)

    
    def generate_member_number(self):
        prefix = "ACI-"
        random_digits = ''.join(random.choices(string.digits, k=4))
        return prefix + random_digits

    def __str__(self):
        return self.full_name