# Generated by Django 2.0 on 2019-02-25 20:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_number', models.CharField(max_length=5, unique=True, validators=[django.core.validators.MaxLengthValidator(limit_value=5, message='The article number must be 5 characters maximum.'), django.core.validators.MinLengthValidator(limit_value=1, message='The article number must be 1 character minimum.')])),
                ('base_amount', models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.DecimalValidator(decimal_places=2, max_digits=7), django.core.validators.MinValueValidator(limit_value=0.01, message='The base amount cannot be equals to 0.00')])),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.DecimalValidator(decimal_places=2, max_digits=7), django.core.validators.MinValueValidator(limit_value=0.01, message='The base price cannot be equals to 0.00')])),
                ('unit', models.CharField(choices=[('G', 'Grams'), ('KG', 'Kilograms'), ('CL', 'Centiliters'), ('LT', 'Liters')], max_length=5)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
