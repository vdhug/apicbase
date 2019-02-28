from django.db import models, IntegrityError, DataError
from django.core.validators import MaxLengthValidator, MinLengthValidator, DecimalValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Q
from ingredients.models import Ingredient

""" RecipeManager, class to manage all the db operations related to the recipe model """
class RecipeManager(models.Manager):
    """ Create method """
    def save_recipe(self, name, description, method_of_preparation):
        try:
            r = Recipe(name=name, description=description, method_of_preparation=method_of_preparation)

            r.full_clean()
            r.save()

            return {'success': True, 'object': r, 'message': 'Success on saving recipe'}

        except ValidationError as e:
            for property, message in e:
                return {'success': False, 'message': message[0], "property": property}

        except IntegrityError as e:
            return {'success': False, 'message': 'There is already a recipe with that id.'}

        except Exception as e:
            return {'success': False, 'message': 'Error in save_recipe method. Raised in path: recipes.models: line 27\n'+str(e)}


class Recipe(models.Model):
    objects = RecipeManager()

    """ Creating name property with django built in validators. Ensuring that name will be a char range with min length of 1 and max length of 64 """
    name = models.CharField(max_length=64, validators = [
        MaxLengthValidator(limit_value=64, message="The name of the recipe must be 5 characters maximum."),
        MinLengthValidator(limit_value=1, message="The name of the recipe must be 1 character minimum."),
        ]
    )

    """ Creating description property with django built in validators. Ensuring that name will be a char range with min length of 1 and max length of 64 """
    description = models.CharField(max_length=64, validators = [
        MaxLengthValidator(limit_value=64, message="The description of the recipe must be 64 characters maximum."),
        MinLengthValidator(limit_value=1, message="The description of the recipe must be 1 character minimum."),
        ]
    )

    """ Creating method of preparation property with django built in validators. Ensuring that the method of preparation is not empty """
    method_of_preparation = models.TextField(validators = [
        MinLengthValidator(limit_value=1, message="The  method of preparation field of the recipe cannot be empty."),
        ]
    )

    ingredients_of_recipe = models.ManyToManyField(Ingredient, through='IngredientOfRecipe')

    """ Tracks when this recipe was created """
    date_created = models.DateField(auto_now_add=True)

    """ Tracks when this recipe is modifed """
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.description}"

    def number_of_ingredients(self):
        return len(self.ingredients)


    """ Defining the ordering default to be last_modified descending and in the sequence date_created descending """
    class Meta:
        ordering = ['-last_modified', "-date_created"]


""" IngredientOfRecipeManager, class to manage all the db operations related to the relationship between recipe and ingredient model """
class IngredientOfRecipeManager(models.Manager):
    def add_ingredient_of_recipe(self, recipe, ingredient, quantity):
        try:
            i = IngredientOfRecipe(recipe=recipe, ingredient=ingredient, quantity=quantity)
            i.full_clean()
            i.save()
            return {'success': True, 'object': i, 'message': 'Success on adding ingredient in the recipe'}

        except ValidationError as e:
            for property, message in e:
                return {'success': False, 'message': message[0], "property": property}

        except IntegrityError as e:
            return {'success': False, 'message': 'There is already an ingredient with this id in the recipe.'}

        except Exception as e:
            return {'success': False, 'message': 'Error in add_ingredient_of_recipe method. Raised in path: recipes.models: line 47\n'+str(e)}


    """ Check if one ingredient is already in the recipe """
    def is_ingredient_in_recipe(self, recipe_id, ingredient_id):
        return IngredientOfRecipe.objects.filter(recipe=recipe_id, ingredient=ingredient_id).exists()


""" Intermediary model to manage the relationship between recipe and ingredients """
class IngredientOfRecipe(models.Model):
    objects = IngredientOfRecipeManager()

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f"In the recipe: {self.recipe.name} - we need {self.quantity} of {self.ingredient.name}"

    """ Creating quantity property with django built in validators. Ensuring that the quantity is a decimal number between 0.00 and 9999999.99 """
    quantity = models.DecimalField(max_digits=7, decimal_places=2, validators = [
        DecimalValidator(max_digits=7, decimal_places=2),
        MinValueValidator(limit_value=0.01, message="The quantity has to be greater than 0.00"),
        ]
    )
