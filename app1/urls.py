from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('studentlogin/',views.slogin),
    path('logout/',views.logout),
    path('companylogin/',views.clogin),
    path('student/',views.shp),
    path('company/',views.chp),
    path('student/companies/',views.company),
    path('student/offers/<int:offer_id>',views.offerdets, name='offersdets'),
    path('student/apply/<int:offer_id>',views.application),
    path('student/companies/<int:company_id>/offers',views.offers),
    
    
]