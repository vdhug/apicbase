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
		return render(request, "recipes/recipe.html")
