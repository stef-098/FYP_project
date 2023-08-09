from django.shortcuts import render, redirect
from .forms import loginUser, patientRegister, searchForm, vitalSignForm, admissionForm, billForm, medicalRecordForm, treatmentPlanForm, signupForm, otpForm
from .models import PatientUser, billClass, ReceptionistUser, vitalSignClass, admissionClass, DoctorUser, treatmentPlanClass, medicalRecordClass, NurseUser, attendingPhysicianUser, otp_num, PatientAcc
from django.contrib import messages
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from cryptography.fernet import Fernet
from .models import login
import secrets
import smtplib

from django.db.models import Q
import os

# assign the key from a file named 'encryption_key.bin'
key_file = 'encryption_key.bin'  
if os.path.exists(key_file):
# read the file with binary mode 
    with open(key_file, 'rb') as file:
        key = file.read()

# implement fernet for symmetric encryption so that dat acannot be mainpulated or read without the key
enc_fun = Fernet(key)

# encryption function using utf-8 as its encoding system
def encryption(var1):
    data = var1.encode('utf-8')
    variable = enc_fun.encrypt(data)
    return variable

#decrption function
def decryption(var):
    data = enc_fun.decrypt(var)
    decrypted = data.decode('utf-8')
    return decrypted



def generating_OTP():
    otp = ''.join(str(secrets.randbelow(10)) for _ in range(6))
    return otp

def send_otp_email(email, otp):
    # Set the STMP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    #set the sender's email and the password for the OTP service in gmail
    sender_email = "stefaniefelicia1004@gmail.com"
    sender_password = "rjun btih odcl kbhw"

    #create secure connection to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    #create the email
    subject = "Verification to login into your patient account"
    body = f"Your OTP is: {otp}"
    message = f"Subject: {subject}\n\n{body}"

    #send the email to the recipient
    server.sendmail(sender_email, email, message)

    #close server connection
    server.quit()

#fucntion for patient signup account
@csrf_protect
def SignUp(request):
    if request.method == 'POST':
        form = signupForm(request.POST) 
        if form.is_valid():
            print("valid")
            # if the form is valid, then the fields will be assigned to a variable 
            patient_id = form.cleaned_data['patient_id']
            username = form.cleaned_data['username']
            try: 
                # checks if the patient id that is inputted in the form exist in the database
                exist = PatientUser.objects.get(patient_id=patient_id)
            # if the patient is not found in the database, then an error message will appear in the admin panel
            except PatientUser.DoesNotExist: 
                messages.error(request, "Patient doesn't exist!")
            try:
                # checks of the patient already has an account in the database
                existing_account = PatientAcc.objects.get(patient_id=patient_id)
            # if the patient already has an account, then an error message will appear in the admin panel
            except PatientAcc.DoesNotExist:
                    messages.error(request, "User already has an account!")
            # if the user has an valid patinet id and doesn't have an account yet, then a new account will be created and user will be redirected into the login page
            PatientAcc.objects.create(patient_id=exist, username=username)
            return redirect('login')
        else:
            form = signupForm()
            messages.error(request, "Invalid input!")
    return render(request, "signup_patient.html")

