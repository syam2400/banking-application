from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .models import User, PasswordResetRequest,Transaction
from .serializers import UserSerializer, PasswordResetRequestSerializer,TransactionSerializer
# from .serializers import UserSerializer,Profileview_serializers
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny

from rest_framework.permissions import IsAuthenticated
from .models import Customer, Account

