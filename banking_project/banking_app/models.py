from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser


# class Mpin_for_login(models.Model):
#     login_pin = models.CharField(max_length=10)

#     confirm_mpin = models.CharField(max_length=10,null=True, blank=True)
     
#     def __str__(self):
#         return self.login_pin


class CustomUser(AbstractUser):
    address = models.TextField(null=True, blank=True)
    phone = models.PositiveIntegerField(null=True, blank=True)
    mpin = models.PositiveIntegerField(blank=True,null=True)
    account_number = models.PositiveIntegerField(null=True, blank=True)
    ifsc = models.CharField(max_length = 30,null=True, blank=True)
    account_balance = models.PositiveIntegerField(null=True, blank=True,default=0)
    
    def _str_(self):
        return self.username
    


