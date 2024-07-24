

from django.utils import timezone
import os
from django.shortcuts import render,redirect
from django.http import HttpResponse
from app1.models import Application, Company, Offer, Student
from django.contrib.auth.hashers import check_password
from app1.authentication import create_access_token,decode_access_token
from django.conf import settings
from django.db.models import Q
# Create your views here.
def home (request):
    return render(request,'homepage.html')

def slogin(request):
    token = request.COOKIES.get("access_token")
    if token:
        payload = decode_access_token(token)
        if payload:
            if payload["account_type"] == "Student":
                return redirect('/student')
            if payload["account_type"] == "Company":
                return redirect('/company')
    if request.method == "POST":
        usn=request.POST.get("username")
        pwd=request.POST.get("password")
        students = Student.objects.filter(username=usn)
        if len(students) > 0:
            s=students[0]
            if check_password(pwd, s.password):
                token = create_access_token(usn,'Student')
                response = redirect('/student/')
                response.set_cookie('access_token',token,60*60, httponly=True)
                return response
            else:
                print("Wrong Password")
                return render(request,'Studentlogin.html',{'flag_login': False})
        else:
            print("User is not registered")
            return render(request,'Studentlogin.html',{'flag_login': False})

    elif request.method  == "GET":
        if request.session.get("invalid_session"):
            request.session.pop("invalid_session")
            return render(request,'Studentlogin.html',{'flag_session':False})
        return render(request,'Studentlogin.html')

def clogin(request):
    token = request.COOKIES.get("access_token")
    if token:
        payload = decode_access_token(token)
        if payload:
            if payload["account_type"] == "Student":
                return redirect('/student')
            if payload["account_type"] == "Company":
                return redirect('/company')

    if request.method == "POST":
        usn=request.POST.get("username")
        pwd=request.POST.get("password")
        print(usn, pwd)
        companys = Company.objects.filter(username=usn)
        if len(companys) > 0:
            c=companys[0]
            if check_password(pwd, c.password): 
                token = create_access_token(usn,'Company')
                response = redirect('/company/')
                response.set_cookie('access_token',token,60*60, httponly=True)
                return response
            else:
                print("Wrong Password")
                return render(request,'Companylogin.html',{'flag_login': False})
        else:
            print("User is not registered")
            return render(request,'Companylogin.html',{'flag_login': False})
    elif request.method  == "GET":
        if request.session.get("invalid_session"):
            request.session.pop("invalid_session")
            return render(request,'Companylogin.html',{'flag_session':False})
        return render(request,'Companylogin.html')

def shp(request):
    token = request.COOKIES.get("access_token")
    if not token:
        request.session['invalid_session'] = True
        return redirect('/studentlogin')
    payload = decode_access_token(token)
    if not payload:
        request.session['invalid_session'] = True
        return redirect('/studentlogin')
    if payload['account_type'] == "Company":
        return redirect('/company')
    if payload['account_type'] == "Student":
        if request.method == "GET":
            usn = payload['username']
            student_applications = Application.objects.filter(student__username=usn)
            status = {1:"Pending",2:"Accepted",3:"Rejected"}
            if request.session.get("successful_application"):
                request.session.pop("successful_application")
                return render(request,'shp.html',{'applications':student_applications,'flag_app':bool(len(student_applications)>0),'flag_app_success':True,'status':status})
            return render(request,'shp.html',{'applications':student_applications,'flag_app':bool(len(student_applications)>0),'status':status})

def chp(request):
    token = request.COOKIES.get("access_token")
    if not token:
        request.session['invalid_session'] = True
        return redirect('/companylogin')
    payload = decode_access_token(token)
    if not payload:
        request.session['invalid_session'] = True
        return redirect('/companylogin')
    if payload['account_type'] == "Student":
        return redirect('/student')
    if payload['account_type'] == "Company":
        if request.method == "POST":
            if request.POST.get("accept"):
                application_id = request.POST.get("accept")
                application = Application.objects.filter(id=application_id).update(status=2)
                return redirect(chp)
            if request.POST.get("reject"):
                application_id = request.POST.get("reject")
                application = Application.objects.filter(id=application_id).update(status=3)
                return redirect(chp)
        if request.method == "GET":
            usn = payload['username']
            company = Company.objects.get(username=usn)
            offers = Offer.objects.filter(company=company)
            applications = Application.objects.filter(offer__company=company)
            status = {1:"Pending",2:"Accepted",3:"Rejected"}
            return render(request,'CompanyPage.html', {"company": company, "offers": offers, "applications": applications,'status':status})

