import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.impute import SimpleImputer
import seaborn as sns
from Funcion1D import *
from Funcion2D import *
import os

#Lectura del archivo de la BD
df_bd_original = pd.read_csv('BD/OnlineRetailcsv.csv', sep=',', encoding = 'unicode_escape')

#Obtenemos el análisis 1D de la BD sin preprocesar
Funcion_1D_a_BD_Sin_Preprocesar(df_bd_original)
os.system("PAUSE")

####################################################################
#Ahora comenzamos a preprocesar la BD
print("\n*******COMIENZA EL PREPROCESAMIENTO*******")
#detectamos la cantidad de tuplas que tengan la columna Quantity en negativo
df_quantity_negative = df_bd_original.loc[df_bd_original['Quantity'] < 0]
#detectamos la cantidad de tuplas que tengan la columna CustomerID NULL
df_null = df_bd_original.loc[df_bd_original['CustomerID'].isna()]
#df_deletenull elimina las tuplas con CustomerID = NULL y el resultado se almacena aca mismo
df_deletenull = df_bd_original.dropna(subset=['CustomerID'])
#detecta las tuplas con Quantity negativo en la bd sin nulls
df_quantity_negative_2 = df_deletenull.loc[df_deletenull['Quantity'] < 0]
#se elimina las tuplas con Quantity negativo restantes y se almacena la BD preprocesada en df_bd_nueva
#Comprobamos si existen tuplas duplicadas
df_bd_nueva = df_deletenull.drop(df_deletenull[df_deletenull['Quantity']<0].index)
#Eliminamos las tuplas duplicadas de la BD nueva, almacenandose en df_bd_nueva_final
df_filas_duplicadas = df_bd_nueva[df_bd_nueva.duplicated()]
#Ahora obtenemos la BD nueva sin filas duplicadas
df_bd_nueva_final = df_bd_nueva.drop_duplicates()
#print(df_bd_nueva.count())

print("\nFormato de muestra de registros (cant.filas , columnastotales)\n")
print("-------------------- PREPROCESAMIENTO --------------------")
print("Cantidad de tuplas totales en la BD original:", df_bd_original.shape)
print("Cantidad de tuplas con Quantity negativo:", df_quantity_negative.shape)
print("Cantidad de tuplas con CustomerId = NULL:", df_null.shape)
print("BD nueva sin las tuplas con CustomerID = null:", df_deletenull.shape)
print("Cantidad de tuplas restantes con Quantity < 0 en la BD nueva:", df_quantity_negative_2.shape)
print("Cantidad de tuplas totales de la BD nueva preprocesada:", df_bd_nueva.shape)
print("Número de filas duplicadas: ", df_filas_duplicadas.shape)
print("Total de filas de BD nueva sin filas duplicadas: ",df_bd_nueva_final.shape)
print("----------------------------------------------------------")
#Ya tenemos la BD preprocesada almacenada en df_bd_nueva_final
os.system("PAUSE")
####################################################################

#Obtenemos el análisis 1D de la BD ya preprocesada
Funcion_1D_a_BD_Preprocesada(df_bd_nueva_final)
os.system("PAUSE")

Funcion_2D_a_BD_Preprocesada(df_bd_nueva_final)
os.system("PAUSE")

#print("\n-- Ahora comenzar a procesar los datos para encontrar resultados --")



#IGNORAR DE AQUI A ABAJO
"""
#Creamos la matriz Customer-Item
#utilizamos tres columnas para crear la matriz. CustomerID, StoockCode y Quantity
customer_item_matrix = df_deletenull.pivot_table(index='CustomerID',columns='StockCode',values='Quantity',aggfunc='sum')

customer_item_matrix.loc[12481:].head()
customer_item_matrix.shape
print("\n\n")
df_deletenull['CustomerID'].nunique()
df_deletenull['StockCode'].nunique()
customer_item_matrix.loc[12348.0].sum()

#Utiizamos la función Lambda para transformar los valores distintos de cero a 0
customer_item_matrix = customer_item_matrix.applymap(lambda x: 1 if x>0 else 0)
customer_item_matrix.loc[12481:].head()

#Filtramos utilizando Sklearn
from sklearn.metrics.pairwise import cosine_similarity

#Filtramos según ID
user_to_user_sim_matrix = pd.DataFrame(cosine_similarity(customer_item_matrix))
user_to_user_sim_matrix.head()

#Seteamos la columna de la matriz para mostrar nombres y el ID del usuario
user_to_user_sim_matrix.columns = customer_item_matrix.index
user_to_user_sim_matrix['CustomerID'] = customer_item_matrix.index
user_to_user_sim_matrix = user_to_user_sim_matrix.set_index('CustomerID')
user_to_user_sim_matrix.head()

#Ahora, realizamos recomendaciones de productos
user_to_user_sim_matrix.loc[12350.0].sort_values(ascending = False)

#Mostramos los productos comprados por el primer Customer
items_bought_by_A = set(customer_item_matrix.loc[12350.0].iloc[customer_item_matrix.loc[12350.0]].index)
print("Items comprados por el primer cliente:")
print(items_bought_by_A)

#Mostramos los productos comprados por el siguiente cliente
print("Items comprados por el cliente siguiente:")
items_bought_by_B = set(customer_item_matrix.loc[17935.0].iloc[customer_item_matrix.loc[17935.0]].index)
print(items_bought_by_B)


items_to_recommend_User_B = items_bought_by_A - items_bought_by_B

print("Te recomiendo que compres: \n")
print(items_to_recommend_User_B)

df_deletenull.loc[
    df_bd_original['StockCode'].isin(items_to_recommend_User_B),
    ['StockCode','Description']
].drop_duplicates().set_index('StockCode')

#Usamos un CustomerID random para encontrar las recomendaciones de productos en base al primer Customer
###HASTA ACA, ES LA RECOMENDACIÓN SEGÚN LO COMPRADO POR EL PRIMER CUSTOMER

"""

"""
#Otro tipo basado en los productos
###AHORA ES LA RECOMENDACIÓN BASADO EN LOS PRODUCTOS COMPRADOS EN GENERAL
item_item_sim_matrix = pd.DataFrame(cosine_similarity(customer_item_matrix.T))

item_item_sim_matrix.columns = customer_item_matrix.T.index
item_item_sim_matrix['StockCode'] = customer_item_matrix.T.index
item_item_sim_matrix = item_item_sim_matrix.set_index('StockCode')

item_item_sim_matrix.head()

#Ahora hacemos las recomendaciones

top_10_similar_items = list(
    item_item_sim_matrix\
        .loc['23166']\
        .sort_values(ascending=False)\
        .iloc[:10]\
    .index
)

print(top_10_similar_items)

#Obtenemos el top10 de items similares
df_bd_original.loc[
    df_bd_original['StockCode'].isin(top_10_similar_items), 
    ['StockCode', 'Description']
].drop_duplicates().set_index('StockCode').loc[top_10_similar_items]
"""
