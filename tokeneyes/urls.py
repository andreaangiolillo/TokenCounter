from django.urls import path
from . import views

urlpatterns = [
    path("", views.calculate_tokens, name = "calculate_tokens"),
    path("about", views.about, name = "about"),
]
