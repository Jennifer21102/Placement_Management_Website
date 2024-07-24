import email
from enum import unique
from tkinter.font import nametofont
from unittest.util import _MAX_LENGTH
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
# Create your models here.
class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    logo = models.ImageField(upload_to ='app1/static/images', default='app1/static/images/')
    spock_name = models.CharField(max_length=64)
    spock_email = models.EmailField(max_length=254)
    spock_phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    username = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200) 
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.password.startswith('bcrypt$$'):
            self.password = make_password(self.password, hasher="bcrypt")
        super().save(*args, **kwargs)
        
class Offer(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="Offers")
    designation = models.CharField(max_length=64)
    no_of_vaccancies = models.IntegerField()
    job_type = models.CharField(max_length=10)
    mode_of_work = models.CharField(max_length=16)
    qualifications = models.CharField(max_length=64)
    year_of_graduation =  models.IntegerField()
    discipline_required = models.CharField(max_length=64)
    eligibility = models.CharField(max_length=64)
    bond_contract = models.CharField(max_length=64)
    ctc_pa = models.CharField(max_length=8)
    last_date = models.DateField()
    shortlist = models.BooleanField()
    written_test = models.BooleanField()
    gd = models.BooleanField()
    interview = models.BooleanField()
    no_of_rounds = models.IntegerField()
    extra_comments = models.CharField(max_length=16)
    def __str__(self):
        return self.designation

class Student(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    register_no = models.CharField(max_length=8)
    phone_no = models.CharField(validators=[phone_regex], max_length=17, blank=True) 
    gender = models.CharField(max_length=8)
    year_of_graduation = models.IntegerField()
    combination = models.CharField(max_length=8)
    marks10th = models.IntegerField()
    marks12th = models.IntegerField()
    dob = models.DateField()
    username = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name 

    def save(self, *args, **kwargs):
        if not self.password.startswith('bcrypt$$'):
            self.password = make_password(self.password, hasher="bcrypt")
        super().save(*args, **kwargs)    

class Application(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="Application")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="Application")
    status = models.IntegerField(default=1)
    resume = models.FileField(upload_to='app1/static/student-resume/')
    aggregate = models.IntegerField()
    def __str__(self):
        return str(self.id)


