"""
URL configuration for hospital_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from system import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.logIn, name='login'),
    path ('logout', views.log_out, name='logout'),
    path('homepage-receptionist', views.home, name='homepage-receptionist'),
    path('homepage-receptionist/register_patient', views.register_patients, name='register_patient'),
    path('homepage-receptionist/search_patients', views.search_patient, name='search_patients'),
    path('homepage-receptionist/admit_patient', views.admitting_patient, name='admit_patient'),
    path('homepage-receptionist/generate_bill', views.generate_bills, name='generate_bill'),
    path('homepage-receptionist/update_information', views.update_patient, name='update_information'),
    path('homepage-nurse', views.nurse_home, name='homepage-nurse'),
    path('homepage-nurse/medical_record', views.add_medical_record, name='medical_record'),
    path('homepage-nurse/vital_sign', views.add_vital_sign, name='vital_sign'),
    path('homepage-nurse/search_vital_sign', views.search_vital_sign, name='search_vital_sign'),
    path('homepage-nurse/search_medical_record', views.search_medical_record, name='search_medical_record'),
    path('homepage-doctor', views.home_doctor, name='homepage-doctor'),
    path('homepage-doctor/view_vital_sign', views.doctor_vital_sign, name='view_vital_sign'),
    path('homepage-doctor/view_med_record', views.view_medical_rec, name='view_med_record'),
    path('homepage-doctor/treament_plan', views.add_treatment_plan, name='treatment_plan'),
    path('home-patient', views.homepage_patient, name='home-patient'),
    path('home-patient/view_medical_record', views.view_medical_record, name='view_medical_record'),
    path('home-patient/patient_profile', views.patient_profile, name='patient_profile'),
    path('home-patient/past_admissions', views.past_admission, name='past_admission'),
    path('signup', views.SignUp, name='signup'),
    path('otp', views.otp, name='otp'),

]
