from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add_recipe, name="add_recipe"),
    path("save", views.save_recipe, name="save_recipe"),
    path("filter", views.filter_recipes, name="filter_recipes"),
    path("edit/<int:id>", views.edit_recipe, name="edit_recipe"),
    path("delete/<int:id>", views.delete_recipe, name="delete_recipe"),
    path("show_more", views.show_more_recipes, name="show_more_recipes"),
    path("details/<int:id>", views.details, name="details"),
]
