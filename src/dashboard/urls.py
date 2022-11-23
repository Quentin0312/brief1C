from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainDashboard, name="mainDashboard")
]