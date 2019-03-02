from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add_recipe, name="add_recipe"),
    path("save", views.save_recipe, name="save_recipe"),
    path("filter", views.filter_recipes, name="filter_recipes"),
    path("edit/<int:id>", views.edit_recipe, name="edit_recipe"),
    path("details/<int:id>", views.details, name="details"),
]
