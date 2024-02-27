# Generated by Django 5.0.1 on 2024-02-25 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_app', '0009_customuser_account_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fund_transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.IntegerField(blank=True, default=0, null=True)),
                ('account_number', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('confirm_account_number', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('ifsc', models.CharField(max_length=20)),
                ('account_holder_name', models.CharField(max_length=30)),
            ],
        ),
    ]
