# -*- coding: utf-8 -*-
"""Image_PR_Funciones.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nEvaw9I0JudqVNhe3rFPNNl_enzFTdsm
"""

#Función que importa todas las librerías necesarias para correr las demás funcinoes. 
def imports_all():
  import os 
  import numpy as np 
  import pandas as pd 
  import skimage
  import imageio
  import scipy
  import matplotlib.pyplot as plt
  from PIL import Image
  import statistics
  from scipy.stats import kurtosis

#Función para tener una lista de strings del PATH de las imagenes 
def PATH(IMG_path):
  img_name=[]
  for file_name in IMG_path: 
     img_name.append(file_name)
     img_name.sort()
  return img_name

#Función que te da un vector de 0 a 256 con la frecuencia de cada pixel 
def vectRGB (path,Img):

  import imageio
  import numpy as np 

  Img = imageio.imread(path+'/'+Img)
  
  r,g,b = Img[:,:,0], Img[:,:,1], Img[:,:,2] #separamos las dimensiones 

  x = Img.shape[0]
  y = Img.shape[1]
  Vr=[]
  Vb=[]
  Vg=[]

#Aquí hacemos vectores con los tres canales, un vector R,G y B
  for i in range(x-1):
    for j in range(y-1):
      Vr.append(r[i,j]) 

  for i in range(x-1):
    for j in range(y-1):
      Vg.append(g[i,j])  

  for i in range(x-1):
    for j in range(y-1):
      Vb.append(b[i,j]) 
  
  vRGB = np.hstack((Vr,Vg,Vb))
  VIMG = np.concatenate((Vr, Vg, Vb))

  VectorR = np.zeros(256)
  VectorG = np.zeros(256)
  VectorB = np.zeros(256)

  frecuenciaR = {}
  frecuenciaG = {}
  frecuenciaB = {}

#Aquí estamos haciendo un histograma con formato json

  for n in Vr:
    if n in frecuenciaR:
      frecuenciaR[n] += 1
    else:
      frecuenciaR[n] = 1

  for n in Vg:
    if n in frecuenciaG:
      frecuenciaG[n] += 1
    else:
      frecuenciaG[n] = 1
  
  for n in Vb:
    if n in frecuenciaB:
      frecuenciaB[n] += 1
    else:
      frecuenciaB[n] = 1

#Aquí estamos convirtiendo el arreglo json en un arreglo normal,
#cada posición corresponde a una intensidad y 
#tiene distintos valores de las veces que se repite la intencidad

  for valorR in sorted(frecuenciaR):
    VectorR[valorR] = frecuenciaR[valorR]

  for valorG in sorted(frecuenciaG):
    VectorG[valorG] = frecuenciaG[valorG]

  for valorB in sorted(frecuenciaB):
    VectorB[valorB] = frecuenciaB[valorB]

  totalvect = np.concatenate((VectorR, VectorG, VectorB))

  Rr = VectorR.tolist() 
  Gg = VectorG.tolist()
  Bb = VectorB.tolist()

  totallist = Rr+Gg+Bb

#Estamos regresando el histograma aquí 
  
  return totallist

#Lo que hace esta función es poner en un arreglo todos los valores de los pixeles 1xn 
#pero son listas de listas, es decir, cada posición es una [img1= 1xn][img2=1xn_1][img_3=1xn_2][img_4=1xn_3][img_4=1xn_4]
def vectRGB_S (path,Img):

  import imageio
  import numpy as np 
  
  Img = imageio.imread(path+'/'+Img)
  
  r,g,b = Img[:,:,0], Img[:,:,1], Img[:,:,2]

  x = Img.shape[0]
  y = Img.shape[1]
  Vr=[]
  Vb=[]
  Vg=[]

  for i in range(x-1):
    for j in range(y-1):
      Vr.append(r[i,j])

  for i in range(x-1):
    for j in range(y-1):
      Vg.append(g[i,j])  

  for i in range(x-1):
    for j in range(y-1):
      Vb.append(b[i,j]) 
  
  return Vr, Vg, Vb

