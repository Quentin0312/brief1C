# Pandas W3schools
# https://www.w3schools.com/python/pandas/pandas_cleaning_empty_cells.asp

# Doc panda methode string sur panda series
# https://pandas.pydata.org/docs/user_guide/text.html#string-methods

import pandas as pd
import numpy as np
import re

df = pd.read_csv('./ressources/data2010-2011s1.csv', encoding = "ISO-8859-1")

# Print en entier
# print(df.to_string())

# print(df)

# Affiche les 10 er
# print(df.head(10))

#Affiche les derniers
# print(df.tail())

# Maximum rows
# print(pd.options.display.max_rows) 

# Info sur les champs du csv
# print(df.info()) 

# Affiche True les elt doublons
# print(str(df.duplicated()))

# Compte les doublons
# i = 0
# for elt in df.duplicated():
#     if elt == True:
#         i+= 1
#         # print(str(elt) +str(i))
# print(i)

# Affiche row selon conditions 
# print(df.loc[(df["Quantity"]) < 0 & (df["UnitPrice"] > 0)])

# Affiche seulement le contenu d'un champs
# print(df["Country"])

# Affiche la valeur "Country" du row [0]
# test = df["Country"]
# print(test[0])

# Affiche les elt unique dans le champs
def allUniqueElementsIn1Colonne(dataFrame, colonne): # colonne => "entreGuillemets"
    contenueColonne = dataFrame[colonne]
    liste = []

    init = 0
    for elt in contenueColonne:
        if init == 0:
            liste.append(elt)
            init = 1
        if elt in liste:
            continue
        else:
            liste.append(elt)

    return liste

# listePays = allUniqueElementsIn1Colonne("Country")

# print(listePays)

# Renvoie le nombre de row correspondant à la condition
# test = df.loc[(df["Quantity"]) < 0 & (df["UnitPrice"] > 0)]
# print(len(test))

# Remplacer les ? par la bonne valeur et garder les autre elt ecrit ex: wrong code

# ---------InvoiceNo --------------- Renvoie les diff len présent
def diffLenDans(dataFrame, colonne):

    contenueColonne = dataFrame[colonne]
    liste = []

    debug = 0
    for elt in contenueColonne:
        debug +=1
        print(debug)
        if len(elt) in liste:
            continue
        else:
            liste.append(len(elt))

    return liste

# diffLen = diffLenDans(df, "InvoiceNo")
# print(diffLen)

# ---------InvoiceNo --------------- Donne les indexs des valeur d'un len précis
def indexsValeursDontLen(dataFrame, colonne, lenCible):
    contenueColonne = dataFrame[colonne]
    listeIndexs = []
    debug = 0

    for elt in contenueColonne:
        debug+=1
        print(debug)
        if len(elt) == lenCible:
            listeIndexs.append(debug)

    return listeIndexs

# listeINdexsSept = indexsValeursDontLen(df, "InvoiceNo", 7)
# print(listeINdexsSept)

# ---------InvoiceNo --------------- Vérifier si tout les noFacture commencant par C sont des avoirs

# test = df.loc[(df["InvoiceNo"].str.len() > 6) & (df["Quantity"] > 0)]
# print(test.to_string())

# ---------Quantity --------------- Verifier si tte les valeurs sont des entiers

# Vérif les types de donnée
def diffTypes(dataFrame, colonne): # PAS PERTINENT=> 1 seul type de donné par champs 

    contenueColonne = dataFrame[colonne]

    listeType = []
    debug = 0
    for elt in contenueColonne:
        debug +=1
        print(debug)
        if type(elt) in listeType:
            continue
        else:
            listeType.append(type(elt))

    return listeType

# listeTypes = diffTypes(df, "Quantity")
# print(listeTypes)

# ---------Quantity --------------- Verifier si valeurs manquantes (len==0)

#Renvoie les diff len sachant initialemtn int =>, typecasting

