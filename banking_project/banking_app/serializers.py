from rest_framework import serializers
from .models import CustomUser


#serilizers for user registerations
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = CustomUser.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

# class Profileview_serializers(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'age',]