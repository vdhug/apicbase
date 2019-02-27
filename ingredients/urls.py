from django.urls import path

from . import views

urlpatterns = [
    path("", views.ingredients, name="ingredients"),
    path("add", views.add_ingredient, name="add_ingredient"),
    path("save", views.save_ingredient, name="save_ingredient"),
    path("filter", views.filter_ingredients, name="filter_ingredients"),
    path("show_more", views.show_more_ingredients, name="show_more_ingredients"),
]