@csrf_protect
def logIn(request):
    if request.method == 'POST':
        form = loginUser(request.POST)
        if form.is_valid():
             # if the form is valid, then the fields will be assigned to the input_username variable 
            input_username = form.cleaned_data['input_username'] 
            # checks if the inputted username starts with the letter 'D' and if the length of the username is 10
            if input_username[0] == "D" and len(input_username) == 10:
                try: 
                    # checks if the user exist in the doctor database
                    user = DoctorUser.objects.get(doctor_id=input_username)
                    # if the user exist in the database, then it will create a new login object into the database adn redirect user to otp page
                    login.objects.create(input_username=input_username)
                    return redirect('otp')
                # if doctor username doesn't exist in doctor database 
                except DoctorUser.DoesNotExist: 
                    messages.error(request, "Doctor is not registered in the system!")

            # checks if the inputted username starts with the letter 'P' and if the length of the username is 10
            elif input_username [0] == 'P' and len(input_username) == 10:
                try: 
                    # checks if the user exist in the attending physician database
                    user = attendingPhysicianUser.objects.get(physician_id=input_username)
                    # if the user exist in the database, then it will create a new login object into the database and redirect user to otp page
                    login.objects.create(input_username=input_username)
                    return redirect('otp')
                # if the username doesn't exist in attending physician database 
                except attendingPhysicianUser.DoesNotExist: 
                    messages.error(request, "Attending physician is not registered in the system!")

            # checks if the inputted username starts with the letter 'N' and if the length of the username is 10
            elif input_username[0] == "N" and len(input_username) == 10:
                try:
                    # checks if the user exist in the nurse database
                    user = NurseUser.objects.get(nurse_id=input_username)
                    # if the user exist in the database, then it will create a new login object into the database and redirect user to otp page
                    login.objects.create(input_username=input_username)
                    return redirect('otp')
                # if the username doesn't exist in nurse database 
                except NurseUser.DoesNotExist: 
                    messages.error(request, "Nurse is not registered in the system!")

             # checks if the inputted username starts with the letter 'R' and if the length of the username is 10
            elif input_username[0] == "R" and len(input_username) == 10:
                try:
                    # checks if the user exist in the receptionist database
                    user = ReceptionistUser.objects.get(receptionist_id=input_username)
                    # if the user exist in the database, then it will create a new login object into the database and redirect user to otp page
                    login.objects.create(input_username=input_username)
                    return redirect('otp')
                # if the username doesn't exist in receptionist database 
                except ReceptionistUser.DoesNotExist: 
                    messages.error(request, "Receptionist is not registered in the system!")
            else: 
                try: 
                    # checks if the user exist in the patient account database
                    user = PatientAcc.objects.get(username=input_username)
                    # if the user exist in the database, then it will create a new login object into the database and redirect user to otp page
                    login.objects.create(input_username=input_username)
                    return redirect('otp')
                # if the username doesn't exist in patient account database 
                except PatientAcc.DoesNotExist:
                    messages.error(request, "Patient is not registered in the system!")
    return render(request, "login.html")




#function for the otp page
@csrf_protect
def otp(request):
    #get the last object of the login object in the database
    search = login.objects.last()
    #assign the user_type to ''
    user_type = ""
    # checks if the last login object's username starts with the letter 'D' and if the length of the username is 10 
    if search.input_username[0] == "D" and len(search.input_username) == 10:
        # get the doctor object based on the id
        user = DoctorUser.objects.get(doctor_id=search.input_username)
        # assign the object's email to mail variable
        mail = user.email
        #assign user type to doctor
        user_type = "doctor"

    # checks if the last login object's username starts with the letter 'P' and if the length of the username is 10 
    elif search.input_username [0] == 'P' and len(search.input_username) == 10: 
        # get the attending physician object based on the id
        user = attendingPhysicianUser.objects.get(physician_id=search.input_username)
        # assign the object's email to mail variable
        mail = user.email
        #assign user type to attending physician
        user_type = "physician"

    # checks if the last login object's username starts with the letter 'N' and if the length of the username is 10 
    elif search.input_username[0] == "N" and len(search.input_username) == 10:
        # get the nurse object based on the id
        user = NurseUser.objects.get(nurse_id=search.input_username)
        # assign the object's email to mail variable
        mail = user.email
        #assign user type to nurse
        user_type = "nurse"

    # checks if the last login object's username starts with the letter 'R' and if the length of the username is 10 
    elif search.input_username[0] == "R" and len(search.input_username) == 10:
        # get the receptionist object based on the id
        user = ReceptionistUser.objects.get(receptionist_id=search.input_username)
        # assign the object's email to mail variable
        mail = user.email
        #assign user type to receptionist
        user_type = "receptionist"
    else: 
        # get the patinet account object based on the id
        user = PatientAcc.objects.get(username=search.input_username)
        # get the patient id
        search = user.patient_id
        # get the patient object based on patient id
        search_email = PatientUser.objects.get(patient_id=search)
        # assign the object's email to mail variable
        mail = search_email.email
        #assign user type to patient
        user_type = "patient"
        
    if request.method == 'GET':
        #generate OTP
        otp = generating_OTP()
        #send the otp to the user's email
        send_otp_email(mail, otp)
        print(otp)
        #create a new otp object
        otp_num.objects.create(num=otp)

    if request.method == 'POST':
        form = otpForm(request.POST)
        if form.is_valid():
        #if the otp matches the one that is stored in the database, then it will redirect user to login page and deletes the OTP number egnerated from the database 
            otps = form.cleaned_data['otp']
            num = otp_num.objects.last()
            print("inputted value", otps)
            print("database value", num)
         #get the stored OTP from the session
            if num.num == otps:
                num.delete()
                # if the user type is receptionist, then it will redirect the user to the receptionist's homepage
                if user_type == "receptionist":
                    return redirect('homepage-receptionist')
                # if the user type is attending physocian, then it will redirect the user to the attending physician's homepage
                elif user_type == "physician":
                    return redirect('homepage-doctor')
                # if the user type is doctor, then it will redirect the user to the doctor's homepage
                elif user_type == "doctor":
                    return redirect('homepage-doctor')
                # if the user type is nurse, then it will redirect the user to the nurse's homepage
                elif user_type == "nurse":
                    return redirect('homepage-nurse')
                # if the user type is patient, then it will redirect the user to the patient's homepage
                elif user_type == "patient":
                    return redirect('home-patient')   
            else:
                # if the OTP iputted doesn't match the one that is stored in the database, it will show error message and deletes the OTP generated from the database 
                messages.error(request, "invalid OTP")
                num.delete()
        else: 
            # if the form is not valid thsi message will appear in the admin panel
            messages.error(request, "invalid form")
    return render(request, 'otp.html')

