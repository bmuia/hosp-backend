from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GetCurrentUserSerializer,RegisterSerializer, HospitalSerializer,CustomObtainPairSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.
class GetCurrentUserView(APIView):
    
    def get(self,request):
        serializer = GetCurrentUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RegisterNewUser(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


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
    
