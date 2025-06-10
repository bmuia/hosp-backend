from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GetCurrentUserSerializer, CreateUserSerializer, HospitalSerializer, CustomObtainPairSerializer, UserSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Hospital
from .permissions import IsDoctorUser
from django.contrib.auth import get_user_model

User = get_user_model()

class GetCurrentUserView(APIView):

    def get(self,request):
        serializer = GetCurrentUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterNewUser(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateUserSerializer 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            if user.roles == 'doctor':
                user.is_staff = True
                user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllUsers(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.exclude(roles='admin')

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomObtainPairSerializer


class NewHospitalView(generics.CreateAPIView):

    permission_classes = [IsAdminUser]
    serializer_class = HospitalSerializer

    def post(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            hospital = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllHospitals(generics.ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAdminUser]

class fetchAllPatients(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsDoctorUser]

    def get_queryset(self):
        return User.objects.filter(roles='patient')

