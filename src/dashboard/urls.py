from django.urls import path
from . import views
# from dashboard.views import upload_file

urlpatterns = [
    path('', views.mainDashboard, name="mainDashboard"),
    path('add', views.add, name="add"),
    path('list', views.upload_file, name='list')
]