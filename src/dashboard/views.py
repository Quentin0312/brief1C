from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db import connections

from . forms import UploadFileForm

from .models import Factures, Produits, Contenir

import pandas as pd

def csvToBDD(dataframe):

    for elt in dataframe.loc:

        cursor = connections['default'].cursor()

        cursor.execute("INSERT INTO produits(codeproduit) VALUES( %s )", [elt[1]])
        cursor.execute("INSERT INTO factures(nofacture,region) VALUES( %s , %s )", [elt[0], elt[7]]) # Manque date
        cursor.execute("INSERT INTO contenir(nofacture,codeproduit,qte) VALUES ( %s , %s , %s )",[elt[0], elt[1], elt[3]])

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

def add(request):
    return render(request, "add.html")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file'] # Juste à partir de la le script peut se lancer ? Car pas besoin de save le fichiers csv juste l'enregistrer en pandas dataframe ?
        df = pd.read_csv(file)
        csvToBDD(df)

        return HttpResponse("Nom du fichiers: "+str(df))
    # Etape 1 : Ouverture du lien => GET
    else:
        form = UploadFileForm()
    return render(request, 'add.html', context={'form':form})

