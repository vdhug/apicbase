from django.test import TestCase
from ingredients.models import Ingredient
from .models import Recipe, IngredientOfRecipe

# Create your tests here.
class ModelsTestCase(TestCase):

    def setUp(self):
        # Create ingredients.
        i1 = Ingredient.objects.save_ingredient(name="Coffe", article_number="CO001", base_amount=1.00, unit='LT', base_price=2.00)
        r1 = Recipe.objects.save_recipe(name="Capuccino", description="Espresso-based coffee drink prepared with steamed milk foam.", method_of_preparation="Put chocolate with coffe with milk and blend.")



    """ Check if the save_recipe method is working properly when receiveing an recipe with article number empty """
    def test_recipe_save(self):
        result = Recipe.objects.save_recipe(name="Capuccino", description=" Espresso-based coffee drink prepared with steamed milk foam.", method_of_preparation="Put chocolate with coffe with milk and blend.")
        self.assertTrue(result['success'])


    """ Check if the save_recipe method is working properly when receiveing an recipe with name empty """
    def test_recipe_empty_name(self):
        result = Recipe.objects.save_recipe(name="", description="Espresso-based coffee drink prepared with steamed milk foam.", method_of_preparation="Put chocolate with coffe with milk and blend.")
        self.assertFalse(result['success'])


    """ Check if the save_recipe method is working properly when receiveing an recipe with description empty """
    def test_recipe_empty_description(self):
        result = Recipe.objects.save_recipe(name="Capuccino", description="", method_of_preparation="Put chocolate with coffe with milk and blend.")
        self.assertFalse(result['success'])


    """ Check if the save_recipe method is working properly when receiveing an recipe with method of preparation empty """
    def test_recipe_empty_method_of_preparation(self):
        result = Recipe.objects.save_recipe(name="Capuccino", description="Espresso-based coffee drink prepared with steamed milk foam.", method_of_preparation="")
        self.assertFalse(result['success'])


    """ Check if the add_ingredient_of_recipe method is working properly """
    def test_add_ingredient_of_recipe(self):
        r = Recipe.objects.get(name="Capuccino")
        i = Ingredient.objects.get(article_number="CO001")

        result = IngredientOfRecipe.objects.add_ingredient_of_recipe(recipe=r, ingredient=i, quantity=2)
        self.assertTrue(result['success'])


    """ Check if number of ingredients from one recipe """
    def test_check_number_of_ingredients_from_recipe(self):
        i1 = Ingredient.objects.get(name="Coffe")
        r1 = Recipe.objects.get(name="Capuccino")
        result = IngredientOfRecipe.objects.add_ingredient_of_recipe(recipe=r1, ingredient=i1, quantity=2)
        result = IngredientOfRecipe.objects.add_ingredient_of_recipe(recipe=r1, ingredient=i1, quantity=4)
        self.assertEqual(r1.ingredients.count(), 2)


    """ Check if is_ingredient_in_recipe method is working properly in returning false """
    def test_check_is_ingredient_not_in_recipe(self):
        r1 = Recipe.objects.get(name="Capuccino")
        i1 = Ingredient.objects.get(name="Coffe")
        IngredientOfRecipe.objects.add_ingredient_of_recipe(recipe=r1, ingredient=i1, quantity=2)
        i2 = Ingredient.objects.save_ingredient(name="Milk", article_number="MI001", base_amount=1.00, unit='LT', base_price=0.75)
        result = IngredientOfRecipe.objects.is_ingredient_in_recipe(recipe_id=r1.id, ingredient_id=i2['object'].id)
        self.assertFalse(result)


    """ Check if is_ingredient_in_recipe method is working properly in returning True """
    def test_check_is_ingredient_in_recipe(self):
        r1 = Recipe.objects.get(name="Capuccino")
        i1 = Ingredient.objects.get(name="Coffe")
        IngredientOfRecipe.objects.add_ingredient_of_recipe(recipe=r1, ingredient=i1, quantity=2)
        i2 = Ingredient.objects.save_ingredient(name="Milk", article_number="MI001", base_amount=1.00, unit='LT', base_price=0.75)
        result = IngredientOfRecipe.objects.is_ingredient_in_recipe(recipe_id=r1.id, ingredient_id=i1.id)
        self.assertTrue(result)


    """ Check if is_ingredient_in_recipe method is working properly in returning False """
    def test_check_recipe_has_ingredient(self):
        r1 = Recipe.objects.get(name="Capuccino")
        i1 = Ingredient.objects.get(name="Coffe")
        IngredientOfRecipe.objects.add_ingredient_of_recipe(recipe=r1, ingredient=i1, quantity=2)
        i2 = Ingredient.objects.save_ingredient(name="Milk", article_number="MI001", base_amount=1.00, unit='LT', base_price=0.75)
        Recipe.objects.save_recipe(name="Test", description="Test", method_of_preparation="Test")
        recipe = Recipe.objects.get(name="Test")
        result = IngredientOfRecipe.objects.is_ingredient_in_recipe(recipe_id=recipe.id, ingredient_id=i1.id)
        self.assertFalse(result)


    """ Check if the get_cost method is working properly """
    def test_get_cost(self):
        r = Recipe.objects.get(name="Capuccino")
        i = Ingredient.objects.get(article_number="CO001")

        result = IngredientOfRecipe.objects.add_ingredient_of_recipe(recipe=r, ingredient=i, quantity=2)
        self.assertEqual(r.get_cost(), 4)
