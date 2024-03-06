
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import serializers
from .models import *

from django.contrib.auth import authenticate
# from django.db import transaction

from rest_framework import status
#serializers for user registerations
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

# class MPINSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MPIN
#         fields = ('mpin',)

# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = ('id', 'user', 'amount', 'description', 'timestamp')

class App_register_serializers(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    account_number = serializers.CharField(max_length=20)



  #fund transfer
class User_fund_transfer_serializers(serializers.ModelSerializer):
    sender_user_username = serializers.CharField(source='sender_user.username', read_only=True)
    receiving_account_holder_name_username = serializers.CharField(source='receiving_account_holder_name.username', read_only=True)
    user_bill_payments = serializers.CharField(source='bill_payments', read_only=True)
    date_of_transaction = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Fund_transfer
        fields = ['sender_user_username', 'receiving_account_holder_name_username','user_bill_payments', 'transaction_id', 'ifsc', 'account_number', 'amount','date_of_transaction']
      

   


class Fund_transfer_serializers(serializers.Serializer):   
    sender_user = serializers.CharField(max_length=30,write_only=True)
    account_number = serializers.IntegerField(default=0,write_only=True)
    confirm_account_number = serializers.IntegerField(default=0,write_only=True)
    ifsc = serializers.CharField(max_length=20,write_only=True)
    amount = serializers.IntegerField(default=0,write_only=True)
    receiving_account_holder_name = serializers.CharField(max_length=30,write_only=True)
    mpin = serializers.IntegerField(default=0,write_only=True)



class PayBillsSerializer(serializers.Serializer):
    payment_for = serializers.CharField(max_length=30,write_only=True)
    logged_user_id = serializers.IntegerField(default=0,write_only=True)
    payment_amount = serializers.IntegerField(default=0,write_only=True)
    mpin = serializers.IntegerField(default=0,write_only=True)

  