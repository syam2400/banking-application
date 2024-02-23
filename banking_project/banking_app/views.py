from django import http
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import  UserSerializer,UserLoginSerializer,Profileview_serializers
from rest_framework import status

from rest_framework import generics

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


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
    #     user_serilizers = Profileview_serializers(user_details)
    #     if user_serilizers.is_valid():
    #         user_serilizers.save()
    #         return Response(user_serilizers.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'error':'invalid'},status=status.HTTP_400_BAD_REQUEST)

