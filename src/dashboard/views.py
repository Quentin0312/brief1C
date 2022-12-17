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


# Fonctions ---------------------------------------------------------------------------------------------------------

# Concerne graphTCD seulement
# M=> Récupération de la liste des produits pour le graph TCD à partie rows SQL
# I=> rows (liste de tuples)
# O=> liste des produits (liste de str)
def recupererListeProduitsTCD(rows):
    listeProduits = []
    for elt in rows:
        if elt[1] not in listeProduits:
            listeProduits.append(elt[1])
    return listeProduits

# Concerne le graphTCD seulement
# M=> Récupération de la liste des pays pour le graph TCD
# I=> rows (liste de tuples)
# O=> liste des pays (liste de str)
def recupererListePaysTCD(rows):
    listePays = []
    for elt in rows:
        if elt[0] not in listePays:
            listePays.append(elt[0])
    return listePays

# M=> Contribue à la production du datasets pour chart JS
#     Produit 2 listes (valeurs et labels) à partir liste de tuples(rows)
# I=> rows (liste de tuples)
# O=> listes des valeurs "data" (list de int), liste des labels (list de str)
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
    
    return valeurs,labels


# Concerne seuelement le graphTCD
# M=> Contribue à la production du datasets graph bar stacked "fraudé" pour le graph TCD
# I=> listePays, listeProduits, rows=> correspond à la requet SQL datasets du graph TCD: ventes par produits par pays => columns: region, codeproduit, vente
# O=> Dictionnaire de data contenant liste de datas(value) par pays(key) (Dictionnaire contenant des listes)
def produitGraphDataset(listePays, listeProduits, rows):
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

# M=> Fait une requete SQL (ATTENTION : Pas seulement SELECT car fetchall() )
# I=> Requete SQL (str)
# O=> Rows, ce que renvoie la requete SQL (liste de tuples)
def selectSQL(scriptSQL):
    cursor = connections['default'].cursor()
    cursor.execute(scriptSQL)
    rows = cursor.fetchall() # Contient ce que le SELECT renvoie
    return rows

# À faire : Gestion des mauvaises entrées dans formulaire => ex si pas int valeurs par default
# M=> Permet de récuperer le top ? dans la BDD ou définit valeur par default
# I=> Nom du graph concerné (str) "pays" OU "produits" OU "graph3ProduitsPays" OU "graph3PaysProduits"
# O=> Nombre correspondant au top (int)
def recupererTopX(nomGraph):
    try:
        # Requete SQL
        topSQL = "SELECT LAST_VALUE(param1) OVER(ORDER BY auto_increment_id ASC RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) test FROM paramgraph WHERE nomgraph ='"+ nomGraph +"' LIMIT 1"
        top = selectSQL(topSQL)
        # Si pas de valeurs TOP dans la BDD
        if top == []:
            top = 10
        # Récupération du int dans la liste de tuples
        else:
            for elt in top:
                for subelt in elt:
                    top = subelt
    # Autre situation d'erreur ?
    except:
        top = 10
    return top

# M=> Executer la bonne requete SQL selon le top x pour le graphProduits
# I=> Nombre representant le top voulue (int)
# O=> Ce que renvoie la requete SQL (liste de tuples)
def selectSQLproduit(top):
    # Si valeur vide entrée
    if top == None:
        top = 10

    requeteSQL = "SELECT codeproduit, COUNT(*) AS vente FROM contenir GROUP BY codeproduit ORDER BY vente DESC LIMIT "+str(top)
    cursor = connections['default'].cursor()
    cursor.execute(requeteSQL)
    rows = cursor.fetchall() # Contient ce que le SELECT renvoie
    return rows

# M=> Executer la bonne requete SQL selon le top x pour le graphPays
# I=> Nombre representant le top voulue (int)
# O=> Ce que renvoie la requete SQL (liste de tuples)
def selectSQLpays(top):
    # Si valeur vide entrée
    if top == None:
        top = 10

    requeteSQL = "SELECT factures.region, COUNT(*) AS vente FROM factures INNER JOIN contenir ON factures.nofacture = contenir.nofacture GROUP BY factures.region ORDER BY vente DESC LIMIT "+str(top)
    cursor = connections['default'].cursor()
    cursor.execute(requeteSQL)
    rows = cursor.fetchall() # Contient ce que le SELECT renvoie
    return rows

