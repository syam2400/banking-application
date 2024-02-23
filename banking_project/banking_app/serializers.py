from rest_framework import serializers
from .models import CustomUser


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

class App_register_serializers(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    account_number = serializers.CharField(max_length=20)