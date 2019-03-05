from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


""" View to show a little joke about the creative process of this project """
def process(request):
	context = {}
	if not request.user.is_authenticated:
		context['auth'] = "auth"
	return render(request, "home/process.html", context)


""" View to show about route of this project """
def about(request):
	context = {}
	if not request.user.is_authenticated:
		context['auth'] = "auth"
	return render(request, "home/about.html", context)

""" Render login page in GET request | authenticate user in POST request"""
def auth_login(request):
	if request.method == "GET":

		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse("index"))
		else:
			context = {"auth": "auth"}
		return render(request, "home/login.html", context)

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		context = {"auth": "auth"}
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			context['message'] = "User or password incorrect."
			return render(request, "home/login.html", context)


""" Logout user """
def auth_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))
