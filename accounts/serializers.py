from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Hospital

User = get_user_model()

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['name', 'location']


class GetCurrentUserSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer()

    class Meta:
        model = User
        fields = ['email', 'is_staff', 'hospital']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password','role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create_user(email=email, password=password)
        return user