#function for logout
def log_out(request):
    return render(request, 'logout.html')

@csrf_protect
# functions for receptionists
#function to register patients
def register_patients(request):
    if request.method == 'POST':
        form = patientRegister(request.POST)
        if form.is_valid(): 
            #if the form is valid, then all of the fields in form will be assigned to a variable which will be saved into the databse 
            patient_id= form.cleaned_data['patient_id']
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            gender = form.cleaned_data['gender']
            age = escape(request.POST['age'])
            phone_number_uncr = escape(request.POST['phone_number'])
            phone_number = encryption(phone_number_uncr)
            email = form.cleaned_data['email']
            dob = form.cleaned_data['dob']    
            ic_uncr = form.cleaned_data['ic']
            ic = encryption(ic_uncr)
            address_uncr = form.cleaned_data['address']
            address = encryption(address_uncr)
            nationality = form.cleaned_data['nationality']
            name_emergency = form.cleaned_data['name_emergency']
            emergency_number_uncr = escape(request.POST['emergency_number'])
            emergency_number = encryption(emergency_number_uncr)
            # then a new patient object will be created
            PatientUser.objects.create(patient_id=patient_id, fname=fname, lname=lname, gender=gender, age=age, phone_number=phone_number, email=email, dob=dob, ic=ic, address=address, nationality=nationality, name_emergency=name_emergency, emergency_number=emergency_number)

        else:
            form = patientRegister()
            #if the input is invalid this message will appear in the admin panel
            messages.error(request, "Registration invalid!")
    return render(request, 'register_pat.html')

#function to display receptionist's homepage
def home(request):
    return render(request, 'home_rcptionist.html')

# function to the search patient for receptionist
@csrf_protect
def search_patient(request):
    form = searchForm(request.GET or None)
    decrypted = []
    found = []
    # when the 
    if request.method == 'GET' and form.is_valid():
        search_item = request.GET['search_item']
        # the search function is based on the searching for patient's full name
        name = search_item.split()
        #split the inputted name into 2, first name and last name
        fname_search = name[0] 
        lname_search = name [1]
        #search the patient by filtering through their first name and last name and assigning it to a variable named found
        found = PatientUser.objects.filter(fname=fname_search, lname=lname_search)
    return render(request, 'search_patient.html', {'found': found})

#function to update an existing patient's information
def update_patient(request):
    if request.method == 'POST':
        form = patientRegister(request.POST)
        if form.is_valid(): 
            #if the form is valid, then all of the fields in form will be assigned to a variable which will be saved into the databse 
            patient_id = form.cleaned_data['patient_id']
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            gender = form.cleaned_data['gender']
            age = escape(request.POST['age'])
            phone_number = escape(request.POST['phone_number'])
            email = form.cleaned_data['email']
            dob = form.cleaned_data['dob']    
            ic = form.cleaned_data['ic']
            address = form.cleaned_data['address']
            nationality = form.cleaned_data['nationality']
            name_emergency = form.cleaned_data['name_emergency']
            emergency_number = escape(request.POST['emergency_number'])
            try: 
                #get the patient data from database and update fields andsave it
                patient = PatientUser.objects.get(patient_id=patient_id)
                patient.fname = fname
                patient.lname = lname
                patient.gender = gender
                patient.age = age
                patient.phone_number = phone_number
                patient.email = email
                patient.dob = dob
                patient.ic = ic
                patient.address = address
                patient.nationality = nationality
                patient.name_emergency = name_emergency
                patient.emergency_number = emergency_number
                patient.save()
            except PatientUser.DoesNotExist: 
                # if patient id doesn't exist then this message will appear in the admin panel
                messages.error(request, "Patient don't exist!")
        else:
            # if form is invalid this message will appear in the admin panel
            form = patientRegister()
            messages.error(request, "Update invalid!")
    return render(request, 'update_patient_info.html')

