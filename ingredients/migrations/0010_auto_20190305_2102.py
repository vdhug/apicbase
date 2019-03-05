# Generated by Django 2.0 on 2019-03-05 21:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0009_auto_20190305_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(choices=[('G', 'Grams'), ('KG', 'Kilograms'), ('CL', 'Centiliters'), ('LT', 'Liters'), ('ML', 'Milliliters'), ('U', 'Unit')], max_length=5, validators=[django.core.validators.MaxLengthValidator(limit_value=5, message='The unit abbreviation must be 5 characters maximum.'), django.core.validators.MinLengthValidator(limit_value=1, message='The unit abbreviation must be 1 character minimum.')]),
        ),
    ]