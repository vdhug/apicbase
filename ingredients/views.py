from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Ingredient
from django.core import serializers


""" Render index page from ingredients with all ingredients that are in the database  """
def ingredients(request):

	context = {}
	ingredients = Ingredient.objects.get_all()
	request.session['last_query'] = ""

	""" Loading first 5 results in the screen """
	if ingredients.count() > 5:
		ingredients = ingredients[0:5]
	else:
		context['all_results'] = True

	context['ingredients'] = ingredients
	return render(request, "ingredients/index.html", context)


""" Render page to create a new ingredient """
def add_ingredient(request):
	if request.method == "GET":
		context = {}
		if request.session.has_key('result_message'):
			context['resultMessage'] = request.session['result_message']
			del request.session['result_message']
		return render(request, "ingredients/ingredient.html", context)


""" Receive a POST request, try to save the object and redirect to the same page with a feedback message """
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
		# If id do not exist, persist the object in the database
		else:
			result = Ingredient.objects.save_ingredient(article_number=articleNumber, name=name,  base_amount=baseAmount, unit=unit, base_price=basePrice)
			request.session['result_message'] = result['message']

			return HttpResponseRedirect(reverse("add_ingredient"))


""" Filter the ingredients accordingly some text passed by the user  """
def filter_ingredients(request):
	if request.method == "GET":
		filter = request.GET.get('filter')

		ingredients = Ingredient.objects.filter_ingredients(filter)
		if ingredients.count() > 5:
			""" Query for first ten  objects """
			ingredients = ingredients[0:5]
		""" Saving filter in the cache """
		request.session['last_query'] = filter
		data = serializers.serialize('json', list(ingredients))

		return JsonResponse(data, safe=False)

""" Load next 5 or the remaining ingredients object with filter applied  """
def show_more_ingredients(request):
	if request.method == "GET":
		page = int(request.GET.get('page'))
		filter = ""
		""" Get text filter cached """
		if request.session.has_key('last_query'):
			filter = request.session['last_query']

		ingredients = Ingredient.objects.filter_ingredients(filter)

		if ingredients.count() >= 5*page+5:
			""" Query for another ten next objects """
			ingredients = ingredients[page*5:page*5+5]
		else:
			""" Query for lest bunch of objects """
			ingredients = ingredients[page*5:ingredients.count()]

		data = serializers.serialize('json', list(ingredients))


		return JsonResponse(data, safe=False)
