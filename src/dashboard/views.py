from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db import connections


from .models import Factures, Produits, Contenir

# Create your views here.
def mainDashboard(request):
    # for elt in Factures.objects.raw('SELECT * FROM factures'):
    #     test = elt.region
    date = '2010-01-12'
    region ='United Kingdom'
    stockcode = '85123A'
    # Produits.objects.raw("INSERT INTO produits VALUES ('85123A')")
    cursor = connections['default'].cursor()
    cursor.execute("INSERT INTO produits(codeproduit) VALUES( %s )", [stockcode])

    return HttpResponse("Ouais...")