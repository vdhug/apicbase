from django.db import models, IntegrityError, DataError
from django.core.validators import MaxLengthValidator, MinLengthValidator, DecimalValidator, MinValueValidator
from django.core.exceptions import ValidationError


""" IngredientManager, class to manage all the db operations related to the ingredient model """
class IngredientManager(models.Manager):

    """ Create """
    def create_ingredient(self, article_number, base_amount, unit, base_price):
        try:
            i = Ingredient(article_number=article_number, base_amount=base_amount, unit=unit, base_price=base_price)
            i.full_clean()
            i.save()
            return {'success': True, 'object': i}
        except ValidationError as e:
            return {'success': False, 'message': e}
        except IntegrityError as e:
            return {'success': False, 'message': 'There is already an ingredient with that article number.'}
        except Exception as e:
            raise e

class Ingredient(models.Model):
    objects = IngredientManager()

    """ Creating Article number property with django built in validators. Ensuring that article number will be a char range with min length of 1 and max length of 5 """
    article_number = models.CharField(max_length=5, unique=True, validators = [
        MaxLengthValidator(limit_value=5, message="The article number must be 5 characters maximum."),
        MinLengthValidator(limit_value=1, message="The article number must be 1 character minimum."),
        ]
    )

    """ Creating base amount property with django built in validators. Ensuring that the base amount is a decimal number between 0.00 and 9999999.99 """
    base_amount = models.DecimalField(max_digits=7, decimal_places=2, validators = [
        DecimalValidator(max_digits=7, decimal_places=2),
        MinValueValidator(limit_value=0.01, message="The base amount cannot be equals to 0.00"),
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
        max_length=5,
    )

    """ Creating base price property with django built in validators. Ensuring that the base price is a decimal number between 0.00 and 9999999.99 """
    base_price = models.DecimalField(max_digits=7, decimal_places=2, validators = [
        DecimalValidator(max_digits=7, decimal_places=2),
        MinValueValidator(limit_value=0.01, message="The base price cannot be equals to 0.00"),
        ]
    )

    """ Tracks when this ingredient was created """
    date_created = models.DateField(auto_now_add=True)
