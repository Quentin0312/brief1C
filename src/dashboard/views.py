from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .forms import UploadFileForm, ParamForm, graph3Form

from .models import Factures, Produits, Contenir
from django.db import connections

from sqlalchemy import create_engine

import pandas as pd
import numpy as np

import os


# Fonctions -------------------------------------------
def recupererListeProduitsTCD(rows):
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

def recupererListePaysTCD(rows):
    listePays = []
    for elt in rows:
        if elt[0] not in listePays:
            listePays.append(elt[0])
    return listePays

def rowToVariable(rows):
    labels = []
    valeurs = []
    # print(rows)
    for elt in rows:
        for subElt in elt:
            if isinstance(subElt, str):
                labels.append(subElt)
            else:
                valeurs.append(subElt)
    
    # print("Labels=> "+str(labels))
    # print("Valeurs=> "+str(valeurs))
    
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
        print(top)
        if top == []:
            top = 10
        else:
            for elt in top:
                for subelt in elt:
                    top = subelt
    except:
        top = 10
    return top

def selectSQLproduit(top):
    # Si valeur vide entrée
    if top == None:
        top = 10

    requeteSQL = "SELECT codeproduit, COUNT(*) AS vente FROM contenir GROUP BY codeproduit ORDER BY vente DESC LIMIT "+str(top)
    cursor = connections['default'].cursor()
    cursor.execute(requeteSQL)
    rows = cursor.fetchall() # Contient ce que le SELECT renvoie
    return rows

def selectSQLpays(top):
    # Si valeur vide entrée
    if top == None:
        top = 10

    requeteSQL = "SELECT factures.region, COUNT(*) AS vente FROM factures INNER JOIN contenir ON factures.nofacture = contenir.nofacture GROUP BY factures.region ORDER BY vente DESC LIMIT "+str(top)
    cursor = connections['default'].cursor()
    cursor.execute(requeteSQL)
    rows = cursor.fetchall() # Contient ce que le SELECT renvoie
    return rows

def nettoyageDataframe(dataframe):
    avantNettoyage = len(dataframe)

    #Suppression "CustomerID"
    dataframe.drop('CustomerID', inplace=True, axis=1)

    # uppercase les codeproduits pour la bonne correspondance de la FK dans la BDD
    dataframe['StockCode'] = dataframe['StockCode'].str.upper()

    # Suppression doublons
    dataframe.drop_duplicates(subset=['InvoiceNo','StockCode'],inplace=True)
    
    # Pays à supprimer : Unspecified
    dataframe.drop(dataframe[dataframe['Country'] == 'Unspecified'].index, inplace = True)

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

    # Feedback data perdues
    apresNettoyage = len(dataframe)
    reste = avantNettoyage - apresNettoyage
    pourcentageDataPerdues = reste / avantNettoyage *100
    print("Pourcentage data perdues durant nettoyage=======> "+str(pourcentageDataPerdues))
    return dataframe

def importerProduits(df, engine):

    # Modification à effectué sur copie pour pas influencer les autres imports
    produitDF = df.copy() #IMPORTANT vraie copie

    # codeproduit => PK : Suppression des doublons dans le dataframe
    produitDF.drop_duplicates(subset=['codeproduit'], inplace=True)

    # Situtation import initial
    querySQLtest = pd.read_sql_query('''SELECT * FROM produits''', engine)
    if "Empty DataFrame" in str(querySQLtest):  # Vérifie si la table est vide

        print("Import initial produits")

        # Importation dans la table Produits
        produitDF[['codeproduit','description']].to_sql('produits', con=engine, if_exists='append', index=False)
    
    # Situation import supplémentaire
    else:
        print('Import suppl produits')
        
        # Création dataframe à partir SQL query
        querySQL = pd.read_sql_query('''SELECT * FROM produits''', engine)

        #Création des dataframes à concaténer
        dataframeSQL = pd.DataFrame(querySQL, columns=['codeproduit','description'])
        dataframeSQLcopie = dataframeSQL.copy() # dataframeSQL en double pour ne garder seulement que les nouvelles data via drop_duplicates par la suite
        dataframeProduit = produitDF[['codeproduit','description']]
        
        # Concatenation
        dataframeConcatenee = pd.concat([dataframeProduit, dataframeSQL, dataframeSQLcopie])

        # Suppression des doublons
        dataframeConcatenee.drop_duplicates(subset=['codeproduit'], inplace=True, keep=False)

        # Importation dans BDD
        dataframeConcatenee.to_sql('produits', con=engine, if_exists='append', index=False)

