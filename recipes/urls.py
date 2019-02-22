from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add_recipe, name="add_recipe"),
    path("save", views.save_recipe, name="save_recipe"),
]
