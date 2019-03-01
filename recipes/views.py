from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ingredients.models import Ingredient
from .models import Recipe, IngredientOfRecipe
from django.core import serializers

# Create your views here.
def index(request):
	return render(request, "recipes/index.html")


""" Render page to create a new recipe """
def add_recipe(request):
	if request.method == "GET":
		context = {"recipe": Recipe}
		if request.session.has_key('result_message'):
			context['resultMessage'] = request.session['result_message']
			del request.session['result_message']
		return render(request, "recipes/recipe.html", context)


def save_recipe(request):
	if request.method == "POST":
		q = request.POST
		articleNumbers = q.getlist('articleNumber')
		quantities = q.getlist('quantity')

		""" Create dictionary with the format "articleNumber": quantity """
		ingredients = dict(zip(articleNumbers, quantities))

		""" Persist recipe in the database """
		result = Recipe.objects.save_recipe(name=q['nameOfRecipe'], description=q['description'], method_of_preparation=q['method'])

		""" Loop through all the ingredients in the recipe and persist them """
		for i in ingredients.keys():
			""" Retrive the ingredient object via article number """
			ingredient = Ingredient.objects.get_ingredient_by_article_number(i)
			""" Persist the IngredientOfRecipe object """
			IngredientOfRecipe.objects.add_ingredient_of_recipe(recipe=result['object'], ingredient=ingredient, quantity=ingredients[i])

		request.session['result_message'] = result['message']

		return HttpResponseRedirect(reverse("add_recipe"))
