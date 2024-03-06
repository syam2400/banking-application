from django import http
from django.shortcuts import get_object_or_404, render
from django.views import View

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, Fund_transfer
from .serializers import *
from rest_framework import status
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# from .views import reset_mpin
# from .serializers import TransactionSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
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

from django.db import transaction
from rest_framework.pagination import PageNumberPagination


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




#app registraion and forgot password
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
                        f'Click here to reset your password: http://127.0.0.1:8000/new-password/confirm/{uidb64}/{token}/',
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
   



#email template rendering class for user who get a email with a link which he can add new mpin through a custom template
class CustomPasswordResetConfirmView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        return render(request,'banking_app/templates/email-template.html', context)
    

 #new mpin creation and validation,from the custom template    
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
            if new_password.isdigit() and new_password == password_confirm:
                # try:
                #     validate_password(new_password, user)
                # except ValidationError as e:
                #     return Response({'errors': list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(new_password)
                user.save()
                success_msg = 'Password reset successfully'
                return render(request,'banking_app/templates/email-template.html',{"success_msg":success_msg})
            else:
                # return Response({'error': 'Password does not match the confirm password or is not provided.'}, status=status.HTTP_400_BAD_REQUEST)
                success_msg = 'Password validation failed re-enter password'
                return render(request,'banking_app/templates/email-template.html',{"success_msg":success_msg})
        else:
            success_msg = 'token is invalid create a new requeset'
            return render(request,'banking_app/templates/email-template.html',{"success_msg":success_msg})


   
#login user with returned token with user data
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
class UserProfileview(generics.RetrieveAPIView):
    permission_classes =  [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = Profileview_serializers


#FUND TRANSFER TO SAME BANK USER
class Fund_Transfer_views(APIView):
    permission_classes = [AllowAny]
   
    def post(self, request, *args, **kwargs):
        
        transfer_serializer = Fund_transfer_serializers(data=request.data)
        
        if  transfer_serializer.is_valid():
    
            user = get_object_or_404(CustomUser, username=transfer_serializer.validated_data.get('sender_user'))
            account_holder_name = get_object_or_404(CustomUser, username=request.data.get('receiving_account_holder_name'))
           

            confirmation_mpin = int(request.data.get('mpin'))
            amount = int(request.data.get('amount'))

            if request.data['account_number'] != request.data.get('confirm_account_number'):
                return Response({"status":"Account number and confirm account number must match."},status=status.HTTP_401_UNAUTHORIZED)
            
            if int(request.data.get('confirm_account_number')) !=  int(account_holder_name.account_number):
                 return Response({"status":"Account number and account holder name must match."},status=status.HTTP_401_UNAUTHORIZED)
            
            if user.account_balance < amount:  
                return Response({'error': 'Insufficient balance'}, status=status.HTTP_204_NO_CONTENT)
          
          
            user = authenticate(username=user.username, password=confirmation_mpin)
            if user is not None:
                with transaction.atomic():
                        user.account_balance -= amount
                        user.save()

                        account_holder_name.account_balance += amount
                        account_holder_name.save()

                        # Create the Fund_transfer object
                        confirm_transfer = Fund_transfer.objects.create(sender_user=user.username,account_number=account_holder_name.account_number,
                                                                        ifsc=request.data.get('ifsc'),receiving_account_holder_name=account_holder_name,
                                                                        amount=amount)
                    
                        return Response({'message':'fund tranfered succesfully'}, status=status.HTTP_201_CREATED)
            else:      
              return Response({'message':"invalid mpin"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            return Response( transfer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#fund transfer to other banks
class OtherBank_Fund_Transfer_views(APIView):
    permission_classes = [AllowAny]
   
    def post(self, request, *args, **kwargs):
        
        transfer_serializer =Fund_transfer_serializers(data=request.data)
        
        if  transfer_serializer.is_valid():
    
            user = get_object_or_404(CustomUser, username=transfer_serializer.validated_data.get('sender_user'))
         
            confirmation_mpin = int(request.data.get('mpin'))
            amount = int(request.data.get('amount'))

            if request.data['account_number'] != request.data.get('confirm_account_number'):
                return Response({"status":"Account number and confirm account number must match."},status=status.HTTP_401_UNAUTHORIZED)
            
           
            if user.account_balance < amount:  
                return Response({'error': 'Insufficient balance'}, status=status.HTTP_204_NO_CONTENT)
          
          
            user = authenticate(username=user.username, password=confirmation_mpin)
            if user is not None:
                with transaction.atomic():
                        user.account_balance -= amount
                        user.save()

                        confirm_transfer = Fund_transfer.objects.create(sender_user=user,account_number=request.data.get('confirm_account_number'),
                                                                        ifsc=request.data.get('ifsc'),
                                                                        fund_receiving_other_bank_user=request.data.get('receiving_account_holder_name'),
                                                                        amount=amount)
                      
                        print('confirm_transfer')
                        return Response({'message':'fund tranfered succesfully'}, status=status.HTTP_201_CREATED)
            else:      
              return Response({'message':"invalid mpin"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            return Response( transfer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#when user completed tha transaction next step will be entering the mpin ,with front end should pass the sender and receiver data


#USER TRANSACTIONS DETAILS
class LoggedUserTransactionsDetails(APIView):
    permission_classes = [AllowAny]
    # queryset = Fund_transfer.objects.all()
    # serializer_class = User_fund_transfer_serializers
    # lookup_fields = 'id'
    def get(self, request,id):
        # logged_user = request.data.get('pk')
        user = get_object_or_404(CustomUser,id=id)
       
        current_user_transaction = Fund_transfer.objects.filter(sender_user=user)
        
        paginator = PageNumberPagination()
        paginator.page_size = 3
        result_page = paginator.paginate_queryset(current_user_transaction, request)
        
        transaction_Serilizer = User_fund_transfer_serializers(result_page, many=True)
        return paginator.get_paginated_response(transaction_Serilizer.data)
      
      
        
#payment setup through banking app
class PayBills(APIView):
    permission_classes = [AllowAny]
    # queryset = Fund_transfer.objects.all()
    # serializer_class = PayBilllsSerializer
    def post(self, request, *args, **kwargs):
        paybills_serializer = PayBillsSerializer(data=request.data)

        if paybills_serializer.is_valid():

            payment_for = paybills_serializer.validated_data.get('payment_for')
            user_id = paybills_serializer.validated_data.get('logged_user_id')
            logged_user = get_object_or_404(CustomUser,pk=user_id)
            bill_amount = paybills_serializer.validated_data.get('payment_amount')
            mpin = paybills_serializer.validated_data.get('mpin')

            if int(logged_user.account_balance) < int(bill_amount):
                return Response({"status": "insufficent account balance"},status=status.HTTP_400_BAD_REQUEST)
            
            
            logged_user = authenticate(username=logged_user.username, password=mpin)
            if  logged_user is not None:
                with transaction.atomic():
                        logged_user.account_balance  -= int(bill_amount)
                        
                        logged_user.save()

                        confirm_bill_payment = Fund_transfer.objects.create(sender_user= logged_user,bill_payments=payment_for,
                                                                         amount=bill_amount)
                        
                        return Response({'message':'bill payment succesfully done'}, status=status.HTTP_201_CREATED)
            else:      
              return Response({'message':"invalid mpin"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            return Response(paybills_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                                                      
            