#function for pAtient admission
@csrf_protect
def admitting_patient(request):
    if request.method == 'POST':
        form = admissionForm(request.POST)
        if form.is_valid(): 
            #if the form is valid, then all of the fields in form will be assigned to a variable which will be saved into the databse 
            patient_id = form.cleaned_data['patient_id']
            doctor_name = form.cleaned_data['doctor_name']
            physician_name = form.cleaned_data['physician_name']
            department = form.cleaned_data['department']
            visit_type = form.cleaned_data['visit_type']
            #if user's visit type is IPD, then the room no variable will be assigned to the value submitted in form
            if visit_type == "IPD":
                print("iPD")
                room_no = str(form.cleaned_data['room_no'])
            else: 
                print("O")
                # if the user's visit type if OPD, then the room no variable will be assigned to not applicable
                room_no = "NA"
            try: 
                #get patient object and change the patient's status to admitted and then create a new admission object 
                patient = PatientUser.objects.get(patient_id=patient_id)
                patient.status = "admitted"
                patient.save()
                admissionClass.objects.create(patient_id=patient, doctor_name=doctor_name, physician_name=physician_name, department=department, visit_type=visit_type, room_no=room_no)
            except PatientUser.DoesNotExist: 
                # if patient doesn't exist in the database, this message will appear in the admin panel
                messages.error(request, "Patient don't exist!")
        else: 
            # if the form is invalid this message appear in teh admin panel
            form = admissionForm()
            messages.error(request, "Admission form invalid!")
    return render(request, 'add_admission.html')

#function to generate new bill
def generate_bills(request):
    if request.method == 'POST':
        form = billForm(request.POST)
        if form.is_valid():
            #if the form is valid, then all of the fields in form will be assigned to a variable which will be saved into the databse 
            patient_id = form.cleaned_data['patient_id']
            room_fee = form.cleaned_data['room_fee']
            pharmacy_charges = form.cleaned_data['pharmacy_charges']
            
            doctor_fee = form.cleaned_data['doctor_fee']
            credit_card_encr = form.cleaned_data['credit_card']
            credit_card = encryption(credit_card_encr)
            # credit_card_unecr = form.cleaned_data['credit_card']
            # credit_card = encryption(credit_card_unecr)
            try: 
                # get patient object from the database and change the status into discharged
                patient = PatientUser.objects.get(patient_id=patient_id)
                patient.status = "discharged"
                patient.save()
                #create a new bill object
                billClass.objects.create(patient_id=patient, room_fee=room_fee, pharmacy_charges=pharmacy_charges, doctor_fee=doctor_fee, credit_card=credit_card)
            # if patient doesn't exist in the patient database, then the message will appear in the admin panel
            except PatientUser.DoesNotExist: 
                messages.error(request, "Patient don't exist!")
        else: 
            # if form is invalid, then the message will appear in the admin panel
            form = billForm()
            messages.error(request, "Bill form invalid!")
            print(form.errors)
    return render(request, 'generate_bills.html')



# functions for nurse
#function for nurse's homepage
def nurse_home(request):
    return render(request, 'nurse_homepage.html')

#function for nurse to search if patient has existing medical record
@csrf_protect
def search_medical_record(request):
    form = searchForm(request.GET or None)
    found = []
    # when the form is valid
    if request.method == 'GET' and form.is_valid():
        # assign the form value to search item variable
        search_item = request.GET['search_item']
        # search from the medical record database if patient has existing medical record by their patient id and then assign it to foudn variable
        found = medicalRecordClass.objects.filter(patient_id=search_item)
        # pass variable into the HTML
    return render(request, 'medical_record_search.html', {'found': found})

