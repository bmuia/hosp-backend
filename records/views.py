from rest_framework import generics, status
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated
from .serializers import PatientRecordSerializer
from accounts.permissions import IsDoctorUser
from .models import PatientRecord

class PatientRecordView(generics.ListCreateAPIView):
    queryset = PatientRecord.objects.all()
    serializer_class = PatientRecordSerializer
    permission_classes = [IsAuthenticated, IsDoctorUser]

    def post(self, request, *args, **kwargs):
        if request.user.roles != 'doctor':
            return Response({'error': 'Only doctors can access this resource'}, status=status.HTTP_401_UNAUTHORIZED)
        return self.create(request, *args, **kwargs)
