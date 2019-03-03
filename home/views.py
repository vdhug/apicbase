from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


""" View to show a little joke about the creative process of this project """
def process(request):
	return render(request, "home/process.html")


""" Render login page in GET request | authenticate user in POST request"""
def auth_login(request):
	if request.method == "GET":
		context = {"auth": "auth"}
		return render(request, "home/login.html", context)

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))


""" Logout user """
def auth_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))
