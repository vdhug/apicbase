from django.db import models, IntegrityError, DataError
from django.core.validators import MaxLengthValidator, MinLengthValidator, DecimalValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Q

""" IngredientManager, class to manage all the db operations related to the ingredient model """
class IngredientManager(models.Manager):

    """ Create and update method """
    def save_ingredient(self, name, article_number, base_amount, unit, base_price, id=None):
        try:
            i = Ingredient(id=id, name=name, article_number=article_number, base_amount=base_amount, unit=unit, base_price=base_price)

            if i.id==None:
                i.full_clean()
                i.save()
            else:
                i.full_clean(exclude=['id', 'article_number'])
                self.update(name=i.name, article_number=i.article_number, base_amount=i.base_amount, unit=i.unit, base_price=i.base_price)
            return {'success': True, 'object': i, 'message': 'Success on saving object'}

        except ValidationError as e:
            for property, message in e:
                return {'success': False, 'message': message[0], "property": property}

        except IntegrityError as e:
            return {'success': False, 'message': 'There is already an ingredient with that article number.'}

        except Exception as e:
            return {'success': False, 'message': 'Error in create_ingredient method. Raised in path: ingredient.models: line 27\n'+str(e)}

    """ Function that filter ingredients by name and article number """
    def filter_ingredients(self, text):
        return self.filter(Q(name__icontains=text) | Q(article_number__icontains=text))

class Ingredient(models.Model):
    objects = IngredientManager()

    """ Creating Article number property with django built in validators. Ensuring that article number will be a char range with min length of 1 and max length of 5 """
    article_number = models.CharField(max_length=5, unique=True, validators = [
        MaxLengthValidator(limit_value=5, message="The article number must be 5 characters maximum."),
        MinLengthValidator(limit_value=1, message="The article number must be 1 character minimum."),
        ]
    )

    """ Creating name property with django built in validators. Ensuring that name will be a char range with min length of 1 and max length of 64 """
    name = models.CharField(max_length=64, validators = [
        MaxLengthValidator(limit_value=64, message="The name of the article must be 5 characters maximum."),
        MinLengthValidator(limit_value=1, message="The name of the article must be 1 character minimum."),
        ]
    )

    """ Creating base amount property with django built in validators. Ensuring that the base amount is a decimal number between 0.00 and 9999999.99 """
    base_amount = models.DecimalField(max_digits=7, decimal_places=2, validators = [
        DecimalValidator(max_digits=7, decimal_places=2),
        MinValueValidator(limit_value=0.01, message="The base amount has to be greater than 0.00"),
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
        validators = [
            MaxLengthValidator(limit_value=5, message="The unit abbreviation must be 5 characters maximum."),
            MinLengthValidator(limit_value=1, message="The unit abbreviation must be 1 character minimum."),
            ]
    )

    """ Creating base price property with django built in validators. Ensuring that the base price is a decimal number between 0.00 and 9999999.99 """
    base_price = models.DecimalField(max_digits=7, decimal_places=2, validators = [
        DecimalValidator(max_digits=7, decimal_places=2),
        MinValueValidator(limit_value=0.01, message="The base price has to be greater than 0.00"),
        ]
    )

    """ Tracks when this ingredient was created """
    date_created = models.DateField(auto_now_add=True)
