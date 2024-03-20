from os import name
from django.urls import include, path
from rest_framework.authtoken import views
from .views import (
    UserRegistrationRudview,
    AccountRudView,
    UnAprovedImployeeView,
    AproveView,
    CustomAuthToken,
    CustomAdminAuthToken,
    AssignLocationToAstaffMember,
    AprovedImployeeView,
    DeleteAccountView
)

urlpatterns = [

    path('', UserRegistrationRudview.as_view(), name = 'user-rud'),
    path('accounts/', AprovedImployeeView.as_view(), name = 'acc-rud'),
    path('login/', CustomAuthToken.as_view(), name = 'login-rud'),
    path('adminlogin/', CustomAdminAuthToken.as_view(), name = 'admin-login'),
    path('unapproved/', UnAprovedImployeeView.as_view(), name='unapproved'),
    path('approve/<int:pk>/', AproveView.as_view(), name='Aprove'),
    path('deleteaccount/<int:pk>/', DeleteAccountView.as_view(), name = 'delete'),
    path('assignLocation/<int:pk>/<int:id>/', AssignLocationToAstaffMember.as_view(), name = "AssignLocationToAstaffMember"),
    
]