def company(request):
    token = request.COOKIES.get("access_token")
    if not token:
        request.session['invalid_session'] = True
        return redirect('/studentlogin')
    payload = decode_access_token(token)
    if not payload:
        request.session['invalid_session'] = True
        return redirect('/studentlogin')
    if payload['account_type'] == "Company":
        return redirect('/company')
    if payload['account_type'] == "Student":
        if request.method == "GET":
            companies = Company.objects.all()
            company_with_offers = []
            for company in companies:
                offers = Offer.objects.filter(company__id=company.id,last_date__gt = timezone.now())
                if len(offers) > 0:
                    company_with_offers.append(company)
            return render(request,'Register.html',{'companys':company_with_offers})

def offerdets(request, offer_id):
    token = request.COOKIES.get("access_token")
    if not token:
        request.session['invalid_session'] = True
        return redirect('/studentlogin')
    payload = decode_access_token(token)
    if not payload:
        request.session['invalid_session'] = True
        return redirect('/studentlogin')
    if payload['account_type'] == "Company":
        return redirect('/company')
    if payload['account_type'] == "Student":
        if request.method == "GET":
            offer = Offer.objects.filter(id=offer_id,)[0]
            if request.session.get('invalid_combination'):
                request.session.pop('invalid_combination')
                return render(request,'CompanyDetails.html',{"offer":offer,'flag_comb':False})
            if request.session.get('invalid_year'):
                request.session.pop('invalid_year')
                return render(request,'CompanyDetails.html',{"offer":offer,'flag_year':False})
            if request.session.get('invalid_applied'):
                request.session.pop('invalid_applied')
                return render(request,'CompanyDetails.html',{"offer":offer,'flag_applied':False})
            if request.session.get('invalid_duedate'):
                request.session.pop('invalid_duedate')
                return render(request,'CompanyDetails.html',{"offer":offer,'flag_duedate':False})
            return render(request,'CompanyDetails.html',{"offer":offer})

def application(request, offer_id):
    token = request.COOKIES.get("access_token")
    if not token:
        request.session['invalid_session'] = True
        return redirect('/studentlogin')
    payload = decode_access_token(token)
    if not payload:
        request.session['invalid_session'] = True
        return redirect('/studentlogin')
    if payload['account_type'] == "Company":
        return redirect('/company')
    if payload['account_type'] == "Student":
        usn = payload['username']
        # now = timezone.now()
        student = Student.objects.get(username=usn)
        offer = Offer.objects.get(id=offer_id,last_date__gt = timezone.now())
        appl = Application.objects.filter(offer=offer,student=student)
        if len(appl) > 0:
            request.session['invalid_applied'] = True
            return redirect(offerdets, offer_id)
        if request.method == "POST":
            agr=request.POST.get("aggregate")
            file_name = request.FILES['resume'].name
            with open(os.path.join(settings.BASE_DIR, 'app1','static','student-resume',file_name), 'wb+') as destination:
                for chunk in request.FILES['resume'].chunks():
                    destination.write(chunk)
            resume=f'app1/static/student-resume/{file_name}'
            Appl = Application(student=student,offer=offer,aggregate=agr,resume=resume)
            Appl.save()
            request.session['successful_application'] = True
            return redirect(shp)
        if request.method == "GET":
            if student.combination not in offer.discipline_required.split(','):
                request.session['invalid_combination'] = True
                return redirect(offerdets, offer_id)
            if student.year_of_graduation != offer.year_of_graduation:
                request.session['invalid_year'] = True
                return redirect(offerdets, offer_id)
           
            return render(request,'registrationform.html')

def offers(request,company_id): 
    token = request.COOKIES.get("access_token")
    if not token:
        request.session['invalid_session'] = True
        return redirect('/studentlogin')
    payload = decode_access_token(token)
    if not payload:
        request.session['invalid_session'] = True
        return redirect('/studentlogin')
    if payload['account_type'] == "Company":
        return redirect('/company')
    if payload['account_type'] == "Student":
        if request.method == "GET":
            offers = Offer.objects.filter(company__id=company_id,last_date__gt = timezone.now())
            image_url = str(offers[0].company.logo)
            return render(request,'Offers.html',{"company_id": company_id,"offers":offers,"image_url":image_url})

def logout(request):
    response = redirect(home)
    if request.COOKIES.get('access_token'):
        response.delete_cookie('access_token')
    return response