def importerFactures(df,engine):

    # Modification à effectué sur copie pour pas influencer les autres imports
    factureDF = df.copy() #IMPORTANT vraie copie

    # nofacture => PK donc suppression des donblons en amont necessaire
    factureDF.drop_duplicates(subset=['nofacture'],inplace=True)

    # Situtation import initial
    querySQLtest = pd.read_sql_query('''SELECT * FROM factures''', engine)
    if "Empty DataFrame" in str(querySQLtest): # Vérifie si la table est vide

        print("Import initial factures")

        # Importation dans la table Factures
        factureDF[['nofacture','datefacturation','region']].to_sql('factures', con=engine, if_exists='append', index=False)

    # Situation import supplémentaire
    else:
        print('Import suppl factures')

        # Création dataframe à partir SQL query
        querySQL = pd.read_sql_query('''SELECT * FROM factures''', engine)

        # Création des dataframes à concaténer
        dataframeSQL = pd.DataFrame(querySQL, columns=['nofacture','datefacturation','region'])
        dataframeSQLcopie = dataframeSQL.copy()  # dataframeSQL en double pour ne garder seulement que les nouvelles data via drop_duplicates par la suite
        dataframeFacture = factureDF[['nofacture','datefacturation','region']]

        # Concatenation
        dataframeConcatenee = pd.concat([dataframeFacture, dataframeSQL, dataframeSQLcopie])

        # Suppression des doublons
        dataframeConcatenee.drop_duplicates(subset=['nofacture'], inplace=True, keep=False)

        # Importation dans la table factures
        dataframeConcatenee.to_sql('factures', con=engine, if_exists='append', index=False)

def importerContenir(df, engine):

    # Modification à effectuer sur copie pour pas influencer les autres imports
    contenirDF = df.copy() # IMPORTANT vrai copie

    # Situation import initial
    querySQLtest = pd.read_sql_query('''SELECT * FROM contenir''', engine)
    if "Empty DataFrame" in str(querySQLtest): # Vérifie si la table est vide

        print("Import initial contenir")

        # Import dans la table contenir
        contenirDF[['nofacture','codeproduit']].to_sql('contenir', con=engine, if_exists='append', index=False)
    
    # Situtation import suppl
    else:
        print("Import suppl contenir")

        # Création dataframe à partir SQL query
        querySQL = pd.read_sql_query('''SELECT * FROM contenir''', engine)

        # Création dataframes à concaténer
        dataframeSQL = pd.DataFrame(querySQL, columns=['nofacture','codeproduit'])
        dataframeSQLcopie = dataframeSQL.copy()  # dataframeSQL en double pour ne garder seulement que les nouvelles data via drop_duplicates par la suite
        dataframeContenir = contenirDF[['nofacture','codeproduit']]

        # Concatenation
        dataframeConcatenee = pd.concat([dataframeContenir, dataframeSQL, dataframeSQLcopie])

        # Suppression des doublons
        dataframeConcatenee.drop_duplicates(subset=['nofacture','codeproduit'], inplace=True, keep=False)

        # Importation dans BDD
        dataframeConcatenee.to_sql('contenir', con=engine, if_exists='append', index=False)

def importer(df):
    engine = create_engine('postgresql://postgres:azerty@localhost:5432/brief1C')

    # Table produits
    importerProduits(df, engine)

    # Table facture
    importerFactures(df, engine)

    # Table contenir
    importerContenir(df, engine)

def recupererParam2(nomGraph):
    try:
        SQL = "SELECT LAST_VALUE(param2) OVER(ORDER BY auto_increment_id ASC RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) test FROM paramgraph WHERE nomgraph ='"+nomGraph+"' LIMIT 1"
        query = selectSQL(SQL)

        if query == [] and nomGraph == "graph3ProduitsPays":
            paramCible = 'United Kingdom'
        elif query == [] and nomGraph == "graph3PaysProduits":
            paramCible = '85123A'
        else:
            for elt in query:
                for subelt in elt:
                    paramCible = subelt
    except:
        if nomGraph == 'graph3ProduitsPays':
            paramCible = 'United Kingdom'
        else:
            paramCible = '85123A'
    return paramCible

def requeteSQLgraph3_1(paysCible,topCible):
    requeteSQL = "SELECT contenir.codeproduit, COUNT(*) AS vente FROM contenir INNER JOIN factures ON factures.nofacture = contenir.nofacture WHERE region = '" + paysCible + "' GROUP BY factures.region, contenir.codeproduit ORDER BY vente DESC LIMIT " + str(topCible)
    cursor = connections['default'].cursor()
    cursor.execute(requeteSQL)
    rows = cursor.fetchall() # Contient ce que le SELECT renvoie
    return rows