#Variables path y lista_path 
#la variable path es un string de la ubicación completa de un folder, es decir /root/data/imagenes/subtipo1 
#esa ruta es un ejemplo para poder explicar lo que significa path y lista path 
#esa ruta puede contener por ejemplo 100 imagenes (que se pueden llamar cómo sea) en este caso serán img_n (n de 0 a 99) 
#entonces path= '/root/data/imagenes/subtipo1/'
#mientras lista_path = [] es una lista, que contiene 100 posiciones, cada posición con el nombre de una imagen, es decir:
#lista_path= [img_1][img_2][img_3][img_4][img_5][img_6].....[img_n]

#En este se utiliza también la función PATH y la función vectRGB
#lo que hace esto es hacer un for loop para todas las imagenes dentro de un archivo 
#según yo puede leer cualquier imagen de un folder por qué tan distintas esten los nombres...
#pero por si acaso es mejor tenerlo bien estrúcturado y organizados los nombres

def Histograma(path,lista_path):
  import pandas as pd
  
  Nombre=[]
  Value = []

  for i in range(len(PATH(lista_path))): #aquí para i en la longitud de x se utilizará... 
    Nombre.append(PATH(lista_path)[i]) #la función PATH para sacar el nombre de la imagen 
  for i in range(len(PATH(lista_path))):#aquí para i en la longirud de x se utilizará
    Value.append(vectRGB(path,PATH(lista_path)[i])) #la función vectRGB que necesita de un path, y de la función path 

  df = pd.DataFrame() #realiza un DF 

  for i in range(len(Value)):
    df[i] = Value[i]

  df_ = pd.DataFrame()
  df_= df.transpose() # lo transpone para cambiarlo de posición
  df_.insert(0, "Nombre", Nombre, allow_duplicates=False)  #por ultimo incluye una columna llamada nombre, con la información de la lista Nombre 
  #en la posición 0 
  return df_  #por ultimo se hace un return del df para que se pueda exportar o visualizar.

#Aquí lo que se hace es utilzar un path y la lista_path para poder realizar...
#un vector único, en vez de que sean listas de listas (una lista de n posiciones y dentro de cada posición todos los valores...
#de cada una de las imagenes) en este caso es UN SOLO ARREGLO DE TODAS LAS IMAGENES.    

def totalvec(path,lista_path):
  
  import numpy as np
  
  VR_1 = []
  VG_1 = []
  VB_1 = []

  for i in range(len(PATH(lista_path))):
    VR_, VG_, VB_ = vectRGB_S (path,PATH(lista_path)[i])
  
    VR_1.append(VR_)
    VG_1.append(VG_)
    VB_1.append(VB_)

  VR_1_T = []
  VG_1_T = []
  VB_1_T = []

  for i in range(len(VR_1)):
    for j in range(len(VR_1[i])):
      VR_1_T.append(VR_1[i][j])

  for i in range(len(VG_1)):
    for j in range(len(VG_1[i])):
      VG_1_T.append(VG_1[i][j])

  for i in range(len(VB_1)):
    for j in range(len(VB_1[i])):
      VB_1_T.append(VB_1[i][j])


  VR_1_T = np.asarray(VR_1_T)
  VG_1_T = np.asarray(VG_1_T)
  VB_1_T = np.asarray(VB_1_T)

  return (VR_1_T, VG_1_T, VB_1_T)

#Este hace practicamente lo mismo que la función vectRGB_S, pero es como un segundo paso 
#para asegurarse que todo funciona bien, este ya está comprobado que funciona bien 
#es un paso extra, pero funciona. 
#solamente está guardando en variables los resultados de la función de vectRGB_S
#y ya 

def semivec(path,lista_path):
  
  import numpy as np
  
  VR_1 = []
  VG_1 = []
  VB_1 = []

  for i in range(len(PATH(lista_path))):
    VR_, VG_, VB_ = vectRGB_S (path,PATH(lista_path)[i])
  
    VR_1.append(VR_)
    VG_1.append(VG_)
    VB_1.append(VB_)
  
  return (VR_1,VG_1,VB_1)
