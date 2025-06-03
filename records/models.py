from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class PatientRecord(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'roles': 'patient'},
        related_name='records'
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'roles': 'doctor'},
        related_name='doctor_records'
    )
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)

    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    notes = models.TextField(blank=True, null=True)
    
    visit_date = models.DateField(auto_now_add=True)
    follow_up_date = models.DateField(blank=True, null=True)

    blood_pressure = models.CharField(max_length=20, blank=True, null=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    pulse_rate = models.PositiveIntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.diagnosis[:30]}"


class Prescription(models.Model):
    record = models.ForeignKey(PatientRecord, on_delete=models.CASCADE, related_name='prescriptions',null=True, blank=True)
    drug_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)  
    frequency = models.CharField(max_length=100)  
    duration = models.CharField(max_length=100)  

    def __str__(self):
        return f"{self.drug_name} ({self.dosage})"
