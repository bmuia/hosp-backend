from django.urls import path
from .views import PatientRecordView


urlpatterns = [
    path('records/create/',PatientRecordView.as_view(), name='create-records')
]
