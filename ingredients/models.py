from django.db import models

# Create your models here.
class Ingredient(models.Model):

    """ Creating Article number property with django built in validators. Ensuring that article number will be a char range with min length of 1 and max length of 5 """
    article_number = models.CharField(max_length=5, unique=True, validators = [
        MaxLengthValidator(limit_value=5, message="The article number must be 5 characters maximum."),
        MinLengthValidator(limit_value=1, message="The article number must be 1 character minimum."),
        ]
    )

    """ Creating base amount property with django built in validators. Ensuring that the base amount is a decimal number between 0.00 and 9999999.99 """
    base_amount = models.DecimalField(max_digits=7, decimal_place=2, validators = [
        DecimalValidator(max_digits=7, max_decimal_places=2, message="The base amount must be a 7 decimal number with two decimal places maximum."),
        MinValueValidator(limit_value=0.01, message="The base amount cannot be equals to 0.00"),
        ]
    )

    """ Creating base price property with django built in validators. Ensuring that the base price is a decimal number between 0.00 and 9999999.99 """
    base_price = models.DecimalField(max_digits=7, decimal_place=2, validators = [
        DecimalValidator(max_digits=7, max_decimal_places=2, message="The base price must be a 7 decimal number with two decimal places maximum."),
        MinValueValidator(limit_value=0.01, message="The base price cannot be equals to 0.00"),
        ]
    )

    """ List of units supported by the application. """
    UNIT_CHOICES = (
        ('G', 'Grams'),
        ('KG', 'Kilograms'),
        ('CL', 'Centiliters'),
        ('LT', 'Liters'),
    )
    unit = models.CharField(
        choices=UNIT_CHOICES,
    )

    """ Tracks when this ingredient was created """
    date_created = models.DateField(auto_now_add=True)
