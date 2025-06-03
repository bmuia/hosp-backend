from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Hospital
from records.models import PatientRecord

User = get_user_model()

class DataAccessRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('denied', 'Denied'),
        ('granted', 'Granted'),
    )
    from_hospital = models.ForeignKey(Hospital, related_name='outgoing_transfers', on_delete=models.CASCADE)
    to_hospital = models.ForeignKey(Hospital, related_name='incoming_transfers', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'roles': 'patient'})
    record = models.ForeignKey(PatientRecord, on_delete=models.SET_NULL, null=True,blank=True)
    request_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_data_access_requests',null=True,blank=True) 



    def __str__(self):
        return f"TransferRequest from {self.from_request} to {self.to_request} - Status: {self.status}"
