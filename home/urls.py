from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("process", views.process, name="process"),
]
