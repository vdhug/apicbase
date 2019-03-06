from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Ingredient
from django.core import serializers
import json


""" Render index page from ingredients with all ingredients that are in the database  """
@login_required
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
@login_required
def add_ingredient(request):
	if request.method == "GET":
		context = {"ingredient": Ingredient}
		if request.session.has_key('result_message'):
			context['resultMessage'] = request.session['result_message']
			del request.session['result_message']
		return render(request, "ingredients/ingredient.html", context)


""" Render page to edit a ingredient """
@login_required
def edit_ingredient(request, id):
	try:
		ingredient = Ingredient.objects.get(pk=id)
	except Ingredient.DoesNotExist as e:
		raise Http404("Ingredient does not exist")

	context = {}

	if request.session.has_key('result_message'):
		context['resultMessage'] = request.session['result_message']
		del request.session['result_message']

	context['ingredient'] = ingredient
	return render(request, "ingredients/ingredient.html", context)


""" Render page to delete a ingredient """
@login_required
def delete_ingredient(request, id):
	try:
		ingredient = Ingredient.objects.get(pk=id)
	except Ingredient.DoesNotExist as e:
		raise Http404("Ingredient does not exist")

	if request.method == "GET":
		context = {}
		context['ingredient'] = ingredient
		return render(request, "ingredients/ingredient_delete.html", context)

	if request.method == "POST":
		result = Ingredient.objects.delete_ingredient(ingredient.id)
		request.session['result_message'] = result['message']
		return HttpResponseRedirect(reverse("add_ingredient"))


""" Receive a POST request, try to save the object and redirect to the same page with a feedback message """
@login_required
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
			'article_number': articleNumber,
			'name': name,
			'base_amount': baseAmount,
			'base_price': basePrice,
			'unit': unit,
		}

		# If id exists update the object
		if id != 'None':
			result = Ingredient.objects.update_ingredient(id, ingredient)
			request.session['result_message'] = result['message']
			url = reverse('edit_ingredient', kwargs={'id': id})
			# Redirect to edit page with feedback message
			return HttpResponseRedirect(url)
		# If id do not exist, persist the object in the database
		else:
			result = Ingredient.objects.save_ingredient(article_number=articleNumber, name=name,  base_amount=baseAmount, unit=unit, base_price=basePrice)
			request.session['result_message'] = result['message']

			return HttpResponseRedirect(reverse("add_ingredient"))


""" Filter the ingredients accordingly some text passed by the user  """
@login_required
def filter_ingredients(request):
	if request.method == "GET":
		filter = request.GET.get('filter')
		if filter == "":
			ingredients = Ingredient.objects.all()
		else:
			ingredients = Ingredient.objects.filter_ingredients(filter)

		if ingredients.count() > 5:
			""" Query for first ten  objects """
			ingredients = ingredients[0:5]
		""" Saving filter in the cache """
		request.session['last_query'] = filter
		data = serializers.serialize('json', list(ingredients))

		return JsonResponse(data, safe=False)


""" Get ingredient by article number  """
@login_required
def get_ingredient(request, articleNumber):
	if request.method == "GET":
		try:
			ingredient = Ingredient.objects.get_ingredient_by_article_number(articleNumber)
			data = serializers.serialize('json', [ingredient])
			obj = {"result": True, "object": data}
			return JsonResponse(obj, safe=False)
		except Ingredient.DoesNotExist:
			result = {"success": False}
			return JsonResponse(result, safe=False)


""" Load next 5 or the remaining ingredients object with filter applied  """
@login_required
def show_more_ingredients(request):
	if request.method == "GET":
		page = int(request.GET.get('page'))
		filter = ""
		""" Get text filter cached """
		if request.session.has_key('last_query'):
			filter = request.session['last_query']

		if filter == "":
			ingredients = Ingredient.objects.all()
		else:
			ingredients = Ingredient.objects.filter_ingredients(filter)

		if ingredients.count() >= 5*page+5:
			""" Query for another ten next objects """
			ingredients = ingredients[page*5:page*5+5]
		else:
			""" Query for lest bunch of objects """
			ingredients = ingredients[page*5:ingredients.count()]

		data = serializers.serialize('json', list(ingredients))


		return JsonResponse(data, safe=False)
