from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser




class CustomUser(AbstractUser):
    address = models.TextField()
    phone = models.PositiveIntegerField(null=True, blank=True)
    mpin = models.PositiveIntegerField(null=True, blank=True)
    
    def _str_(self):
        return self.username
class MPIN(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mpin = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user.username}'s MPIN"

class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digit=10,decimal_places=2)
    description=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