# M=> Nettoyer le dataframe
# I=> Dataframe (dataframe pandas)
# O=> Dataframe (dataframe pandas),
#     Pls données feedback (int)
def nettoyageDataframe(dataframe):
    avantNettoyage = len(dataframe)

    #Suppression "CustomerID"
    dataframe.drop('CustomerID', inplace=True, axis=1)

    # uppercase les codeproduits pour la bonne correspondance de la FK dans la BDD
    dataframe['StockCode'] = dataframe['StockCode'].str.upper()

    # Suppression doublons
    dataframe.drop_duplicates(subset=['InvoiceNo','StockCode'],inplace=True)
    # Données feedback
    apresSupprDoublons = len(dataframe)
    qteSupprDoublons = avantNettoyage - apresSupprDoublons
    
    # Pays à supprimer : Unspecified
    dataframe.drop(dataframe[dataframe['Country'] == 'Unspecified'].index, inplace = True)
    # Données feedback
    apresSupprPays = len(dataframe)
    qteSupprPays = apresSupprDoublons - apresSupprPays

    # Suppression des avoirs
    # len == 7
    dataframe.drop(dataframe[dataframe['InvoiceNo'].str.len() == 7].index, inplace = True)
    # Quantity < 0
    dataframe.drop(dataframe[dataframe['Quantity'] <0].index, inplace = True)
    # UnitPrice == 0
    dataframe.drop(dataframe[dataframe['UnitPrice'] == 0].index, inplace = True)
    # Données feedback
    apresSupprAvoir = len(dataframe)
    qteSupprAvoir = apresSupprPays - apresSupprAvoir
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
    lignesSuppr = avantNettoyage - apresNettoyage
    pourcentageDataPerdues = lignesSuppr / avantNettoyage *100
    print("Pourcentage data perdues durant nettoyage=======> "+str(pourcentageDataPerdues))
    return dataframe, pourcentageDataPerdues, avantNettoyage, apresSupprDoublons, qteSupprDoublons, apresSupprPays, qteSupprPays, apresSupprAvoir, qteSupprAvoir, apresNettoyage, lignesSuppr

# M=> Remplir la table produits
# I=> Dataframe (dataframe Pandas), engine SQLalchemy
# O=> Pas de variables retournées
#     ACTION: Import dans table produits
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

# M=> Remplir la table factures
# I=> Dataframe (dataframe Pandas), engine SQLalchemy
# O=> Pas de variables retournées
#     ACTION: Import dans table factures
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

# M=> Remplir la table contenir
# I=> Dataframe (dataframe Pandas), engine SQLalchemy
# O=> Pas de variables retournées
#     ACTION: Import dans table contenir
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

# M=> Importer dans la BDD
# I=> Dataframe (dataframe Pandas)
# O=> Pas de variables retournées
#     ACTION: Import dans la BDD
def importer(df):
    engine = create_engine('postgresql://postgres:azerty@localhost:5432/brief1C')

    # Table produits
    importerProduits(df, engine)

    # Table facture
    importerFactures(df, engine)

    # Table contenir
    importerContenir(df, engine)

# Concerne graph3 seulement
# M=> Récupérer le dernier param2 correspondant au pays voulu dans la BDD
# I=> Nom du graph (str) "graph3ProduitsPays" OU "graph3PaysProduits"
# O=> param2 de la table paramgraph (str)
def recupererParam2(nomGraph):
    try:
        # Requete SQL
        SQL = "SELECT LAST_VALUE(param2) OVER(ORDER BY auto_increment_id ASC RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) test FROM paramgraph WHERE nomgraph ='"+nomGraph+"' LIMIT 1"
        query = selectSQL(SQL)

        # Si table vide => valeurs par default
        if query == [] and nomGraph == "graph3ProduitsPays":
            paramCible = 'United Kingdom' # Pour un code "pro" cette valeurs doit être dynamique, car compatible peut importe les pays existant dans le dataframe
        elif query == [] and nomGraph == "graph3PaysProduits":
            paramCible = '85123A' # Pour un code "pro" cette valeurs doit être dynamique, car compatible peut importe les produits existant dans le dataframe
        
        # Sinon valeurs présentes, récup du str dans la liste 
        else:
            for elt in query:
                for subelt in elt:
                    paramCible = subelt
    # Autre situation d'erreur ? => valeurs par defaults
    except:
        if nomGraph == 'graph3ProduitsPays':
            paramCible = 'United Kingdom' # Pour un code "pro" cette valeurs doit être dynamique, car compatible peut importe les pays existant dans le dataframe
        else:
            paramCible = '85123A' # Pour un code "pro" cette valeurs doit être dynamique, car compatible peut importe les produits existant dans le dataframe
    return paramCible

# Concerne le graph3 et modal page graphPays
# M=> Execute la requete SQL pour recup datasets top produits pour paysCible définit
# I=> paysCible (str), topCible (int)
# O=> Ce que renvoie la requeteSQL, datasets à retransformer (liste de tuples)
def requeteSQLgraph3_1(paysCible,topCible):
    requeteSQL = "SELECT contenir.codeproduit, COUNT(*) AS vente FROM contenir INNER JOIN factures ON factures.nofacture = contenir.nofacture WHERE region = '" + paysCible + "' GROUP BY factures.region, contenir.codeproduit ORDER BY vente DESC LIMIT " + str(topCible)
    cursor = connections['default'].cursor()
    cursor.execute(requeteSQL)
    rows = cursor.fetchall() # Contient ce que le SELECT renvoie
    return rows

