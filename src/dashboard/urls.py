from django.urls import path
from . import views
# from dashboard.views import upload_file

urlpatterns = [
    path('', views.mainDashboard, name="mainDashboard"),
    path('add', views.upload_file, name='add'),
    path('graphPays', views.graphPays, name="graphPays"),
    path('graphProduits', views.graphProduits, name="graphProduits"),
    path('graphTCD', views.graphTCD, name="graphTCD"),
    path('graph3', views.graph3, name='graph3'),
    path('testActuel', views.testImportationToutLesTops, name='testActuel'),
    path('upload_confirmation', views.upload_confirmation, name="upload_confirmation"),
    path('testValidationImport', views.testValidationImport, name="testValidationImport")
]