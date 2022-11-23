from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db import connections


from .models import Factures, Produits, Contenir

# Attention type de nofacture dans BDD à changer => varchar

# Create your views here.
def mainDashboard(request):

    # for elt in Factures.objects.raw('SELECT * FROM factures'):
    #     test = elt.region
    #---------------------------------------------------------------------------------------------
    # date = '2010-01-12'
    # region ='United Kingdom'
    # stockcode = '85123A'
    # invoiceno = 536365
    # invoicedate = '2010-01-12'
    # country = 'United Kingdom'
    # qte = 6

    # cursor = connections['default'].cursor()
    # cursor.execute("INSERT INTO produits(codeproduit) VALUES( %s )", [stockcode])
    # cursor.execute("INSERT INTO factures(nofacture,datefacturation,region) VALUES( %s , %s , %s )", [invoiceno, invoicedate, country])
    # cursor.execute("INSERT INTO contenir(nofacture,codeproduit,qte) VALUES ( %s , %s , %s )",[invoiceno, stockcode, qte])
    #---------------------------------------------------------------------------------------------

    return render(request,"mainDashboard.html")