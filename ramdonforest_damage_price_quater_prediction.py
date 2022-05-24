# -*- coding: utf-8 -*-
"""RamdonForest_Damage_Price_Quater_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1v0aQ_6w8AXZ9GvsjW-7unEaGL4rFjsUj

#Descarga de Datasets
"""


"""#Inicialiación de Datos y Desarrollo del modelo"""

#Bibliotecas necesarias
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

#Obtenemos los datos de los archivos descargados y los mostramos
df_viviendas=pd.read_excel('Datasets/viviendas.xlsx')
df_poblacion=pd.read_csv('Datasets/poblacion.csv')
df_datos_sismicos=pd.read_excel('Datasets/IGP_datos_sismicos.xlsx')

df_datos_sismicos

df_poblacion

df_viviendas

#A continuación, guardamos en dos listas los distritos y los gatos por daño, basandonos en la cantidad de sismos del dataset de Sismos
list_distr=[]
list_damage_expe=[]
for i in (df_datos_sismicos.index):
  #Creamos una variable auxiliar que al principio de cada iteración  tendrá un valor de 100 elevado a la 9
  #Esto es necesario para actualizar esta variable con los valores más pequeños a ese
  aux=math.pow(100,9)
  for j in df_viviendas.index:
    #Obtenemos la distancia euclidiana de los sismos con los distritos
    d_eu = math.sqrt(math.pow(df_viviendas['Longitud'][j]-df_datos_sismicos['longitud'][i],2) + math.pow(df_viviendas['Latitud'][j]-df_datos_sismicos['latitud'][i],2))
    #Si la distancia euclidiana es menor al auxiliar entra->
    if aux > d_eu:
      #Ahora el auxiliar va a tener la distancia euclidiana que fue menor a él
      aux=d_eu
      #Aca guardamos el index del distrito para utilizarlo en nuestro modelo ML, en ves de utilizar su nombre
      distr = j
      #Con ayuda del dataset Viviendas obtenemos los supuestos gastos por daños de cada distrito
      #Multiplicamos el metro cuadrado de cada distrito por la valorización por metro cuadrado
      damage_expe = df_viviendas['Precio metro cuadrado (soles)'][j]*(df_viviendas['Area km2'][j]*math.pow(10,6))
  #Los resultados los guardamos cada uno en una lista, y esta lista se irá lllenando por cada sismo en el dataset de Sismos
  list_distr.append(distr)
  list_damage_expe.append(damage_expe)

#Hacemos una copia del DataFrame de Sismos para utilizarlo como datos de entrenamiento y testeo en nuestro modelo ML
df=df_datos_sismicos.copy()

#Le insertamos las columnas distrito y gastos por daño, con sus respectivos datos de cada lista perteneciente
df['distrito']=list_distr
df['gasto por daño']=list_damage_expe

#Eiminamos las columnas q no nos sirven
df.drop(['fecha UTC', 'hora UTC'], axis=1, inplace=True)

#Vista del nuevo dataframe que luego será separado en datos de entrenamiento y de prueba
df

df.to_csv('sismos.csv')

#Guardamos en una variable X_df las columnas con los datos que nos serviran de entrada para el modelo ML
X_df=df.iloc[:,[0,1,2,3,4]]

#Guardamos en una variable X_df las columnas con los datos que nos serviran de tarjet para el modelo ML
y_df=df.iloc[:,[-1]]

#Separamos los datos de entrenamiento con los datos de prueba
X_train, X_test, y_train, y_test=train_test_split(X_df,y_df,random_state=100)

#Creamos el modelo ML Random Forest
ModelRF=RandomForestRegressor(n_estimators=50,random_state=9599,min_samples_leaf=8)

#Entrenamos el modelo
ModelRF.fit(X_train,y_train)

#Ponemos a prueba nuestro modelo con la funcion ModelRF.predict donde nuestro parametro 
#serán nuestros datos de entrada y el resultado va a ser la predicción
y_pred=ModelRF.predict(X_test)

#Observamos que la prediccón en la fila 528 es la siguiente
y_pred[528]

#Corroboramos que sea esa la predicci+on correcta, viendo  en y_test 
#que tiene el resultado que debería dar nuestra predicción
y_test.iloc[528,]
#Apartir del resultado vemos que la predicción ha sido acertada

#Creamos una función para probar una predicción personalizada

def Prediction(profundidad, magnitud, distrito, latitud, longitud):
  #Creamos 5 listas q almacenarán un solo valor
  l_p_p=[profundidad]
  l_p_m=[magnitud]
  l_p_d=[distrito]
  l_p_la=[latitud]
  l_p_lo=[longitud]
  
  #Para ello es necesario crear un dataframe
  df_aux=pd.DataFrame()
  df_aux['latitud']= l_p_la
  df_aux['longitud']= l_p_lo
  df_aux['profundidad (km)']=l_p_p
  df_aux['magnitud (M)']=l_p_m
  df_aux['distrito']=l_p_d

  return df_aux

#Función de predicción  Colocar la Latitud,Longitud,Profundidad,Magnitud,Distrito para predecir los gastos por sismo 
df_prediction=Prediction(-16.1450,-72.1440,60,9,29)
p_y_pred=ModelRF.predict(df_prediction)

print(p_y_pred[0])

#from mlxtend.plotting import plot_confusion_matrix
#from sklearn.metrics import confusion_matrix
#matriz=confusion_matrix(y_test,y_pred)
#
#plot_confusion_matrix(conf_mat=matriz, figsize=(6,6), show_normed=False)
#plt.tight_layout()