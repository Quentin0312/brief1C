import pandas as pd
import numpy as np
import re

df = pd.read_csv('./ressources/data2010-2011s1.csv', encoding = "ISO-8859-1")

# Vérification -------------------
#---------------------------------

# Nettoyage ----------------------

#Suppression "CustomerID"
# df.drop('CustomerID', inplace=True, axis=1)

#Suppression doublons
# print(df.info())
# df.drop_duplicates(subset=['InvoiceNo','StockCode'],inplace=True)
# print(df.info())

# test = df.duplicated(keep='first')
# print(test)


# --------------------------------

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

iteration = 0

for elt in df.loc:
    iteration +=1
    # apresConversion = elt[3].item()
    print(type(elt[3].item()))
    if iteration > 5:
        break