def requeteSQLgraph3_2(produitCible,topCible):
    requeteSQL = "SELECT factures.region, COUNT(*) AS vente FROM contenir INNER JOIN factures ON factures.nofacture = contenir.nofacture WHERE codeproduit = '" + produitCible + "' GROUP BY factures.region, contenir.codeproduit ORDER BY vente DESC LIMIT " + str(topCible)
    cursor = connections['default'].cursor()
    cursor.execute(requeteSQL)
    rows = cursor.fetchall() # Contient ce que le SELECT renvoie
    return rows

def produireLabelsEtDataGraph3(nomGraph, noGraph):

    # Recupérer top
    topCible = recupererTopX(nomGraph)

    # Récupérer paysCible
    paramCible = recupererParam2(nomGraph)

    # Requete SQL si graph 1
    if noGraph == 1:
        rows = requeteSQLgraph3_1(paramCible, topCible)
    # Requete SQL si graph 2
    elif noGraph == 2:
        rows = requeteSQLgraph3_2(paramCible, topCible)


    # Rows to labels et data lists
    valeurs, labels = rowToVariable(rows)
    # print(valeurs)
    return valeurs, labels, topCible, paramCible

def recupererListePays():
    # Requete SQL
    rows = selectSQL("SELECT region FROM factures GROUP BY region ORDER BY region ASC")
    
    # Transforme tuple dans liste à liste normal
    listePays = []
    for elt in rows:
        for subelt in elt:
            eltModifie = subelt.replace(",","")
            listePays.append(eltModifie)

    return listePays

def recupererListeProduits():

    # Requete SQL
    rows = selectSQL("SELECT codeproduit FROM produits GROUP BY codeproduit ORDER BY codeproduit ASC")    
    
    # Transforme tuple dans liste à liste normal
    listeProduits = []
    for elt in rows:
        for subelt in elt:
            eltModifie = subelt.replace(",","")
            listeProduits.append(eltModifie)

    return listeProduits

# Views -----------------------------------------------
def mainDashboard(request):
    if request.user.is_authenticated == True:
        print(request.user.is_authenticated)

        # Test à supprimer
        request.session["test"] = 123 

        return render(request,"mainDashboard.html")
        # return redirect('testValidationImport', valeurTest = 12)
    else:
        return redirect('/login') 

def graphPays(request):
    # Vérification que user est login
    if request.user.is_authenticated ==False:
        return redirect('login')
    
    # Situation entrée valeur top
    if request.method == "POST":
        form = ParamForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('graphPays')
    
    # Récuperer le top X
    top = recupererTopX("pays")

    # Requette SQL
    rows = selectSQLpays(top)

    # Transformation rows en datasets compatible pour chart JS
    valeurs, labels = rowToVariable(rows)

    # Modal
    # Conctituer les datas et labels
    dicoDataModal = {}
    dicoLabelsModal = {}
    for elt in labels:
        rows = requeteSQLgraph3_1(elt, 5) # À rendre dynamique (TOP X et et 5)
        valeurs0, labels0 = rowToVariable(rows)
        dicoDataModal[elt] = valeurs0
        dicoLabelsModal[elt]= labels0

    # Context
    form = ParamForm
    context = {
        'labels' : labels,
        'data' : valeurs,
        'form' : form,
        'dicoDataModal' : dicoDataModal,
        'dicoLabelsModal' : dicoLabelsModal
    }

    return render(request, "graphPays.html", context)

def graphProduits(request):
    # Vérification que user est login
    if request.user.is_authenticated ==False:
        return redirect('login')

    # Situation entrée valeur top
    if request.method == "POST":
        form = ParamForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('graphProduits')

    # Recup SQL qui recupère le TOP X           ATTENTION IL FAUT METTRE EN PLACE UN SYST DE "NETTOYAGE" POUR LES ANCIENNES VALEURS...FAUT QUE C'EST PROPRE!!
    top = recupererTopX("produits")

    # Requete SQL pour récuperer datasets, nécessite top x
    rows = selectSQLproduit(top)

    # Transformation rows en datasets compatible pour chart JS
    valeurs, labels = rowToVariable(rows)

    # Modal
    # Constituer les datas et labels
    dicoDataModal = {}
    dicoLabelsModal = {}
    for elt in labels:
        rows = requeteSQLgraph3_2(elt, 5) # À rendre dynamique (TOP X et et 5)
        valeurs0, labels0 = rowToVariable(rows)
        dicoDataModal[elt] = valeurs0
        dicoLabelsModal[elt]= labels0
    
    # Context
    form = ParamForm
    context = {
        'labels' : labels,
        'data' : valeurs,
        'form' : form,
        'dicoDataModal' : dicoDataModal,
        'dicoLabelsModal' : dicoLabelsModal
    }

    return render(request, "graphProduits.html", context)

