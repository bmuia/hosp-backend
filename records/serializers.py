from rest_framework import serializers
from .models import PatientRecord, Prescription
class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'


class PatientRecordSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionSerializer(many=True)  
    class Meta:
        model = PatientRecord
        fields = '__all__'  

    def create(self, validated_data):
        prescriptions_data = validated_data.pop('prescriptions', [])
        record = PatientRecord.objects.create(**validated_data)

        for prescription in prescriptions_data:
            Prescription.objects.create(record=record, **prescription)

        return record

    def update(self, instance, validated_data):
        prescriptions_data = validated_data.pop('prescriptions', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if prescriptions_data is not None:
            instance.prescriptions.all().delete()
            for prescription in prescriptions_data:
                Prescription.objects.create(record=instance, **prescription)

        return instance
