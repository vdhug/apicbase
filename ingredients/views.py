from django.shortcuts import render
from .models import Ingredient
# Create your views here.
def ingredients(request):
	return render(request, "ingredients/index.html")


def add_ingredient(request):
	if request.method == "GET":
		return render(request, "ingredients/ingredient.html")


def save_ingredient(request):
	if request.method == "POST":
		id = request.POST['id']
		articleNumber = request.POST['articleNumber']
		name = request.POST['name']
		baseAmount = request.POST['baseAmount']
		basePrice = request.POST['basePrice']
		unit = request.POST['unit']
		ingredient = {
			'id': id,
			'articleNumber': articleNumber,
			'name': name,
			'baseAmount': baseAmount,
			'basePrice': basePrice,
			'unit': unit,
		}

		# If id exists update the object
		if id:
			result = Ingredient.objects.update(ingredient.id, ingredients)
			context = {
				"resultMessage": result['message'],
			}
			return render(request, "ingredients/ingredient.html", context)
		else:
			result = Ingredient.objects.save_ingredient(article_number=articleNumber, name=name,  base_amount=baseAmount, unit=unit, base_price=basePrice)
			context = {
				"resultMessage": result['message'],
			}
			return render(request, "ingredients/ingredient.html", context)
