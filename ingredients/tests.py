from django.test import TestCase
from .models import Ingredient

# Create your tests here.
class ModelsTestCase(TestCase):

    def setUp(self):
        # Create ingredients.
        i1 = Ingredient.objects.save_ingredient(name="Corn", article_number="AA111", base_amount=1.75, unit='KG', base_price=2.50)


    """ Check if the save_ingredient method is working properly when receiveing an ingredient with article number empty """
    def test_ingredient_save(self):
        result = Ingredient.objects.save_ingredient(name="Corn", article_number="BB111", base_amount=1.75, unit='KG', base_price=2.50)
        self.assertTrue(result['success'])


    """ Check if the save_ingredient method is working properly when receiveing an ingredient with article number empty """
    def test_ingredient_empty_article_number(self):
        result = Ingredient.objects.save_ingredient(name="Corn", article_number="", base_amount=1.75, unit='KG', base_price=2.50)
        self.assertFalse(result['success'])


    """ Check if the save_ingredient method is working properly when receiveing objects with more than 5 characters long as article_number property """
    def test_ingredient_invalid_article_number(self):
        result = Ingredient.objects.save_ingredient(name="Corn", article_number="123456", base_amount=1.75, unit='KG', base_price=2.50)
        self.assertFalse(result['success'])


    """ Check if the save_ingredient method is working properly when receiveing an object with article number repeated """
    def test_save_ingredient_with_repeated_article_number(self):
        result = Ingredient.objects.save_ingredient(name="Corn", article_number="AA111", base_amount=1.50, unit='KG', base_price=2.50)
        self.assertFalse(result['success'])


    """ Check if the save_ingredient method is working properly when receiveing an ingredient with base amount equals to 0.00 """
    def test_ingredient_invalid_base_amount(self):
        result = Ingredient.objects.save_ingredient(name="Corn", article_number="BB123", base_amount=0.00, unit='KG', base_price=2.50)
        self.assertFalse(result['success'])


    """ Check if the save_ingredient method is working properly when receiveing an ingredient with negative base amount """
    def test_ingredient_negative_base_amount(self):
        result = Ingredient.objects.save_ingredient(name="Corn", article_number="BB123", base_amount=-3.00, unit='KG', base_price=2.50)
        self.assertFalse(result['success'])


    """ Check if the save_ingredient method is working properly when receiveing an object with unit empty """
    def test_save_ingredient_with_unit_empty(self):
        result = Ingredient.objects.save_ingredient(name="Corn", article_number="AA111", base_amount=1.50, unit='', base_price=2.50)
        self.assertFalse(result['success'])


    """ Check if the save_ingredient method is working properly when receiveing an ingredient with base price equals to 0.00 """
    def test_ingredient_invalid_base_price(self):
        result = Ingredient.objects.save_ingredient(name="Corn", article_number="BB123", base_amount=1.00, unit='KG', base_price=0.00)
        self.assertFalse(result['success'])


    """ Check if the save_ingredient method is working properly when receiveing an ingredient with negative base price """
    def test_ingredient_negative_base_price(self):
        result = Ingredient.objects.save_ingredient(name="Corn", article_number="BB123", base_amount=1.00, unit='KG', base_price=-2.50)
        self.assertFalse(result['success'])


    """ Check if the save_ingredient method is working properly when receiveing an ingredient to update """
    def test_ingredient_update(self):
        i = Ingredient.objects.get(article_number='AA111')
        updates = {"name": "BB333"}
        result = Ingredient.objects.update_ingredient(id=i.id, updates=updates)
        b = Ingredient.objects.get(article_number='AA111')
        self.assertEqual(b.name, "BB333")


    """ Check if the filter_ingredients function is working properly (filtering by article_number and name) """
    def test_filter_ingredients(self):
        # Add more objects to database
        obj1 = Ingredient.objects.save_ingredient(name="Corn", article_number="BB123", base_amount=1.00, unit='KG', base_price=2.50)
        obj2 = Ingredient.objects.save_ingredient(name="Oil", article_number="CC234", base_amount=1.00, unit='LT', base_price=2.50)
        # Querying for objects that has 1 in name or article_number.
        result = Ingredient.objects.filter_ingredients(text="1")
        self.assertEqual(result.count(), 2)
