import streamlit as st
import pandas as pd
from PIL import Image
import requests

# Ruta al archivo CSV (recuerda reemplazar con la ruta real)
ruta_csv = "/home/abeldg24/Documentos/python/PYTHON CODIGOS/STREAMLIT_NICE/Catalogo_nice.csv"  

# Carga la base de datos desde el archivo CSV
df_productos = pd.read_csv(ruta_csv)

# Convierte el DataFrame a un diccionario (usando 'ID' como clave)
productos = df_productos.set_index('ID').to_dict('index')

st.title("Consulta de productos")

# Inicializa el total
total_acumulado = 0

# Input para el ID del producto
id_producto = st.text_input("Introduce el ID del producto:")

if id_producto:
    try:
        if id_producto in productos:
            producto = productos[id_producto]

            # Descripción
            st.write("**Descripción:**", producto["DESCRIPCION"])

            # Imagen (asumiendo que la columna 'imagen' contiene URLs)
            try:
                imagen = Image.open(requests.get(producto["imagen"], stream=True).raw)
                st.image(imagen, caption=producto["DESCRIPCION"])
            except:
                st.write("Error al cargar la imagen.")

            # Cantidad
            cantidad = st.number_input("Cantidad:", min_value=1, value=1)

            # Precio individual (convierte a float)
            precio_individual = float(str(producto["PRECIO CATALOGO"]).replace("$", "").replace(",", ""))
            st.write("**Precio individual:**", precio_individual)
            
            # Calcula el total del producto actual
            total_producto = cantidad * precio_individual

            # Actualiza el total acumulado
            total_acumulado += total_producto

            # Muestra el total del producto actual
            st.write("**Total del producto:**", total_producto)

        else:
            st.write("Producto no encontrado.")

        # Muestra el total acumulado
        st.write("**Total acumulado:**", total_acumulado)

    except Exception as e:
        st.write(f"Error al buscar el producto: {e}")