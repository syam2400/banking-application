# Generated by Django 5.0.1 on 2024-02-28 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_app', '0016_fund_transfer_fund_receiving_other_bank_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund_transfer',
            name='bill_payments',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