def upload_file(request):
    # Vérification que user est login
    if request.user.is_authenticated ==False:
        return redirect('login')

    # Etape 2: Situation POST
    if request.method == 'POST':

        # Form file
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        
        # Création dataframe à partir csv uploadé
        df = pd.read_csv(file, encoding='ISO-8859-1')

        # Nettoyage du dataframe
        df = nettoyageDataframe(df)

        # TEST À SUPPR
        df = df.to_json() 
        request.session['test'] = df
        # Importation dans la BDD
        # importer(df)

        # return HttpResponse("C'est fait !")
        # return redirect('/dashboard/upload_confirmation', df = "test", feedback = "Ceci est un feedback !")
        return render(request, 'add.html', context={'form':form})
    # Etape 1
    else:
        form = UploadFileForm()
    return render(request, 'add.html', context={'form':form}) #Actualise la page en ajoutant le form file en context

def graphTCD(request):
    # Vérification que user est login
    if request.user.is_authenticated ==False:
        return redirect('login')

    # Requette SQL
    rows = selectSQL('SELECT factures.region, contenir.codeproduit, COUNT(*) AS vente FROM contenir INNER JOIN factures ON factures.nofacture = contenir.nofacture GROUP BY factures.region, contenir.codeproduit ORDER BY vente DESC LIMIT 1000')

    # Récuperer la liste des produits
    listeProduits = recupererListeProduitsTCD(rows)

    # Récuperer la liste des pays
    listePays = recupererListePaysTCD(rows)

    # Produit datasets pour chart JS
    dictionnaireData = produitGraphDataset(listePays,listeProduits,rows)

    context={
        'labels' : listeProduits,
        'dicoData' : dictionnaireData,
        'listePays': listePays 
    }

    return render(request, "graphTCD.html", context)

def graph3(request):
    # Vérification que user est login
    if request.user.is_authenticated ==False:
        return redirect('login')

    # Situation entrée valeur top
    if request.method == "POST":
        form = graph3Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('graph3')

    # Données graph 1 Top produits par pays
    valeurs1, labels1, topCible1, paramCible1 = produireLabelsEtDataGraph3("graph3ProduitsPays", 1)
    
    # Données graph 2 Top pays par praoduits
    valeurs2, labels2, topCible2, paramCible2 = produireLabelsEtDataGraph3("graph3PaysProduits", 2) 

    # Récup la liste des pays pour l'input list dans HTML
    listePays = recupererListePays() 

    # Récup liste produits pour l'input list dans HTML
    listeProduits = recupererListeProduits()


    # Context
    form = graph3Form
    context = {
        # Form
        'form' : form,

        # Graph 1 Top produits par pays
        'labels1' : labels1,
        'data1' : valeurs1,
        'pays1' : paramCible1,
        'top1' : topCible1,
        # Pour list input
        'listePays' : listePays,
        'listeProduits' : listeProduits,

        # Graph 2 Top pays par produits
        'labels2' : labels2,
        'data2' : valeurs2,
        'top2' : topCible2,
        'produits2' : paramCible2
    }

    return render(request, "graph3.html", context)

def upload_confirmation(request, df, feedback):

    return HttpResponse(df, feedback)

# Test/Labos------------------------------------------
def testImportationToutLesTops(request):# NON trop long...
    # Vérification que user est login
    if request.user.is_authenticated ==False:
        return redirect('login')

    dicoDataTotal = {}

    # Liste Pays
    listePays = recupererListePays()

    for elt in listePays:
        # Récupérer datas 
        rows = requeteSQLgraph3_1(elt, 5)
        valeurs, labels = rowToVariable(rows)
        # Insérer/Enregistrer dans dictionnaire
        dicoDataTotal[elt] = valeurs

    # Liste Produits
    listeProduits = recupererListeProduits()
    i = 0
    for elt in listeProduits:
        i+=1
        if i > 100:
            break
        # Récupérer datas 
        rows = requeteSQLgraph3_2(elt, 5)
        valeurs, labels = rowToVariable(rows)
        # Insérer/Enregistrer dans dictionnaire
        dicoDataTotal[elt] = valeurs


    # Faire importer tout les tops5 pour voir si temps pas trop longs ou optimisable
    # Obj => graph3, utiliser chart.update() => necessite donc toutes les data préchargé dans chart JS
    return HttpResponse(str(dicoDataTotal))

def testValidationImport(request):
    df = request.session['test']
    df = pd.read_json(df)
    print(df)
    return HttpResponse(str(df))