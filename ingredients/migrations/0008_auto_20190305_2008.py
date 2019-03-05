# Generated by Django 2.0 on 2019-03-05 20:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0007_auto_20190227_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(choices=[('G', 'Grams'), ('KG', 'Kilograms'), ('CL', 'Centiliters'), ('LT', 'Liters'), ('U', 'UNIT')], max_length=5, validators=[django.core.validators.MaxLengthValidator(limit_value=5, message='The unit abbreviation must be 5 characters maximum.'), django.core.validators.MinLengthValidator(limit_value=1, message='The unit abbreviation must be 1 character minimum.')]),
        ),
    ]