#function for nurse to search patient's vital sign
@csrf_protect
def search_vital_sign(request):
    form = searchForm(request.GET or None)
    found = []
    # when the form is valid
    if request.method == 'GET' and form.is_valid():
        # assign the form value to search item variable
        search_item = request.GET['search_item']
        # search the vital sign database based on the patient's id and then assign it to the found variable
        found = vitalSignClass.objects.filter(patient_id=search_item)
        # pass the found variable to the HTML
    return render(request, 'search_vital_sign.html', {'found': found})

#function for nurse to add patient's vital sign
@csrf_protect
def add_vital_sign(request):
    if request.method == 'POST':
        form = vitalSignForm(request.POST)
        # when the form is valid
        if form.is_valid():
            # all of the value from the form will be assigned to variables
            patient_id = form.cleaned_data['patient_id']
            temperature = form.cleaned_data['temperature']
            weight = form.cleaned_data['weight']
            respiratory = form.cleaned_data['respiratory']
            diastolic = form.cleaned_data['diastolic']
            systolic = form.cleaned_data['systolic']
            pulse = form.cleaned_data['pulse']
            try: 
                #checks if patient exist in the databasebased on their id
                patient = PatientUser.objects.get(patient_id=patient_id)
                # create a new vital sign object in databsae if patient exist in the database
                vitalSignClass.objects.create(patient_id=patient, weight=weight, temperature=temperature, respiratory=respiratory, diastolic=diastolic, systolic=systolic, pulse=pulse)
            #if patient doesn't exist in the database, then this message is displayed in the admin panel
            except PatientUser.DoesNotExist: 
                messages.error("Patient don't exist!")
        else: 
            # if form is invalid, then this message will be displayed
            form = vitalSignForm()
            messages.error(request, "Vital sign form invalid!")
    return render(request, 'vital_signs.html')

#function for nurse to add patient's medocal record
@csrf_protect
def add_medical_record(request):
    if request.method == 'POST':
        form = medicalRecordForm(request.POST)
        # when the form is valid
        if form.is_valid():
            # all of the value from the form will be assigned to variables
            patient_id = form.cleaned_data['patient_id']
            surgery_list = form.cleaned_data['surgery_list']
            surgery_year = str(form.cleaned_data['surgery_year']) 
            allergies = form.cleaned_data['allergies']
            try: 
                # checks if patient is registered in the database
                patient = PatientUser.objects.get(patient_id=patient_id)
                # a new medical record object is created if patient is regsitered into the database
                medicalRecordClass.objects.create(patient_id=patient, surgery_list=surgery_list, surgery_year=surgery_year, allergies=allergies)
            # if patient is not registered in the system, then this message will be displayed in the admin panel
            except PatientUser.DoesNotExist: 
                messages.error("Patient don't exist!")
        else: 
            # if invalid form, the message will appear in the admin panel
            form = medicalRecordForm() 
            messages.error(request, "Medical record form invalid!")
    return render(request, 'add_medical_record.html')



# functions for doctors and attending physicians
# homepage for doctors and attending physicians
def home_doctor(request):
    return render(request, 'homepage_doctor.html')

# function to search for patient's medical record
def view_medical_rec(request):
    form = searchForm(request.GET or None)
    found = []
    # when the form is valid
    if request.method == 'GET' and form.is_valid():
        # assign the form value to search item variable
        search_item = request.GET['search_item']
        # search from the medical record database patient's medical record by their patient id and then assign it to foudn variable
        found = medicalRecordClass.objects.filter(patient_id=search_item)
        # pass the variable into the HTML
    return render(request, 'doctor_med_record.html', {'found':found})

# function to search for patient's votal sign
def doctor_vital_sign(request):
    form = searchForm(request.GET or None)
    found = []
    # when the form is valid
    if request.method == 'GET' and form.is_valid():
        search_item = request.GET['search_item']
        # search from the vital sign database bsaed on their patient id and then assign it to found variable
        found = vitalSignClass.objects.filter(patient_id=search_item)
        # pass the variable into the HTML
    return render(request, 'doctr_vital_sign.html', {'found':found})

