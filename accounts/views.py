from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GetCurrentUserSerializer,RegisterSerializer, HospitalSerializer
from rest_framework.permissions import IsAdminUser
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

class NewHospitalView(generics.CreateAPIView):

    permission_classes = [IsAdminUser]
    serializer_class = HospitalSerializer

    def post(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            hospital = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
