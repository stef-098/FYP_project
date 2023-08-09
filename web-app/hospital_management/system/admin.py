from django.contrib import admin
from .models import login, ReceptionistUser, DoctorUser, PatientUser, billClass, vitalSignClass, admissionClass, medicalRecordClass, NurseUser, attendingPhysicianUser, otp_num, treatmentPlanClass, PatientAcc

# Register your models here.
class loginAdmin(admin.ModelAdmin):
    list_display = ('input_username', 'verification', 'login_time')

class otpAdmin(admin.ModelAdmin):
    list_display = ['num']

class patientAccountAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'username')

class patientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'fname', 'lname', 'gender', 'age', 'phone_number', 'email', 'dob', 'ic', 'address', 'nationality', 'name_emergency', 'emergency_number', 'status')

class billAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'room_fee', 'pharmacy_charges', 'doctor_fee', 'credit_card')

class admissionAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'datetime', 'doctor_name', 'physician_name', 'department', 'visit_type', 'room_no', 'admitted_date')

class vitalSignAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'temperature', 'pulse', 'weight', 'respiratory', 'systolic', 'diastolic', 'pulse', 'datetime_vitalsign')

class medicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'surgery_list', 'surgery_year', 'allergies')

class doctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'fname', 'lname', 'email', 'phone_number', 'department_doctor', 'specialization')

class physicianAdmin(admin.ModelAdmin):
    list_display = ('physician_id', 'fname', 'lname', 'phone_number', 'email', 'department_physician')

class receptionistAdmin(admin.ModelAdmin):
    list_display = ('receptionist_id', 'given', 'lname', 'email', 'phone_number')

class treatmentPlanAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'diagnosis', 'duration', 'duration_unit', 'medication_name', 'prescription', 'plan_description', 'additional_note')

class nurseAdmin(admin.ModelAdmin):
    list_display = ('nurse_id', 'fname', 'lname', 'email', 'phone_number', 'email')


admin.site.register(login, loginAdmin) 
admin.site.register(otp_num, otpAdmin) 
admin.site.register(PatientUser, patientAdmin)
admin.site.register(PatientAcc, patientAccountAdmin)
admin.site.register(billClass, billAdmin)
admin.site.register(admissionClass, admissionAdmin)
admin.site.register(vitalSignClass, vitalSignAdmin)
admin.site.register(medicalRecordClass, medicalRecordAdmin)
admin.site.register(ReceptionistUser, receptionistAdmin)
admin.site.register(DoctorUser, doctorAdmin)
admin.site.register(attendingPhysicianUser, physicianAdmin)
admin.site.register(NurseUser, nurseAdmin)
admin.site.register(treatmentPlanClass, treatmentPlanAdmin)
