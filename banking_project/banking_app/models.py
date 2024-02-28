import uuid
from django.db import models

from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    address = models.TextField(null=True, blank=True)
    phone = models.PositiveIntegerField(null=True, blank=True)
    mpin = models.PositiveIntegerField(blank=True,null=True)
    account_number = models.PositiveIntegerField(null=True, blank=True)
    ifsc = models.CharField(max_length = 30,null=True, blank=True)
    account_balance = models.PositiveIntegerField(null=True, blank=True,default=0)
    
    def __str__(self):
        return self.username
    


class Fund_transfer(models.Model):
    sender_user = models.ForeignKey('CustomUser',on_delete=models.CASCADE,
        related_name='sent_transfers',  # Unique related_name for sender_user
        verbose_name='Sender User',
        null=True, blank=True
    )
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_number = models.PositiveIntegerField(null=True, blank=True, default=0)
    confirm_account_number = models.PositiveIntegerField(null=True, blank=True, default=0)
    ifsc = models.CharField(max_length=20,null=True, blank=True,)
    receiving_account_holder_name = models.ForeignKey('CustomUser',
        on_delete=models.CASCADE,
        related_name='received_transfers',  # Unique related_name for receiving_account_holder_name
        verbose_name='Receiving Account Holder',null=True, blank=True
    )
    fund_receiving_other_bank_user = models.CharField(max_length=30,null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)
    mpin = models.PositiveIntegerField(default=0,null=True,blank=True)
    bill_payments = models.CharField(max_length=30,null=True, blank=True)
    
    def __str__(self):
        if self.receiving_account_holder_name:
            return str(f'{self.sender_user}-{self.transaction_id}-{self.receiving_account_holder_name}')
        elif self.fund_receiving_other_bank_user:
            return str(f'{self.sender_user}-{self.transaction_id}-{self.fund_receiving_other_bank_user}')
        else:
           return str(f'{self.sender_user}-{self.transaction_id}-{self.bill_payments}')
           
