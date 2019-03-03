from django.shortcuts import render


""" View to show a little joke about the creative process of this project """
def process(request):
	return render(request, "home/process.html")


""" Render login page in GET request | authenticate user in POST request"""
def login(request):
	if request.method == "GET":
		return render(request, "home/login.html")
