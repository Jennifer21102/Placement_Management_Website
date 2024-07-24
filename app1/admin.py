from django.contrib import admin
from .models import Application, Company, Offer, Student

# Register your models here.
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(Offer)
admin.site.register(Application)

