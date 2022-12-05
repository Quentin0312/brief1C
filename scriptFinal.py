import pandas as pd
import numpy as np
import re

df = pd.read_csv('./ressources/data2010-2011s1.csv', encoding = "ISO-8859-1")

# Vérification -------------------
#---------------------------------

# Nettoyage ----------------------

#Suppression "CustomerID"
df.drop('CustomerID', inplace=True, axis=1)
# --------------------------------

#Suppression doublons
df.drop_duplicates(subset=['InvoiceNo','StockCode'],inplace=True)
# --------------------------------

# Pays à supprimer
# Unspecified
df.drop(df[df['Country'] == 'Unspecified'].index, inplace = True)
# European Community
df.drop(df[df['Country'] == 'European Community'].index, inplace = True)
# Channel islands
df.drop(df[df['Country'] == 'Channel Islands'].index, inplace = True)
# --------------------------------

# Suppression des avoirs
# len == 7
df.drop(df[df['InvoiceNo'].str.len() == 7].index, inplace = True)
# Quantity < 0
df.drop(df[df['Quantity'] <0].index, inplace = True)
# UnitPrice == 0
df.drop(df[df['UnitPrice'] == 0].index, inplace = True)

# Description ??


# Envoi BDD-----------------------
# 0- InvoiceNo
# 1- StockCode
# 2- Description
# 3- Quantity
# 4- InvoiceDate
# 5- UnitPrice
# 6- CustomerID
# 7- Country

# À envoyer BDD => Factures: 0-4-7 ; Produits => 1 ; Details => 3-0-1
# for elt in df.loc:
# ex: elt[1] => stockcode
    

#---------------------------------

# Labo conversion numpy64int to int

# iteration = 0

# for elt in df.loc:
#     iteration +=1
#     # apresConversion = elt[3].item()
#     print(type(elt[3].item()))
#     if iteration > 5:
#         break

print(df.info())
# test = df.loc[(df["Description"].str.len() < 6)]
# print(test)