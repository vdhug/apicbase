from django.test import TestCase

from .models import Ingredient

# Create your tests here.
class ModelsTestCase(TestCase):

    def setUp(self):

        # Create ingredients.
        i1 = Ingredient.objects.create_ingredient(article_number="AA111", base_amount=1.50, unit='KG', base_price=2.50)
        i2 = Ingredient.objects.create_ingredient(article_number="BB222", base_amount=3.50, unit='G', base_price=3.50)


    """ Check if the create_ingredient method is working properly when receiveing an ingredient with article number empty """
    def test_ingredient_empty_article_number(self):
        result = Ingredient.objects.create_ingredient(article_number="", base_amount=1.75, unit='KG', base_price=2.50)
        for field, messages in result['message']:
            print(messages[0])
        self.assertEqual(result['success'], False)


    """ Check if the create_ingredient method is working properly when receiveing objects with more than 5 characters long as article_number property """
    def test_ingredient_invalid_article_number(self):
        result = Ingredient.objects.create_ingredient(article_number="123456", base_amount=1.75, unit='KG', base_price=2.50)
        for field, messages in result['message']:
            print(messages[0])
        self.assertEqual(result['success'], False)


    def test_create_ingredient_with_repeated_article_number(self):
        result = Ingredient.objects.create_ingredient(article_number="AA111", base_amount=1.50, unit='KG', base_price=2.50)
        for field, messages in result['message']:
            print(messages[0])
        self.assertEqual(result['success'], False)
