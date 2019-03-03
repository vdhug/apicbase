from django.shortcuts import render


""" View to show a little joke about the creative process of this project """
def process(request):
	return render(request, "home/process.html")


""" Render login page in GET request | authenticate user in POST request"""
def login(request):
	if request.method == "GET":
		context = {"not_authenticated": True}
		return render(request, "home/login.html", context)
