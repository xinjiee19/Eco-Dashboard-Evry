# apps/alimentation/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.foodentry_list, name='food_list'),
    path('nouveau/', views.foodentry_create, name='food_form'),
    path('detail/<int:pk>/', views.foodentry_detail, name='food_detail'),
    path('update/<int:pk>/', views.foodentry_update, name='food_update'),
    path('delete/<int:pk>/', views.foodentry_delete, name='food_delete'),
]