# Concerne le graph3 et modal page graphProduits
# M=> Execute la requete SQL pour recup datasets top pays pour produitsCible définit dans I
# I=> produitCible (str), topCible (int)
# O=> Ce que renvoie la requeteSQL, datasets à retransformer (liste de tuples)
def requeteSQLgraph3_2(produitCible,topCible):
    requeteSQL = "SELECT factures.region, COUNT(*) AS vente FROM contenir INNER JOIN factures ON factures.nofacture = contenir.nofacture WHERE codeproduit = '" + produitCible + "' GROUP BY factures.region, contenir.codeproduit ORDER BY vente DESC LIMIT " + str(topCible)
    cursor = connections['default'].cursor()
    cursor.execute(requeteSQL)
    rows = cursor.fetchall() # Contient ce que le SELECT renvoie
    return rows

# Concerne le graph3
# M=> Fonction parente produisant le datasets pour les graph3 et recuperant les top et paramCible dans la BDD
# I=> nomGraph (str) "graph3ProduitsPays" OU "graph3PaysProduits"
# O=> valeurs (list), labels (liste), topCible (int), paramCible (str)
#     Datasets et dernier param top et cible de la BDD
def produireLabelsEtDataGraph3(nomGraph):

    # Recupérer top
    topCible = recupererTopX(nomGraph)

    # Récupérer paysCible
    paramCible = recupererParam2(nomGraph)

    # Requete SQL si graph 1
    if nomGraph == "graph3ProduitsPays":
        rows = requeteSQLgraph3_1(paramCible, topCible)
    # Requete SQL si graph 2
    elif nomGraph == "graph3PaysProduits":
        rows = requeteSQLgraph3_2(paramCible, topCible)


    # Rows to labels et data lists
    valeurs, labels = rowToVariable(rows)
    # print(valeurs)
    return valeurs, labels, topCible, paramCible

# Concerne le graph3
# M=> Récupere la liste des pays présent dans la BDD
# I=> Rien (fonction utilisé 1 seule fois, pas dynamique)
# O=> liste des pays existants dans la table factures (list de str) 
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

# Concerne le graph3
# M=> Récupere la liste des produits présent dans la BDD
# I=> Rien (fonction utilisé 1 seule fois, pas dynamique)
# O=> liste des produits existants dans la table factures (list de str) 
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

# Views ----------------------------------------------------------------------------------------------------------------
def mainDashboard(request):
    # Si utilisateur connecté
    if request.user.is_authenticated == True:

        return render(request,"mainDashboard.html")
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
        df, pourcentageDataPerdues, avantNettoyage, apresSupprDoublons, qteSupprDoublons, apresSupprPays, qteSupprPays, apresSupprAvoir, qteSupprAvoir, apresNettoyage, lignesSuppr  = nettoyageDataframe(df)

        # Données feedback
        dicoFeedback = {}

        dicoFeedback['pourcentageDataPerdues'] = pourcentageDataPerdues
        dicoFeedback['avantNettoyage'] = avantNettoyage
        dicoFeedback['apresSupprDoublons'] = apresSupprDoublons
        dicoFeedback['qteSupprDoublons'] = qteSupprDoublons
        dicoFeedback['apresSupprPays'] = apresSupprPays
        dicoFeedback['qteSupprPays'] = qteSupprPays
        dicoFeedback['apresSupprAvoir'] = apresSupprAvoir
        dicoFeedback['qteSupprAvoir'] = qteSupprAvoir
        dicoFeedback['apresNettoyage'] = apresNettoyage
        dicoFeedback['lignesSuppr'] = lignesSuppr



        # df convertit en JSON pour être enregistré dans request.session
        df = df.to_json()

        # enregistrement du df dans request.session
        request.session['dfNettoye'] = df

        # Render de la page HTML affichant le feedback (dans le même URLs => avantages innaccessible sauf method=POST)
        return render(request, 'addFeedback.html', context={'feedback':dicoFeedback})
    
    # Etape 1
    else:
        # Context
        form = UploadFileForm()
        context = {
            'form':form
            }
    return render(request, 'add.html', context) #Affiche la page en ayant le formulaire en context

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
    valeurs1, labels1, topCible1, paramCible1 = produireLabelsEtDataGraph3("graph3ProduitsPays")
    
    # Données graph 2 Top pays par praoduits
    valeurs2, labels2, topCible2, paramCible2 = produireLabelsEtDataGraph3("graph3PaysProduits") 

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

# Importation dans la BDD
def addDF(request):
    # Vérification que user est login
    if request.user.is_authenticated ==False:
        return redirect('login')
    
    # Récup du dataframe en JSON dans request.session
    dfNettoye = request.session["dfNettoye"]

    # JSON to dataframe
    dfNettoye = pd.read_json(dfNettoye)

    # Format date provenant de JSON (ms since 1970) transformé pour l'import dans postgreSQL 
    dfNettoye["datefacturation"] = pd.to_datetime(dfNettoye["datefacturation"], unit='ms')

    # Import du dataframe dans la BDD
    importer(dfNettoye)

    #Suppression du request.session par sécurité et/ou optimisation ?
    request.session["dfNettoye"] = "Ma déja supprimé, en attente nouvelle valeur"
    
    return redirect(mainDashboard)

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