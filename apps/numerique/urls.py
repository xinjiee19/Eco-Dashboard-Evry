from django.urls import path
from . import views

urlpatterns = [
    path('', views.numerique_dashboard, name='numerique_dashboard'),
    path('list/', views.numerique_list, name='numerique_list'),
    path('add/', views.numerique_create, name='numerique_create'),
    path('update/<int:pk>/', views.numerique_update, name='numerique_update'),
    path('detail/<int:pk>/', views.numerique_detail, name='numerique_detail'),
    path('delete/<int:pk>/', views.numerique_delete, name='numerique_delete'),
]
