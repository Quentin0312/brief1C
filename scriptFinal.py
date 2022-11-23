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
# 1- InvoiceNo
# 2- StockCode
# 3- Description
# 4- Quantity
# 5- InvoiceDate
# 6- UnitPrice
# 7- CustomerID
# 8- Country

# À envoyer BDD => Facures: 1-5-8 ; Produits => 2 ; Details => 4-1-2
# for elt in df.loc:

    

#---------------------------------