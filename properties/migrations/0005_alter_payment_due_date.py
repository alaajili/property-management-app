# Generated by Django 5.1 on 2024-08-31 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_remove_payment_date_payment_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='due_date',
            field=models.DateField(auto_now=True),
        ),
    ]
