# Generated by Django 5.0.1 on 2024-02-21 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_app', '0004_alter_customuser_mpin_delete_mpin_for_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='account_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]