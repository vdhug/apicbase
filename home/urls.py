from django.urls import path

from . import views

urlpatterns = [
    path("", views.auth_login, name="login"),
    path("logout", views.auth_logout, name="logout"),
    path("process", views.process, name="process"),
    path("about", views.about, name="about"),
]
