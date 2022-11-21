# Pandas W3schools
# https://www.w3schools.com/python/pandas/pandas_cleaning_empty_cells.asp

import pandas as pd

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

# contenueColonne = df["Quantity"]

# listeType = []
# debug = 0
# for elt in contenueColonne:
#     debug +=1
#     print
#     if type(elt) in listeType:
#         continue
#     else:
#         listeType.append(type(elt))
