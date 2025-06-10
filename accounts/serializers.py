from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Hospital # Make sure to import Hospital
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id','name', 'location']
        read_only_fields = ['id']

class GetCurrentUserSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer()

    class Meta:
        model = User
        fields = ['email', 'is_staff', 'hospital','roles'] 


class CreateUserSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'roles', 'first_name', 'last_name', 'hospital_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        roles = validated_data.get('roles')
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        hospital_name = validated_data.pop('hospital_name', None) #

        hospital_instance = None
        if hospital_name:
            try:
                hospital_instance = Hospital.objects.get(name=hospital_name)
            except Hospital.DoesNotExist:
                raise serializers.ValidationError({"hospital_name": "Hospital with this name does not exist."})

        user = User.objects.create_user(
            email=email,
            password=password,
            roles=roles,
            first_name=first_name,
            last_name=last_name,
            hospital=hospital_instance 
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(read_only=True) # Nested serializer to display hospital details

    class Meta:
        model = User
        fields = ['id','first_name','last_name','email', 'is_active','is_staff','roles', 'hospital']
        read_only_fields = ['id']

class CustomObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.roles
        token['email'] = user.email

        if user.hospital:
            token['hospital_id'] = user.hospital.id
            token['hospital_name'] = user.hospital.name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'email': self.user.email,
            'role': self.user.roles,
        }
        if self.user.hospital:
            data['user']['hospital_id'] = self.user.hospital.id
            data['user']['hospital_name'] = self.user.hospital.name
        return data