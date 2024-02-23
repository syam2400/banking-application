
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, PasswordResetRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Customer
