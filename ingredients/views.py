from django.shortcuts import render

# Create your views here.
def ingredients(request):
	return render(request, "ingredients/index.html")


def add_ingredient(request):
	if request.method == "GET":
		return render(request, "ingredients/ingredient.html")


def save_ingredient(request):
	if request.method == "POST":
		return render(request, "ingredients/ingredient.html")
