from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from .models import DataAccessRequest
from records.utils import generate_patient_record_json
from accounts.permissions import IsDoctorUser
from django.contrib.auth import get_user_model
from accounts.models import Hospital
from records.models import PatientRecord

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsDoctorUser])
def send_data_access_request(request):
    patient_id = request.data.get('patient_id')
    to_hospital_id = request.data.get('to_hospital_id')

    if not all([patient_id, to_hospital_id]):
        return Response({'error': 'One of the fields is missing'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        patient_user = User.objects.get(id=patient_id, roles='patient')
    except User.DoesNotExist:
        return Response({'error': 'Target patient not found'}, status=status.HTTP_404_NOT_FOUND)

    
    try:
        to_hospital_obj = Hospital.objects.get(id=to_hospital_id)
    except Hospital.DoesNotExist:
        return Response({'error': 'Target hospital not found'}, status=status.HTTP_404_NOT_FOUND)
    
    from_hospital_obj = None
    if hasattr(request.user, 'hospital'): 
        from_hospital_obj = request.user.hospital

    if not from_hospital_obj:
        return Response({'error': 'Could not determine the doctor\'s hospital (from_hospital).'}, status=status.HTTP_400_BAD_REQUEST)
    
    existing_requests = DataAccessRequest.objects.filter(
        patient=patient_user,
        to_hospital=to_hospital_obj,
        from_hospital=from_hospital_obj,
        status='pending'
    ).first()

    if existing_requests:
        return Response({'message': 'A pending request already exists for this patient to this hospital from your hospital.'}, status=status.HTTP_409_CONFLICT)
    
    new_request = DataAccessRequest.objects.create(
        patient=patient_user,
        to_hospital=to_hospital_obj,
        from_hospital=from_hospital_obj,
        status='pending',
        request_by=request.user 
    )

    return Response({'message': 'Data access request sent successfully.', 'request_id': new_request.id}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def grant_access_request(request, request_id):
    try:
        access_request = DataAccessRequest.objects.get(id=request_id)
    except DataAccessRequest.DoesNotExist:
        return Response({'error': 'The request doesn\'t exist'}, status=status.HTTP_404_NOT_NOT_FOUND)

    if access_request.status != 'pending':
        return Response({'message': 'Request was either accepted or denied'}, status=status.HTTP_202_ACCEPTED)

    # NEW: The admin must specify which record they are granting access to
    # This record should belong to the patient linked to the access_request.
    record_id_to_grant = request.data.get('record_id') 
    if not record_id_to_grant:
        return Response({'error': 'No record_id provided for granting access.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the specific PatientRecord. Crucially, ensure it belongs to the patient
        # associated with this access request.
        record_to_grant = PatientRecord.objects.get(
            id=record_id_to_grant, 
            patient=access_request.patient # Ensure the record belongs to the patient in the request
        )
    except PatientRecord.DoesNotExist:
        return Response({'error': 'The specified record_id does not exist for this patient.'}, status=status.HTTP_404_NOT_FOUND)

    # Assign the identified record to the access request
    access_request.record = record_to_grant 
    access_request.status = 'granted'
    access_request.save()

    return Response({
        'message': 'Admin has successfully approved the request'
    }, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsDoctorUser])
def check_access_request(request, request_id):
    try:
        access_request = DataAccessRequest.objects.get(id=request_id, request_by=request.user)
    except DataAccessRequest.DoesNotExist:
        return Response({'error': 'The request doesn\'t exist or you are not the requester'}, status=status.HTTP_404_NOT_FOUND)
    
    if access_request.status != 'granted':
        return Response({'message': 'Request waiting for approval or has been denied'}, status=status.HTTP_202_ACCEPTED)
    
    record = access_request.record
    bundle = generate_patient_record_json(record)

    return Response({
        'data': bundle
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def deny_access_request(request, request_id): 
    try:
        access_request = DataAccessRequest.objects.get(id=request_id)
    except DataAccessRequest.DoesNotExist:
        return Response({'error': 'The request doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)

    if access_request.status != 'pending':
        return Response({'message': 'Request was already approved or denied, or is not pending.'}, status=status.HTTP_202_ACCEPTED)

    access_request.status = 'denied'
    access_request.save() 

    return Response({
        'message': 'Admin has successfully denied the request.'
    }, status=status.HTTP_200_OK)