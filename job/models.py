from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class StuUser(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=25)
    surname=models.CharField(max_length=25)
    email=models.CharField(max_length=50)
    number=models.CharField(max_length=15)
    gender=models.CharField(max_length=15)
    country=models.CharField(max_length=25) 
    state=models.CharField(max_length=25)
    password=models.CharField(max_length=50)
    Cpassword=models.CharField(max_length=50)
    experience=models.CharField(max_length=250)
    type=models.CharField(max_length=25,default="normalUser")
    def _str_(self):
        return self.user.username
      

# recurater
class recuraterUser(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=25)
    role=models.CharField(max_length=25)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    Cpassword=models.CharField(max_length=50)
    type=models.CharField(max_length=25,null="True")
    status =models.CharField(max_length=20,default='pending')
    def _str_(self):
        return self.name



class DashboardJob(models.Model):
    user = models.ForeignKey(recuraterUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    jobtype = models.CharField(max_length=50)
    salary = models.CharField(max_length=50)
    job_description = models.TextField()
    type = models.CharField(max_length=25, default="dashboad")
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        # return f"{self.title} - {self.user.user.username}"
          return self.user.username

from django.db import models

class applicatioForm(models.Model):
    job_id = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    country_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    experience_level = models.CharField(max_length=20)
    experience_details = models.TextField(blank=True, null=True)
    skills = models.CharField(max_length=100)
    aadhaar = models.FileField(upload_to='aadhaar/', blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    job_role = models.CharField(max_length=100)
    expected_salary = models.PositiveIntegerField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_role}"