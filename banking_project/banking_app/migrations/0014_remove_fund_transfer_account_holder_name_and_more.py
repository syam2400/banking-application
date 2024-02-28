# Generated by Django 5.0.1 on 2024-02-26 11:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_app', '0013_fund_transfer_sender_user_alter_fund_transfer_ifsc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fund_transfer',
            name='account_holder_name',
        ),
        migrations.AddField(
            model_name='fund_transfer',
            name='receiving_account_holder_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_transfers', to=settings.AUTH_USER_MODEL, verbose_name='Receiving Account Holder'),
        ),
        migrations.AlterField(
            model_name='fund_transfer',
            name='sender_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_transfers', to=settings.AUTH_USER_MODEL, verbose_name='Sender User'),
        ),
    ]