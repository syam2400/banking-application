from django import http
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import  UserSerializer,UserLoginSerializer,Profileview_serializers,App_register_serializers
from rest_framework import status

from rest_framework import generics

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


#for new mpin setup and app registration
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
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





class User_registration_and_mpin(APIView):
   permission_classes =  [AllowAny]
    # queryset = CustomUser.objects.all()
    # serializer_class = UserSerializer
   
   def post(self, request, *args, **kwargs):
       
            input_data_serializer = App_register_serializers(data=request.data)
            if input_data_serializer.is_valid():
                username = input_data_serializer.validated_data.get('username')
                account_number = input_data_serializer.validated_data.get('account_number')
                print (username, account_number)

                try:
                    user = CustomUser.objects.get(username=username, account_number=account_number)
                    user_email = user.email
                    uid = user.id
                    uidb64 = urlsafe_base64_encode(force_bytes(uid))
                   
                       # Generate and send reset token
                    token_generator = PasswordResetTokenGenerator()
                    token = token_generator.make_token(user)
                    send_mail(
                        'Password Reset Request',
                        f'Click here to reset your password: http://127.0.0.1:8000/password-reset/confirm/{uidb64}/{token}/',
                        'from@your-domain.com',
                        [user_email],
                        fail_silently=False
                    )
                    return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)

                    # user_details_serializer =Profileview_serializers(user)
                    # return Response(user_details_serializer.data)
                except CustomUser.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response(input_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

        
class Reset_password(APIView):
      permission_classes =  [AllowAny]
      def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=uid)
            print(user)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            # Extract new password from request data
            new_password = request.data.get('new_password')
            password_confirm = request.data.get('password_confirm')

            # Validate the new password
            if new_password and new_password == password_confirm:
                try:
                    validate_password(new_password, user)
                except ValidationError as e:
                    return Response({'errors': list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Password does not match the confirm password or is not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Token is invalid'}, status=status.HTTP_400_BAD_REQUEST)


   
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

