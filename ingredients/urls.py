from django.urls import path

from . import views

urlpatterns = [
    path("", views.ingredients, name="ingredients"),
    path("/add", views.add_ingredient, name="add_ingredient"),
    path("/save", views.save_ingredient, name="save_ingredient"),
]
