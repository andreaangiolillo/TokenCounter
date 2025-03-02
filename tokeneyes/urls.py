from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path('calculate-tokens/', views.calculate_tokens, name='calculate_tokens'),
]