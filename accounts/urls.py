from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from .views import GetCurrentUserView, RegisterNewUser, NewHospitalView, CustomLoginView, GetAllHospitals, GetAllUsers, fetchAllPatients


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('logout/', TokenBlacklistView.as_view(), name='blacklist-refresh-token'),

    path('whoami/', GetCurrentUserView.as_view(), name='current-logged-in-user'),
    path('admin/register/', RegisterNewUser.as_view(), name='admin-register-new-user'),
    path('users/', GetAllUsers.as_view(), name='get-all-users'),
    path('patients/', fetchAllPatients.as_view(), name='get-all-patients'),

    path('hospital/create/', NewHospitalView.as_view(), name='new-hospital'),
    path('hospitals/', GetAllHospitals.as_view(), name='all-hospitals')
]