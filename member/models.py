from django.db import models

# Create your models here.
class Member(models.Model):
    member_no = models.CharField(max_length=12)
    title = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10)
    birthday = models.DateField()
    contact_no = models.CharField(max_length=11)
    #image = models.CharField(upload_to='photos/members/', blank=True)
    location = models.CharField(max_length=100)
    committee = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name