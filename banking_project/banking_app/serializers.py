
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import serializers
from .models import *

from django.contrib.auth import authenticate
from django.db import transaction

from rest_framework import status
#serilizers for user registerations
class UserSerializer(serializers.ModelSerializer):
    mpin = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = CustomUser.objects.create(username=validated_data['username'],phone=validated_data['phone'],
                                         email=validated_data['email'],
                                         account_number=validated_data['account_number'],
                                         ifsc = validated_data['ifsc'],
                                         account_balance = validated_data['account_balance'])
                                 
        user.set_password(validated_data['mpin'])
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ['id','username', 'phone', 'email','account_number','ifsc','account_balance','mpin']


class Profileview_serializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = ['id','username', 'phone', 'email','account_number','ifsc','account_balance','mpin']
        fields = '__all__'



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    mpin = serializers.CharField(max_length=128, write_only=True)

class MPINSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPIN
        fields = ('mpin',)

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'user', 'amount', 'description', 'timestamp')

class App_register_serializers(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    account_number = serializers.CharField(max_length=20)



  #fund transfer
class User_fund_transfer_serializers(serializers.ModelSerializer):

    class Meta:
            model = Fund_transfer
            fields = '__all__'

   
# class OtherBank_fund_transfer_serializers(serializers.Serializer):
#     sender_user = serializers.CharField(max_length=30,write_only=True)
#     account_number = serializers.IntegerField(default=0,write_only=True)
#     confirm_account_number = serializers.IntegerField(default=0,write_only=True)
#     ifsc = serializers.CharField(max_length=20,write_only=True)
#     amount = serializers.IntegerField(default=0,write_only=True)
#     receiving_account_holder_name = serializers.CharField(max_length=30,write_only=True)
#     mpin = serializers.IntegerField(default=0,write_only=True)






class Fund_transfer_serializers(serializers.Serializer):   
    sender_user = serializers.CharField(max_length=30,write_only=True)
    account_number = serializers.IntegerField(default=0,write_only=True)
    confirm_account_number = serializers.IntegerField(default=0,write_only=True)
    ifsc = serializers.CharField(max_length=20,write_only=True)
    amount = serializers.IntegerField(default=0,write_only=True)
    receiving_account_holder_name = serializers.CharField(max_length=30,write_only=True)
    mpin = serializers.IntegerField(default=0,write_only=True)



    # def validate(self, request):
            
    
    #         user = get_object_or_404(CustomUser, username=request.data.get('sender_user'))
    #         account_holder_name = get_object_or_404(CustomUser, username=request.data.get('receiving_account_holder_name'))
    #         confirmation_mpin = int(request.data.get('mpin'))
    #         amount = int(request.data.get('amount'))

    #         if request.data['account_number'] != request.data.get('confirm_account_number'):
    #             return Response({"status":"Account number and confirm account number must match"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            
    #         if request.data['account_number'] !=   account_holder_name.account_number:
    #            return Response({"messagge":"invalid user details"}, status=status.HTTP_401_UNAUTHORIZED)
            
    #         if user.account_balance < amount:  
    #             return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
          
          
    #         user = authenticate(username=user.username, password=confirmation_mpin)
    #         if user is not None:
    #             with transaction.atomic():
    #                     user.account_balance -= amount
    #                     user.save()

    #                     account_holder_name.account_balance += amount
    #                     account_holder_name.save()

    #                     # Create the Fund_transfer object
    #                     confirm_transfer = Fund_transfer.objects.create(sender_user=user,account_number=account_holder_name.account_number,
    #                                                                     ifsc=request.data.get('ifsc'),receiving_account_holder_name=account_holder_name,
    #                                                                     amount=amount)
    #                     confirm_transfer_serilizer = confirm_fund_transfer_serializers(data=request.data)
    #                     if confirm_transfer_serilizer.is_valid():    
                        
    #                         return Response(confirm_transfer_serilizer.data, status=status.HTTP_201_CREATED)
    #         else:      
    #           return Response({'message':"invalid mpin"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        

