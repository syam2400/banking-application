from django.shortcuts import render


from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer,Profileview_serializers
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny



# registration class for signup and get the registered user details 
class RegisterUser(APIView):
    def get(self, request):
        if request.user.is_superuser:
            user = CustomUser.objects.all()
            user_serializer = UserSerializer(user, many=True)
            return Response(user_serializer.data)
        else:
            return Response({"detail": "You do not have permission to view this resource."}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        register_serializer = UserSerializer(data=request.data)
        if register_serializer.is_valid():
            register_serializer.save()
            return Response(register_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# this is for token claiming and it adds username to the encoded token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        # ...

        return token


# login class for get tokens
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# to view user profile details
class Profile_details_view(APIView):
    def get(self, request,*args, **kwargs):
        model = CustomUser.objects.all()
        serilized_profile_data = Profileview_serializers(model,many=True)
        return Response(serilized_profile_data.data,status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            create_user_profile = self.get_user_profile



# class Profile_create_view(APIView):
#     def post(self, request, *args, **kwargs):
#         if request.method == 'POST':
#             user = 