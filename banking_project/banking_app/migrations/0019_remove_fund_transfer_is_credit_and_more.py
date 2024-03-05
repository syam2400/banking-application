# Generated by Django 5.0.1 on 2024-02-29 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_app', '0018_fund_transfer_is_credit_fund_transfer_is_debit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fund_transfer',
            name='is_credit',
        ),
        migrations.RemoveField(
            model_name='fund_transfer',
            name='is_debit',
        ),
        migrations.AddField(
            model_name='fund_transfer',
            name='date_of_trasaction',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
