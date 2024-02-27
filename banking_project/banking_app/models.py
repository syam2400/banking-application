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

class MPIN(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mpin = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user.username}'s MPIN"
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

class LoanApplication(models.Model):
    APPLICANT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=APPLICANT_STATUS_CHOICES, default='PENDING')
    # Add other fields as needed

    def __str__(self):
        return f"{self.applicant.username}'s Loan Application"

