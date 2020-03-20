from django.db import models
from django.contrib.auth.models import User
# from django.contrib.postgres.fields import ArrayField


# Create your models here.

#
# class Usernew(models.Model):
#     username = models.ForeignKey(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=30)
#     authy_id = models.CharField(max_length=200)
class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(max_length=255)
    email=models.EmailField(max_length=200,default="")
    age=models.IntegerField(default=18)
    dob = models.DateField()
    address = models.CharField(max_length=1000)
    contact_no = models.CharField(max_length=13,default='+911234567890')
    gender = models.CharField(max_length=100,choices=(('Male','Male'),('Female','Female')),default='Select')
    fb_link = models.CharField(max_length=1000)
    skills=models.CharField(max_length=1000)
    # twitter_link = models.CharField(max_length=1000)
    # linkedin_link = models.CharField(max_length=1000)

