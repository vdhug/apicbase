from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Ingredient


# Create your views here.
def ingredients(request):
	ingredients = Ingredient.objects.get_all()
	context = {
		'ingredients': ingredients,
	}

	return render(request, "ingredients/index.html", context)


def add_ingredient(request):
	if request.method == "GET":
		context = {}
		if request.session.has_key('result_message'):
			context['resultMessage'] = request.session['result_message']
			del request.session['result_message']
		return render(request, "ingredients/ingredient.html", context)


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
			request.session['result_message'] = result['message']

			return HttpResponseRedirect(reverse("add_ingredient"))
