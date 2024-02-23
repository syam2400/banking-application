from django import http
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from .models import CustomUser
from .models import MPIN
from .serializers import  UserSerializer,UserLoginSerializer,Profileview_serializers,MPINSerializer
from .models import User, PasswordResetRequest,Transaction
from .serializers import UserSerializer, PasswordResetRequestSerializer,TransactionSerializer
# from .serializers import UserSerializer,Profileview_serializers
from rest_framework import status
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from your_app.views import reset_mpin
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

# from .models import Customer, Account


# registration class for signup and get the registered user details 
class RegisterUser(generics.CreateAPIView):
    permission_classes =  [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    

# class Registered_user_details(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer


    # def get(self, request):
    #     if request.user.is_superuser:
    #         user = CustomUser.objects.all()
    #         user_serializer = UserSerializer(user, many=True)
    #         return Response(user_serializer.data)
    #     else:
    #         return Response({"detail": "You do not have permission to view this resource."}, status=status.HTTP_403_FORBIDDEN)

    # def post(self, request):
    #     register_serializer = UserSerializer(data=request.data)
    #     if register_serializer.is_valid():
    #         register_serializer.save()
    #         return Response(register_serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class User_app_registration(APIView):
    def put(self, request):
        user = CustomUser.objects.get(username=request.user.name,  account_number=request.user.account_number )

 #login user with returned token with user data
class UserLoginAPIView(generics.CreateAPIView):
    permission_classes =  [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class =  UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('mpin')

            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                serialized_user = UserSerializer(user)
                return Response({
                    'user': serialized_user.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'status': f"{user.username} logged in successfully",
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 
#logout method for blacklisting the tokens for enhanced security    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract the refresh token from the request data
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            # Blacklist the refresh token
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
#to view the details of particular logged user
class UserProfileview(generics.RetrieveUpdateDestroyAPIView):
    permission_classes =  [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = Profileview_serializers

    # def get(self, request):
    #     user = self.request.user0
    #     user_details = CustomUser.objects.get(id=user)
    #     user_serializers = Profileview_serializers(user_details)
    #     if user_serializers.is_valid():
    #         user_serializers.save()
    #         return Response(user_serializers.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'error':'invalid'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_mpin(request):
    serializer = MPINSerializer(data=request.data)
    if serializer.is_valid():
        mpin = serializer.validated_data['mpin']
        user = request.user
        mpin_obj, created = MPIN.objects.get_or_create(user=user)
        mpin_obj.mpin = mpin
        mpin_obj.save()
        return Response({"message": "MPIN reset successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transactions(request):
    transactions = Transaction.objects.filter(user=request.user)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)



