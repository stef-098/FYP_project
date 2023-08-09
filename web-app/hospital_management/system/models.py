from django.contrib.postgres.fields import ArrayField
from django.db import models

        
    
class login(models.Model):
    STATUS = (
        ('logged in', 'Logged in'), 
        ('logged out', 'Logged out'),
    )
    VERIFICATION = (
        ('success', 'Success'),
        ('fail', 'Fail'),
    )
    input_username = models.fields.CharField(max_length=30)
    # input_password = models.fields.CharField(max_length=20)
    login_time = models.fields.DateTimeField(auto_now_add=True)
    verification = models.fields.CharField(choices=VERIFICATION, max_length=7, default='success')
    login_stats = models.fields.CharField(max_length=10, default='logged in')
    # logout_time = models.fields.DateTimeField(null=True)

    def __str__(self):
        return f'{self.input_username}'

class otp_num(models.Model):
    num = models.fields.IntegerField(default=0)    
    def __str__(self):
        return f'{self.num}'


class ReceptionistUser(models.Model):
    receptionist_id = models.CharField(primary_key=True, max_length=10)
    given = models.fields.CharField(max_length=30, default='')
    lname = models.fields.CharField(max_length=30)
    email = models.fields.EmailField(max_length=50, default='')
    phone_number = models.fields.CharField(max_length=50)
    


class PatientUser(models.Model):
    PATIENT_STATUS = (
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
    )
    GENDER = (
        ('F', 'F'),
        ('M', 'M'),
    )
    patient_id = models.CharField(primary_key=True, max_length=10)
    fname = models.fields.CharField(max_length=30)
    lname = models.fields.CharField(max_length=30)
    gender = models.fields.CharField(choices=GENDER, max_length=1)
    age = models.fields.IntegerField(default=0)
    phone_number = models.fields.CharField(max_length=200, default='')
    email = models.fields.EmailField(max_length=200, default='')
    dob = models.fields.CharField(max_length=200)
    ic = models.fields.CharField(max_length=200)
    address = models.fields.CharField(max_length=200)
    nationality = models.fields.CharField(max_length=50)
    name_emergency = models.fields.CharField(max_length=50)
    emergency_number = models.fields.CharField(max_length=200, default='')
    status = models.fields.CharField(choices=PATIENT_STATUS, max_length=10, default='discharged')
    date_registered = models.fields.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient_id}'
    
class PatientAcc(models.Model):
    patient_id = models.ForeignKey(PatientUser,on_delete=models.CASCADE)
    username = models.fields.CharField(max_length=30)
    


    
class admissionClass(models.Model):
    VISIT_TYPES = (
        ('IPD', 'IPD'),
        ('OPD', 'OPD'),
    )
    patient_id = models.ForeignKey(PatientUser,on_delete=models.CASCADE)
    datetime = models.fields.DateTimeField(auto_now_add=True)
    doctor_name = models.fields.CharField(max_length=50)
    physician_name = models.fields.CharField(max_length=50)
    department = models.fields.CharField(max_length=30)
    visit_type = models.fields.CharField(choices=VISIT_TYPES, max_length=3)
    room_no = models.fields.CharField(max_length=3, default='')
    admitted_date = models.fields.DateTimeField(auto_now_add=True)


class billClass(models.Model):
    patient_id = models.ForeignKey(PatientUser,on_delete=models.CASCADE)
    room_fee = models.fields.DecimalField(max_digits = 7, decimal_places = 2, default=0.00)
    pharmacy_charges = models.fields.DecimalField(max_digits = 7, decimal_places = 2, default=0.00)
    doctor_fee = models.fields.DecimalField(max_digits = 7, decimal_places = 2, default=0.00)
    credit_card = models.fields.CharField(max_length=150, default='')


class NurseUser(models.Model):
    nurse_id = models.CharField(primary_key=True, max_length=10)
    fname = models.fields.CharField(max_length=30, db_column='fname')
    lname = models.fields.CharField(max_length=30)
    email = models.fields.EmailField(max_length=50, default='')
    phone_number = models.fields.CharField(max_length=50, default='')
    department_nurse = models.CharField(max_length=30, default='')


class medicalRecordClass(models.Model):
    patient_id = models.ForeignKey(PatientUser,on_delete=models.CASCADE)
    surgery_list = models.fields.CharField(max_length=50, default='')
    additional_surgery = models.fields.CharField(max_length=50, null=True, blank=True)
    surgery_year = models.fields.CharField(max_length=4,default='')
    additional_year= models.fields.CharField(max_length=4, null=True, blank=True)
    allergies = models.fields.CharField(max_length=50, default='')
    additional_allergy = models.fields.CharField(max_length=50, null=True, blank=True)
    


class vitalSignClass(models.Model):
    patient_id = models.ForeignKey(PatientUser,on_delete=models.CASCADE)
    temperature = models.fields.DecimalField(max_digits = 5, decimal_places = 2, default=0.00)
    weight = models.fields.DecimalField(max_digits = 5, decimal_places = 2, default=0.00)
    respiratory = models.fields.IntegerField(default=0)
    diastolic = models.fields.IntegerField(default=0)
    systolic = models.fields.IntegerField(default=0)
    pulse = models.fields.IntegerField(default=0)
    datetime_vitalsign = models.fields.DateTimeField(auto_now_add=True)
    #nurse_id = models.ForeignKey(nurseUser,on_delete=models.CASCADE)

class attendingPhysicianUser(models.Model):
    physician_id = models.CharField(primary_key=True, max_length=10)
    fname = models.fields.CharField(max_length=30)
    lname = models.fields.CharField(max_length=30)
    phone_number = models.fields.CharField(max_length=50, default='') 
    email = models.fields.EmailField(max_length=50, default='')
    department_physician = models.fields.CharField(max_length=30, default='')

class DoctorUser(models.Model):
    doctor_id = models.CharField(primary_key=True, max_length=10)
    phone_number = models.fields.CharField(max_length=50, default='')
    fname = models.fields.CharField(max_length=30)
    lname = models.fields.CharField(max_length=30)
    email = models.fields.EmailField(max_length=50)
    department_doctor = models.fields.CharField(max_length=30)
    specialization = models.fields.CharField(max_length = 30) 
    # p = models.fields.CharField(max_length=30, default='')
    # physician_id = models.ForeignKey(attendingPhysicianUser,on_delete=models.CASCADE)


class treatmentPlanClass(models.Model):
    TIME_FIELD = (
        ('day', 'Day'),
        ('month', 'Month'),
        ('year', 'Year')
    )
    patient_id = models.ForeignKey(PatientUser,on_delete=models.CASCADE)
    #physician_id = models.ForeignKey(attendingphysicianUser,on_delete=models.CASCADE)
    diagnosis = models.fields.CharField(max_length=400)
    duration = models.fields.IntegerField(default='0')
    duration_unit = models.fields.CharField(choices=TIME_FIELD, max_length=5)
    plan_description = models.fields.CharField(max_length=400)
    additional_note = models.fields.CharField(max_length=400, default='')
    medication_name = models.fields.CharField(max_length=100, default='')
    prescription = models.fields.DecimalField(max_digits = 5, decimal_places = 2, default=0.00)