"""
URL configuration for banking_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.urls import path
from banking_app.views import *

# from rest_framework.routers import SimpleRouter
# from .views import PasswordResetView



urlpatterns = [
  path('register_user/',RegisterUser.as_view()),
# path('registered-user-details/<int:pk>/',Registered_user_details.as_view()),
  path('user-login-get-token/',UserLoginAPIView.as_view()),
  path('api/reset-mpin/', reset_mpin, name='reset_mpin'),
  path('api/logout/', LogoutView.as_view(), name='auth_logout'),
  path('user-profile-view/<int:pk>/',UserProfileview.as_view()),

  path('password-reset-view/',User_registration_and_mpin.as_view(),name='initiate-password-reset'),
  path('password-reset/confirm/<str:uidb64>/<str:token>/',Reset_password.as_view(),name='reset-password')
  

]

