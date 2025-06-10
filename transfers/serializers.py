from rest_framework import serializers
from .models import DataAccessRequest
from accounts.models import Hospital
from records.models import PatientRecord
from django.contrib.auth import get_user_model
from records.serializers import PatientRecordSerializer

User = get_user_model()

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

class TransferRequestSerializer(serializers.ModelSerializer):
    from_hospital = HospitalSerializer(read_only=True)
    to_hospital = HospitalSerializer(read_only=True)
    patient = UserSerializer(read_only=True)
    request_by = UserSerializer(read_only=True)
    record = PatientRecordSerializer(read_only=True)

    class Meta:
        model = DataAccessRequest
        fields = '__all__'