# function to add patient's treatment plan
@csrf_protect
def add_treatment_plan(request):
    if request.method == 'POST':
        form = treatmentPlanForm(request.POST)
        # when the form is valid
        if form.is_valid():
            #all of the value in the form will be assigned to variables
            patient_id = form.cleaned_data['patient_id']
            diagnosis = form.cleaned_data['diagnosis']
            duration = form.cleaned_data['duration']
            duration_unit = form.cleaned_data['duration_unit']
            medication_name = form.cleaned_data['medication_name']
            prescription = form.cleaned_data['prescription']
            plan_description = form.cleaned_data['plan_description']
            additional_note = form.cleaned_data['additional_note']
            try: 
                # checks if patient exist in the database by their patient id
                patient = PatientUser.objects.get(patient_id=patient_id)
                # create a new treatment plan if patient exist in the database
                treatmentPlanClass.objects.create(patient_id=patient, diagnosis=diagnosis, duration=duration, duration_unit=duration_unit, medication_name=medication_name, prescription=prescription, plan_description=plan_description,additional_note=additional_note)
            # if patient doesn't exist in the database the message will be displayed in admin panel
            except PatientUser.DoesNotExist: 
                messages.error(request, "Patient don't exist!")
        else: 
            # if form is invalid this message will appear in the adin panel
            form = treatmentPlanForm()
            messages.error(request, "Medical record form invalid!")
    return render(request, 'treatment_plans.html')



#functions for patient
# homepage for patient
def homepage_patient(request):
    return render(request, 'view_patient.html')

# view past admission
def past_admission(request):
    # search for latest login object filtered by the input username, it shouldn't start with 'D', 'P', 'R', 'N' and it will be ordered by the their latest login 
    temp = login.objects.filter(~Q(input_username__istartswith='D') & ~Q(input_username__istartswith='P') & ~Q(input_username__istartswith='R') & ~Q(input_username__istartswith='N')).order_by('-login_time').first()
    print(temp)
    # search for the input username in the patient account database
    patient = PatientAcc.objects.get(username=temp)
    print(patient)
    # get the patient id from the patient account database
    pat_id = patient.patient_id
    try: 
        #filter for patient's admission in admission database
        search = admissionClass.objects.filter(patient_id=pat_id)
        # if patient don't have any admission
    except admissionClass.DoesNotExist: 
        messages.error(request, "The patient don't have medical record")
    
    try: 
        #filter for patient's bill in bills database
        bills = billClass.objects.filter(patient_id=pat_id)
        # if patient don't have any bill
    except billClass.DoesNotExist:
        messages.error(request, "The patient don't have any past bills")
    try: 
        #filter for patient's treatment plan in treatment plan database
        plans = treatmentPlanClass.objects.filter(patient_id=pat_id)
        # if patient don't have any treatment plan
    except treatmentPlanClass.DoesNotExist:
        messages.error(request, "The patient don't have any treatment plans!")

    # pass the objects into context variable and then rendered in the HTML
    context = {
        'search': search,
        'bills': bills,
        'plans': plans,
    }
    return render(request, 'past_admission.html', context)

# view medical record
def view_medical_record(request):
    # search for latest login object filtered by the input username, it shouldn't start with 'D', 'P', 'R', 'N' and it will be ordered by the their latest login 
    temp = login.objects.filter(~Q(input_username__istartswith='D') & ~Q(input_username__istartswith='P') & ~Q(input_username__istartswith='R') & ~Q(input_username__istartswith='N')).order_by('-login_time').first()
    print(temp)
    # search for the input username in the patient account database
    patient = PatientAcc.objects.get(username=temp)
    print(patient)
    # get the patient id from the patient account database
    pat_id = patient.patient_id
    try: 
        # filter patient's medical record 
        search = medicalRecordClass.objects.filter(patient_id=pat_id)

    # if patient doesn't have medical record, error message will appear in the admin panel
    except medicalRecordClass.DoesNotExist: 
        messages.error(request, "The patient don't have medical record")
    return render(request, 'patient_medical_info.html',  {'search': search})

# view patient profile 
def patient_profile(request):
    # search for latest login object filtered by the input username, it shouldn't start with 'D', 'P', 'R', 'N' and it will be ordered by the their latest login 
    temp = login.objects.filter(~Q(input_username__istartswith='D') & ~Q(input_username__istartswith='P') & ~Q(input_username__istartswith='R') & ~Q(input_username__istartswith='N')).order_by('-login_time').first()
    print(temp)
    # search for the input username in the patient account database
    patient = PatientAcc.objects.get(username=temp)
    print(patient)
    # get the patient id from the patient account database
    pat_id = patient.patient_id
    try: 
        # filter patient object
        search = PatientUser.objects.filter(patient_id=pat_id)

        # if patient doesn't have medical record, error message will appear in the admin panel
    except PatientUser.DoesNotExist: 
        messages.error(request, "The patient not found")
    return render(request, 'profile_patient.html', {'search': search})
