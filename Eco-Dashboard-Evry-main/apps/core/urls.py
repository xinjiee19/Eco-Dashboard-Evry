from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    path('send-reminder/', views.send_reminder_email, name='send_reminder'),
    path('api/dashboard-emissions/', views.dashboard_emissions_api, name='dashboard_emissions_api'),
    path('api/statistics-data/', views.statistics_api, name='statistics_data_api'),
    path('export-data/', views.export_data_view, name='export_data'),
    path('statistics/', views.statistics_view, name='statistics'),
]
