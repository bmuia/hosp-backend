from django.urls import path
from . import views


urlpatterns = [
    path('send-request/', views.send_data_access_request, name='send_data_access_request'),
    path('grant-request/<int:request_id>/', views.grant_access_request, name='grant_access_request'),
    path('check-request/<int:request_id>/', views.check_access_request, name='check_access_request'),
    path('deny-request/<int:request_id>/', views.deny_access_request, name='deny_access_request'),
    path('requests/all/',views.get_all_data_access_requests, name='get_all_data_access_requests'),
]