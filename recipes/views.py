from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ingredients.models import Ingredient
from .models import Recipe, IngredientOfRecipe
from django.core import serializers
from django.http import Http404


# Create your views here.
def index(request):
	context = {}
	recipes = Recipe.objects.all()
	request.session['last_query'] = ""

	""" Loading first 5 results in the screen """
	if recipes.count() > 5:
		recipes = recipes[0:5]
	else:
		context['all_results'] = True

	context['recipes'] = recipes
	return render(request, "recipes/index.html", context)


""" Render page to create a new recipe """
def add_recipe(request):
	if request.method == "GET":
		context = {"recipe": Recipe}
		if request.session.has_key('result_message'):
			context['resultMessage'] = request.session['result_message']
			del request.session['result_message']
		return render(request, "recipes/recipe.html", context)


""" Render page to edit a recipe """
def edit_recipe(request, id):
	try:
		recipe = Recipe.objects.get(pk=id)
	except Recipe.DoesNotExist as e:
		raise Http404("Recipe does not exist")
	context = {}

	if request.session.has_key('result_message'):
		context['resultMessage'] = request.session['result_message']
		del request.session['result_message']

	context['recipe'] = recipe
	return render(request, "recipes/recipe.html", context)


""" Render view to see details about one recipe """
def details(request, id):
	try:
		recipe = Recipe.objects.get(pk=id)
	except Recipe.DoesNotExist:
		raise Http404("Recipe does not exist")

	context = {
		"recipe": recipe,
	}
	return render(request, "recipes/details.html", context)


def save_recipe(request):
	if request.method == "POST":
		q = request.POST
		articleNumbers = q.getlist('articleNumber')
		quantities = q.getlist('quantity')
		""" Create dictionary with the format "articleNumber": quantity """
		ingredients = dict(zip(articleNumbers, quantities))
		id = q['id']
		# If id exists update the object
		if id != 'None':
			""" Retrieve recipe object """
			updates = {
				"name": q['nameOfRecipe'],
				"description": q['description'],
				"method_of_preparation": q['method'],
			}
			result = Recipe.objects.update_recipe(id=id, updates=updates)
			if result['success']:
				recipe = Recipe.objects.get(pk=id)
				""" Loop through all the ingredients of this recipe to check if was deleted or updated """
				for ingredientOfRecipe in recipe.ingredients.all():
					""" Store the article number of the ingredient """
					articleNumber = ingredientOfRecipe.ingredient.article_number
					""" Check if the ingredient was deleted """
					if articleNumber in ingredients.keys():
						""" Check if the ingredient was updated """
						if ingredientOfRecipe.quantity != ingredients[articleNumber]:
							# Update the quantity of this ingredient of recipe
							updates = {"quantity": ingredients[articleNumber]}
							IngredientOfRecipe.objects.update_ingredient_of_recipe(ingredientOfRecipe.id, updates)
							# Delete this pair value, was already updated
							del ingredients[articleNumber]
					else:
						# This ingredient was deleted by the user
						ingredientOfRecipe.delete()

				""" Loop through all the new ingredients that was added to the recipe  """
				for i in ingredients.keys():
					""" Retrive the ingredient object via article number """
					ingredient = Ingredient.objects.get_ingredient_by_article_number(i)
					""" Persist the IngredientOfRecipe object """
					IngredientOfRecipe.objects.add_ingredient_of_recipe(recipe=recipe, ingredient=ingredient, quantity=ingredients[i])

				request.session['result_message'] = result['message']
				url = reverse('edit_recipe', kwargs={'id': id})
				# Redirect to edit page with feedback message
				return HttpResponseRedirect(url)
		else:
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


""" Filter the recipes accordingly some text passed by the user  """
def filter_recipes(request):
	if request.method == "GET":
		filter = request.GET.get('filter')

		recipes = Recipe.objects.filter_recipes(filter)
		if recipes.count() > 5:
			""" Query for first ten  objects """
			recipes = recipes[0:5]
		""" Saving filter in the cache """
		request.session['last_query'] = filter

		result = []
		for recipe in recipes:
			result.append((serializers.serialize('json', [ recipe, ]), recipe.cost))

		return JsonResponse(result, safe=False)
