from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, "recipes/index.html")


def add_recipe(request):
	if request.method == "GET":
		return render(request, "recipes/recipe.html")


def save_recipe(request):
	if request.method == "POST":
		return render(request, "recipes/recipe.html")
