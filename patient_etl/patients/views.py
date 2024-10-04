import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Patient, MedicalTest
from .forms import UploadFileForm
from django.conf import settings
from cryptography.fernet import Fernet
import os
from datetime import datetime

# Initialize the Fernet cipher suite
cipher_suite = Fernet(settings.ENCRYPTION_KEY)

def encrypt_mobile_number(mobile_number):
    """Encrypts the mobile number using Fernet encryption."""
    return cipher_suite.encrypt(mobile_number.encode()).decode()

def decrypt_mobile_number(encrypted_mobile_number):
    """Decrypts the mobile number using Fernet decryption."""
    return cipher_suite.decrypt(encrypted_mobile_number.encode()).decode()

def convert_date_format(date_str):
    """Convert date from DD/MM/YYYY to YYYY-MM-DD format."""
    try:
        if isinstance(date_str, float) or pd.isna(date_str):
            return None 

        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None  
def convert_yes_no(value):
    """Convert 'Yes'/'No' to True/False."""
    if isinstance(value, str):
        value = value.strip().lower()  
        if value == 'yes':
            return True
        elif value == 'no':
            return False
    return None  

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            
            excel_file = request.FILES['file']

           
            file_extension = os.path.splitext(excel_file.name)[1].lower()

           
            if file_extension == '.csv':
                df = pd.read_csv(excel_file)
            elif file_extension in ['.xls', '.xlsx']:
                df = pd.read_excel(excel_file)
            else:
                return HttpResponse("Invalid file format. Please upload a CSV or Excel file.")

            
            if 'Visit_Date' in df.columns:
                df['Visit_Date'] = df['Visit_Date'].astype(str)
            if 'Appointment_Date' in df.columns:
                df['Appointment_Date'] = df['Appointment_Date'].astype(str)

            
            for _, row in df.iterrows():
                
                patient = Patient(
                    patient_id=row['Patient_ID'],  
                    patient_name=row['Patient_Name'],
                    patient_gender=row['Patient_Gender'],
                    patient_age=row['Patient_Age'],
                    mobile_number=encrypt_mobile_number(str(row['Mobile_Number'])),
                    center=row['Center'],
                    visit_date=convert_date_format(row['Visit_Date']),
                    doctor_name=row['Doctor_Name'],
                    department=row['Department'],
                    ip_advised=convert_yes_no(row['Ip_Advised']),
                    medications=row['Medications'],
                    investigations=row['Investigations'],
                    diagnosis_advised=row['Diagnosis_Advised'],
                    appointment_date=convert_date_format(row['Appointment_Date'])
                )
                
                patient.save()

                
                MedicalTest.objects.create(
                    patient=patient,
                    test_name=row['Test_Name'],
                    test_value=row['Test_Value']
                )

            return redirect('upload_success')

    else:
        form = UploadFileForm()
    return render(request, 'patients/upload.html', {'form': form})

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})

def patient_detail(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    
    medical_tests = patient.medical_tests.all()  
    return render(request, 'patients/patient_detail.html', {'patient': patient, 'medical_tests': medical_tests})

def upload_success(request):
    return render(request, 'patients/upload_success.html')
def home(request):
    return render(request, 'patients/home.html')
