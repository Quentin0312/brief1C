from django.urls import path
from . import views
# from dashboard.views import upload_file

urlpatterns = [
    path('', views.mainDashboard, name="mainDashboard"),
    path('add', views.upload_file, name='add')
]