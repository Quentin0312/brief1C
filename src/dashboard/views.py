from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .forms import UploadFileForm, ParamForm

from .models import Factures, Produits, Contenir
from django.db import connections

from sqlalchemy import create_engine

import pandas as pd
import numpy as np


# Fonctions -------------------------------------------
def recupererListeProduits(rows):
    listeProduits = []
    for elt in rows:
        if elt[1] not in listeProduits:
            listeProduits.append(elt[1])
    return listeProduits

def csvToBDD(dataframe):
    
    # Importation à chaques itérations
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
    
def recupererTopX(nomGraph):
    try:
        topSQL = "SELECT LAST_VALUE(param1) OVER(ORDER BY auto_increment_id ASC RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) test FROM paramgraph WHERE nomgraph ='"+ nomGraph +"' LIMIT 1"
        top = selectSQL(topSQL)
        if top == []:
            top = 10
        else:
            for elt in top:
                for subelt in elt:
                    top = subelt
    except:
        top = 10
    return top

def selectSQLtop(top):
    requeteSQL = "SELECT codeproduit, COUNT(*) AS vente FROM contenir GROUP BY codeproduit ORDER BY vente DESC LIMIT "+str(top)
    cursor = connections['default'].cursor()
    cursor.execute(requeteSQL)
    rows = cursor.fetchall() # Contient ce que le SELECT renvoie
    return rows

def nettoyageDataframe(dataframe):
    #Suppression "CustomerID"
    dataframe.drop('CustomerID', inplace=True, axis=1)
    # --------------------------------

    #Suppression doublons
    dataframe.drop_duplicates(subset=['InvoiceNo','StockCode'],inplace=True)
    # --------------------------------
    
    # Pays à supprimer
    # Unspecified
    dataframe.drop(dataframe[dataframe['Country'] == 'Unspecified'].index, inplace = True)
    # European Community
    dataframe.drop(dataframe[dataframe['Country'] == 'European Community'].index, inplace = True)
    # Channel islands
    dataframe.drop(dataframe[dataframe['Country'] == 'Channel Islands'].index, inplace = True)
    # --------------------------------

    # Suppression des avoirs
    # len == 7
    dataframe.drop(dataframe[dataframe['InvoiceNo'].str.len() == 7].index, inplace = True)
    # Quantity < 0
    dataframe.drop(dataframe[dataframe['Quantity'] <0].index, inplace = True)
    # UnitPrice == 0
    dataframe.drop(dataframe[dataframe['UnitPrice'] == 0].index, inplace = True)

    # Description ??

    # Suppression columns inutiles
    dataframe.drop('Quantity', inplace=True, axis=1)
    dataframe.drop('UnitPrice', inplace=True, axis=1)

    # Rennomer les colonne
    dataframe = dataframe.rename(columns={'InvoiceNo': 'nofacture', 'StockCode': 'codeproduit', 'InvoiceDate' : 'datefacturation', 'Country' : 'region', 'Description' : 'description'})
    
    # To date
    dataframe["datefacturation"] = pd.to_datetime(dataframe["datefacturation"])

    return dataframe

def importerProduits(df, engine):
    # ATTENTION => pas répétable : PK ! solutions=> try except ou algo manière 
    # déconseillé ? ou recup liste dans bdd et supprimer elt correspondant dans 
    # dataframe

    produitDF = df.copy() #IMPORTANT vraie copie

    # codeproduit => PK
    produitDF.drop_duplicates(subset=['codeproduit'],inplace=True)

    # Importation dans table produits
    produitDF[['codeproduit','description']].to_sql('produits', con=engine, if_exists='append', index=False)

def importerFactures(df,engine):

    factureDF = df.copy() #IMPORTANT vraie copie

    # nofacture=> PK
    factureDF.drop_duplicates(subset=['nofacture'],inplace=True)

    # Importation dans la table Factures
    factureDF[['nofacture','datefacturation','region']].to_sql('factures', con=engine, if_exists='append', index=False)

def importerContenir(df, engine):

    contenirDF = df.copy() # IMPORTANT vrai copie

    # Importation dans la table contenir
    contenirDF[['nofacture','codeproduit']].to_sql('contenir', con=engine, if_exists='append', index=False)




# Views -----------------------------------------------
def mainDashboard(request):

    return render(request,"mainDashboard.html")

def graphPays(request):

    # Requette SQL
        # TOP 5 
    rows = selectSQL("SELECT factures.region, COUNT(*) AS vente FROM factures INNER JOIN contenir ON factures.nofacture = contenir.nofacture GROUP BY factures.region ORDER BY vente DESC LIMIT 5")

    # Récupération datasets pour chart JS
    valeurs, labels = rowToVariable(rows)

    # Context
    context = {
        'labels' : labels,
        'data' : valeurs,
    }

    return render(request, "graphPays.html", context)

def graphProduits(request):

    # Situation entrée valeur top
    if request.method == "POST":
        form = ParamForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('graphProduits')

    # Recup SQL qui recupère le TOP X           ATTENTION IL FAUT METTRE EN PLACE UN SYST DE "NETTOYAGE" POUR LES ANCIENNES VALEURS...FAUT QUE C'EST PROPRE!!
    top = recupererTopX("produits")

    # Requete SQL pour récuperer datasets, nécessite top x
    rows = selectSQLtop(top)

    # Transformation rows en datasets compatible pour chart JS
    valeurs, labels = rowToVariable(rows)

    # Context
    form = ParamForm
    context = {
        'labels' : labels,
        'data' : valeurs,
        'form' : form
    }

    return render(request, "graphProduits.html", context)

def upload_file(request):

    # Etape 2: Situation POST
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        
        # Debut "script" d'importation
        df = pd.read_csv(file)

        # Ici fonction de nettoyage
        df = nettoyageDataframe(df)

        # Importation dans la BDD
        engine = create_engine('postgresql://postgres:azerty@localhost:5432/brief1C')

            # Table produits
        importerProduits(df, engine)

            # Table facture
        importerFactures(df, engine)

            # Table contenir
        importerContenir(df, engine)

        return HttpResponse("C'est fait !")
    
    # Etape 1
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


    
