from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import Factures, Produits, Contenir

# Create your views here.
test =[]
def mainDashboard(request):
    for elt in Produits.objects.raw('SELECT * FROM produits'):
        test.append(elt) 
    print(test)

    return HttpResponse(test)