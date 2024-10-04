from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings

# Encryption setup
cipher_suite = Fernet(settings.ENCRYPTION_KEY)

def encrypt_mobile_number(mobile_number):
    return cipher_suite.encrypt(mobile_number.encode()).decode()

def decrypt_mobile_number(encrypted_mobile_number):
    return cipher_suite.decrypt(encrypted_mobile_number.encode()).decode()

class Patient(models.Model):
    patient_id = models.CharField(max_length=100)  # Removed unique=True
    patient_name = models.CharField(max_length=255)
    patient_gender = models.CharField(max_length=10)
    patient_age = models.IntegerField()
    mobile_number = models.CharField(max_length=255)  # Encrypted
    center = models.CharField(max_length=255)
    visit_date = models.DateField()
    doctor_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    ip_advised = models.BooleanField(default=False)
    medications = models.TextField(null=True, blank=True)
    investigations = models.TextField(null=True, blank=True)
    diagnosis_advised = models.TextField(null=True, blank=True)
    appointment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.patient_name} ({self.patient_id})'

    def get_decrypted_mobile_number(self):
        return decrypt_mobile_number(self.mobile_number)

class MedicalTest(models.Model):
    patient = models.ForeignKey(Patient, related_name="medical_tests", on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    test_value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.test_name} for {self.patient.patient_name}'
