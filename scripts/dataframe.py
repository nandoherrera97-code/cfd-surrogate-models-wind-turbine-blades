#%%
import os
import pandas as pd
import numpy as np

base = os.getcwd()
results = os.path.join(base, "results")
carpetas = os.listdir(results)

# Inicializar DataFrame vacío
df1 = pd.DataFrame(columns=['Simulation', 'Points', 'U', 'P'])
for carpeta in carpetas:
    resultados_csv = os.path.join(results, carpeta, "postProcessing", "resultados.csv")
    
    if not os.path.exists(resultados_csv):
        print(f"Archivo no encontrado: {resultados_csv}")
        continue

    # Leer el archivo CSV
    df = pd.read_csv(resultados_csv)

    # Extraer y organizar los datos
    x = df["Points:0"].values
    y = df["Points:1"].values
    u_x = df["U:0"].values
    u_y = df["U:1"].values
    p = df["p"].values

    points = np.column_stack((x, y))
    u = np.column_stack((u_x, u_y))

    # Crear un DataFrame temporal para la nueva fila
    new_row = pd.DataFrame({'Simulation': [carpeta], 'Points': [points], 'U': [u], 'P': [p]})

    # Concatenar el DataFrame temporal con df1
    df1 = pd.concat([df1, new_row], ignore_index=True)

#%%
#---------- CARGAR SDF------------------

# Ruta al archivo pickle
file_path = 'sdf_df.pkl'

#  Cargar el DataFrame desde el archivo pickle
sdf_df = pd.read_pickle(file_path)
print(df1.head())                
                        
#%%
### --------------- DICRETIZACIÓN DEL ESPACIO ------------------------------

# Definir espacio bidimensional
x_min, x_max = -1.5, 1.5
y_min, y_max = -1.5, 1.5
resolution_x, resolution_y = 256, 256

# Calcular el paso de discretización en ambos ejes
step_x = (x_max - x_min) / (resolution_x - 1)
step_y = (y_max - y_min) / (resolution_y - 1)

# Iterar sobre cada celda de la matriz y determinar si está dentro del perfil
space =np.zeros((resolution_y, resolution_x,2))

for j in range(resolution_y):
    y = y_min + j * step_y
    for i in range(resolution_x):
        x = x_min + i * step_x
        space[j, i] = [x, y]

# Convertir space a una lista de puntos para usar en la interpolación
space_points = space.reshape(-1, 2)

# -------------------------------------------------------------------------------------- 
# CREAR CNN DATAFRAME 
# ---------------------------------------------------------------------------------------

from scipy.interpolate import griddata

# Crear las columnas para almacenar los valores discretizados
CNN_df = pd.DataFrame(columns=['SDF','Ux_discretized','Uy_discretized','P_discretized'])

# Iterar sobre cada simulación
for idx, row in df1.iterrows():
    # Obtener puntos, velocidades y presiones
    points = np.array(row["Points"])
    U = np.array(row["U"])
    P = np.array(row["P"])
    sim=row["Simulation"]
    
    # Interpolación de las componentes de la velocidad y la presión en la malla
    Ux_discretized = griddata(points, U[:, 0], space_points, method='linear')
    Uy_discretized = griddata(points, U[:, 1], space_points, method='linear')
    P_discretized = griddata(points, P, space_points, method='linear')

    #Redimensionar componentes de velocidad y presión
    Ux_discretized=Ux_discretized.reshape(256,256)
    Uy_discretized=Uy_discretized.reshape(256,256)
    P_discretized=P_discretized.reshape(256,256)

    #Voltear matriz para su correcto visualizado 
    Ux_discretized=np.flipud(Ux_discretized)
    Uy_discretized=np.flipud(Uy_discretized)
    P_discretized=np.flipud(P_discretized)

    #Encontrar indice
    indice=sdf_df.index[sdf_df["Simulation"] == sim].tolist()
    # Obtener la matriz SDF correspondiente a la simulación actual
    sdf_matrix = np.array(sdf_df.loc[indice[0]]["SDF"])
    
    # Aplicar la condición de SDF: en las celdas ocupadas por geometría (SDF < 0), no hay valores de fluido
    Ux_discretized[sdf_matrix < 0] = 0
    Uy_discretized[sdf_matrix < 0] = 0
    P_discretized[sdf_matrix < 0] = 0
    
    # Guardar los resultados en el DataFrame
    CNN_df.at[idx, "SDF"] = sdf_matrix
    CNN_df.at[idx, "Ux_discretized"] = Ux_discretized
    CNN_df.at[idx, "Uy_discretized"] = Uy_discretized
    CNN_df.at[idx, "P_discretized"] = P_discretized

print(CNN_df.tail())
#%%
CNN_df.to_pickle('CNN_df.pkl')
# %%
# -------------------- COMPROBACIÓN ----------------------
import matplotlib.pyplot as plt

SDF=CNN_df["SDF"][35]
U_y_plt=CNN_df["Uy_discretized"][35]
U_x_plt=CNN_df["Ux_discretized"][35]
# Crear el colormap
plt.figure(figsize=(6, 6))
plt.imshow(SDF, cmap='viridis')  # 'viridis' es un colormap común, pero puedes elegir otro
plt.colorbar(label='Velocidad (m/s)')   # Agrega una barra de color para indicar la escala
plt.title('Campo de velocidades U_y')
plt.xlabel('Eje X')
plt.ylabel('Eje Y')

# Crear el colormap
plt.figure(figsize=(6, 6))
plt.imshow(U_x_plt, cmap='viridis')  # 'viridis' es un colormap común, pero puedes elegir otro
plt.colorbar(label='Velocidad (m/s)')   # Agrega una barra de color para indicar la escala
plt.title('Campo de velocidades U_y')
plt.xlabel('Eje X')
plt.ylabel('Eje Y')

# Crear el colormap
plt.figure(figsize=(6, 6))
plt.imshow(U_y_plt, cmap='viridis')  # 'viridis' es un colormap común, pero puedes elegir otro
plt.colorbar(label='Velocidad (m/s)')   # Agrega una barra de color para indicar la escala
plt.title('Campo de velocidades U_y')
plt.xlabel('Eje X')
plt.ylabel('Eje Y')

# Mostrar el gráfico
plt.show()
# %%