def diffLenv2(dataFrame, colonne): # typecast en len

    contenueColonne = dataFrame[colonne]
    liste = []

    debug = 0
    for elt in contenueColonne:
        debug +=1
        print(debug)
        # Type cast si pas str
        if type(elt) != "str":
            if len(str(elt)) in liste:
                continue
            else:
                liste.append(len(str(elt)))
                liste.append("index=>"+str(debug))
        # Si str
        else:
            if len(elt) in liste:
                continue
            else:
                liste.append(len(elt))


    return liste

# diffLenPays = diffLenv2(df, "Country")
# print(diffLenPays)

# Renvoie le nombre de valeurs manquantes
# print(df["Quantity"].isna().sum())

# ---------InvoiceDate------------- Vérifier le format (via nb de charactère)
# https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html

# nbCharDate = diffLenv2(df, "InvoiceDate")
# print(nbCharDate)

# ---------InvoiceDate------------- Vérifier les valeurs manquantes

# print(df["InvoiceDate"].isna().sum())

valeurCible = "1/15/2011 19:11"
# test1 = re.fullmatch("[0-9]/[0-9]/[1-2][0-9][0-9][0-9] [0-9]:[0-5][0-9]", valeurCible)
# test2 = re.fullmatch("[0-9]/[0-9]/[1-2][0-9][0-9][0-9] [1-2][0-9]:[0-5][0-9]", valeurCible)
# test3 = re.fullmatch("1[0-9]/[0-9]/[1-2][0-9][0-9][0-9] [1-2][0-9]:[0-5][0-9]", valeurCible)
# test4 = re.fullmatch("1[0-9]/[0-9]/[1-2][0-9][0-9][0-9] [0-9]:[0-5][0-9]", valeurCible)
# test5 = re.fullmatch("[0-9]/[0-9]/[1-2][0-9][0-9][0-9] [1-2][0-9]:[0-5][0-9]", valeurCible)
# test6 = re.fullmatch("[0-9]/[0-9]/[1-2][0-9][0-9][0-9] [0-9]:[0-5][0-9]", valeurCible)
# test7 = re.fullmatch("1[0-9]/[0-9]/[1-2][0-9][0-9][0-9] [1-2][0-9]:[0-5][0-9]", valeurCible)
# test8 = re.fullmatch("1[0-9]/[0-9]/[1-2][0-9][0-9][0-9] [0-9]:[0-5][0-9]", valeurCible)

listeTest = ["[0-9]/[0-9]/[1-2][0-9][0-9][0-9] [0-9]:[0-5][0-9]", #1
    "[0-9]/[0-9]/[1-2][0-9][0-9][0-9] [1-2][0-9]:[0-5][0-9]", #2
    "1[0-9]/[0-9]/[1-2][0-9][0-9][0-9] [1-2][0-9]:[0-5][0-9]", #3
    "1[0-9]/[0-9]/[1-2][0-9][0-9][0-9] [0-9]:[0-5][0-9]", #4
    "[0-9]/[1-3][0-9]/[1-2][0-9][0-9][0-9] [1-2][0-9]:[0-5][0-9]", #5
    "[0-9]/[1-3][0-9]/[1-2][0-9][0-9][0-9] [0-9]:[0-5][0-9]", #6
    "1[0-9]/[0-9]/[1-2][0-9][0-9][0-9] [1-2][0-9]:[0-5][0-9]", #7
    "1[0-9]/[1-3][0-9]/[1-2][0-9][0-9][0-9] [0-9]:[0-5][0-9]"] #8

def verifFormatDate(valeurCible, listeTest):
    i=0
    for elt in listeTest:
        i+=1
        test = re.fullmatch(elt, valeurCible)
        if test:
            resultat = "test"+str(i)+"validé"
            return resultat

    resultat = "Pas de correspondance !"
    return resultat

resultat = verifFormatDate(valeurCible=valeurCible, listeTest=listeTest)
print(resultat)
