from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db import connections

from . forms import UploadFileForm

from .models import Factures, Produits, Contenir

import pandas as pd

# Fonctions
def csvToBDD(dataframe):
    from datetime import datetime
    dateDebut = datetime.now()
    iterations = 0
    for elt in dataframe.loc:
        iterations +=1
        print(iterations)

        cursor = connections['default'].cursor()

        # Ordre important => FK...
        # Importation dans la table Porduits
        try: # codeproduit = PK mais apparait pls fois, ceci ne pose pas probleme pour la suite ... pour l'instant
            cursor.execute("INSERT INTO produits(codeproduit) VALUES( %s )", [elt[1]])
        except:
            pass

        # Importation dans la table factures
        try: # nofacture = PK mais redondante dans le csv => cause donc erreur, ignorer n'est pas un probleme sauf si le csv ne correspond pas à ce qu'attendu
            cursor.execute("INSERT INTO factures(nofacture,datefacturation,region) VALUES( %s , %s , %s )", [elt[0], elt[4], elt[7]])
        except:
            pass
        
        # Importation dans la table contenir
        try:
            cursor.execute("INSERT INTO contenir(nofacture,codeproduit,qte) VALUES ( %s , %s , %s )",[elt[0], elt[1], elt[3].item()]) # .item() transforme numpy.int64 en int "classique" accépté par postgreSQL
        except:
            pass
    dateFin = datetime.now()
    print("dateDebut=>"+str(dateDebut)+"  ;"+"dateFin=>"+str(dateFin))
# Attention type de nofacture dans BDD à changer => varchar

# Views
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

# découper l'interieur en fonctions
def graphPays(request):

    # Requette SQL
    cursor = connections['default'].cursor()
    # TOP 10 seulement
    cursor.execute("SELECT factures.region, COUNT(*) AS vente FROM factures INNER JOIN contenir ON factures.nofacture = contenir.nofacture GROUP BY factures.region ORDER BY vente DESC LIMIT 5")
    rows = cursor.fetchall()
    print(rows)
    print(type(rows))

    # BDD to variable
    labels = []
    valeurs = []

    for elt in rows:
        for subElt in elt:
            if isinstance(subElt, str):
                labels.append(subElt)
            else:
                valeurs.append(subElt)
    
    print("Labels=> "+str(labels))
    print("Valeurs=> "+str(valeurs))

    # Context
    context = {
        'labels' : labels,
        'data' : valeurs,
    }

    return render(request, "graphPays.html", context)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file'] # Juste à partir de la le script peut se lancer ? Car pas besoin de save le fichiers csv juste l'enregistrer en pandas dataframe ?
        
        # Debut "script" d'importation
        df = pd.read_csv(file)
        # Ici aplliquer fonction de nettoyage qui renvoie un dataframe à reutiliser juste après
        csvToBDD(df)

        return HttpResponse("Nom du fichiers: "+str(df))
    # Etape 1 : Ouverture du lien => GET
    else:
        form = UploadFileForm()
    return render(request, 'add.html', context={'form':form}) #Actualise la page en ajoutant le form file en context

