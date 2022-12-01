from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db import connections

from . forms import UploadFileForm

from .models import Factures, Produits, Contenir

import pandas as pd

from django_pivot.pivot import pivot

# Fonctions
def csvToBDD(dataframe):
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

def recupererListeProduits(rows):
    listeProduits = []
    for elt in rows:
        if elt[1] not in listeProduits:
            listeProduits.append(elt[1])
    return listeProduits

def recupererListePays(rows):
    listePays = []
    for elt in rows:
        if elt[0] not in listePays:
            listePays.append(elt[0])
    return listePays

def rowToVariable(rows):
    labels = []
    valeurs = []
    print(rows)
    for elt in rows:
        for subElt in elt:
            if isinstance(subElt, str):
                labels.append(subElt)
            else:
                valeurs.append(subElt)
    
    print("Labels=> "+str(labels))
    print("Valeurs=> "+str(valeurs))
    
    return valeurs,labels

def produitGraphDataset(listePays,listeProduits,rows):
    dictionnaireData = {}
    # Par pays
    for pays in listePays:
        print(pays)

        listeData = [] # Contient liste des data pour 1 pays donc pour une serie de data pour chart js
        # Par produit
        for produit in listeProduits:
            # Verifie toutes les lignes
            for elt in rows:
                trouvee = False
                if pays in elt and produit in elt: # Si dans cette ligne le pays et le produit correspond => recupere la vente
                    listeData.append(elt[2])
                    trouvee = True

            # Si pas trouvé ajoute 0 a la liste pour respecter "format data" nécessaire pour chart js
            if trouvee == False:
                listeData.append(0)

        dictionnaireData[pays] = listeData # À envoyer dans le contexte pour chart JS
        listeData = [] # Réinitialiser pour pays suivant
    return dictionnaireData

def selectSQL(scriptSQL):
    cursor = connections['default'].cursor()
    cursor.execute(scriptSQL)
    rows = cursor.fetchall() # Contient ce que le SELECT renvoie
    return rows
    

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

    # row to variable
    valeurs, labels = rowToVariable(rows)

    # Context
    context = {
        'labels' : labels,
        'data' : valeurs,
    }

    return render(request, "graphPays.html", context)

def graphProduits(request):

    # Requete SQL
    cursor = connections['default'].cursor()
    cursor.execute("SELECT codeproduit, COUNT(*) AS vente FROM contenir GROUP BY codeproduit ORDER BY vente DESC LIMIT 10")
    rows = cursor.fetchall()

    valeurs, labels = rowToVariable(rows)

    # Context
    context = {
        'labels' : labels,
        'data' : valeurs,
    }

    return render(request, "graphProduits.html", context)

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

def graphTCD(request):

    # Requette SQL
    rows = selectSQL('SELECT factures.region, contenir.codeproduit, COUNT(*) AS vente FROM contenir INNER JOIN factures ON factures.nofacture = contenir.nofacture GROUP BY factures.region, contenir.codeproduit ORDER BY vente DESC')

    # Récuperer la liste des produits
    listeProduits = recupererListeProduits(rows)

    # Récuperer la liste des pays
    listePays = recupererListePays(rows)

    # Produit datasets pour chart JS
    dictionnaireData = produitGraphDataset(listePays,listeProduits,rows)

    context={
        'labels' : listeProduits,
        'dicoData' : dictionnaireData,
        'listePays': listePays 
    }

    return render(request, "graphTCD.html", context)


    
