from django.urls import path
from . import views

urlpatterns = [
    path('', views.sensibilisation_page, name='sensibilisation_page'),
]
