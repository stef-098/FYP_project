from .models import login, admissionClass
from django import forms
from django.contrib.postgres.fields import ArrayField
import re


class loginUser(forms.Form):
    input_username = forms.CharField(max_length=30, required=True)
    

    class Meta:
        model = login

class otpForm(forms.Form):
    otp = forms.IntegerField()
    
class searchForm(forms.Form):
    search_item = forms.CharField(max_length=11)
    

class patientRegister(forms.Form):
    patient_id = forms.CharField(max_length=10)
    fname = forms.CharField(max_length=30)
    lname = forms.CharField(max_length=30)
    gender = forms.CharField(max_length=1)
    age = forms.IntegerField()
    phone_number = forms.CharField(max_length=12)
    email = forms.EmailField(max_length=50)
    dob = forms.CharField(max_length=30)
    ic = forms.CharField(max_length=30)
    address = forms.CharField(max_length=100)
    nationality = forms.CharField(max_length=50)
    name_emergency = forms.CharField(max_length=50)
    emergency_number = forms.CharField(max_length=12)
    


class vitalSignForm(forms.Form):
    patient_id = forms.CharField(max_length=10)
    temperature = forms.DecimalField(max_digits=5, decimal_places=2)
    weight = forms.DecimalField(max_digits=5, decimal_places = 2)
    respiratory = forms.IntegerField()
    systolic = forms.IntegerField()
    diastolic = forms.IntegerField()
    pulse = forms.IntegerField()

class admissionForm(forms.Form):
    VISIT_TYPES = (
        ('IPD', 'IPD'),
        ('OPD', 'OPD'),
    )
    patient_id = forms.CharField(max_length=10)
    doctor_name = forms.CharField(max_length=50)
    physician_name = forms.CharField(max_length=50)
    department = forms.CharField(max_length=30)
    visit_type = forms.ChoiceField(choices=VISIT_TYPES)
    room_no = forms.CharField(max_length=3, required=False)


class billForm(forms.Form):
    patient_id = forms.CharField(max_length=10)
    room_fee = forms.DecimalField(max_digits=7, decimal_places=2)
    pharmacy_charges = forms.DecimalField(max_digits=7, decimal_places=2)
    doctor_fee = forms.DecimalField(max_digits=7, decimal_places=2)
    credit_card = forms.CharField()

class treatmentPlanForm(forms.Form):
    patient_id = forms.CharField(max_length=10)
    diagnosis = forms.CharField(max_length=400)
    duration = forms.IntegerField()
    duration_unit = forms.CharField(max_length=5)
    medication_name = forms.CharField(max_length=100)
    prescription = forms.DecimalField(max_digits = 5, decimal_places = 2)
    plan_description = forms.CharField(max_length=400)
    additional_note = forms.CharField(max_length=400)

class medicalRecordForm(forms.Form):
    patient_id = forms.CharField(max_length=10)
    surgery_list = forms.CharField(max_length=50)
    surgery_year = forms.CharField(max_length=4)
    allergies = forms.CharField(max_length=50)
    

class signupForm(forms.Form):
    patient_id = forms.CharField(max_length=10)
    username = forms.CharField(max_length=30)
    