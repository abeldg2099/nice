import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
from urllib.parse import unquote

# Ruta al archivo CSV
ruta_csv = "https://drive.google.com/uc?export=download&id=1u6qi--pwtEcBQgPb0NZHhE-DTcAzvaDa"

try:
    df_productos = pd.read_csv(ruta_csv)
except Exception as e:
    st.error(f"Error al leer el archivo CSV: {e}")
    st.stop()

st.title("Catalogo de Productos")

metodo_busqueda = st.radio("Selecciona el método de búsqueda:", ("Por Código", "Por Imagen"))

if metodo_busqueda == "Por Código":
    # (Código de búsqueda por código sin cambios)
    # ... (Código anterior para búsqueda por código)
    id_producto = st.text_input("Introduce el ID del producto:")
    total_acumulado = 0

    if id_producto:
        try:
            producto = df_productos[df_productos['ID'] == id_producto].iloc[0]
            if not producto.empty:

                st.write(f"**Descripción:** {producto['DESCRIPCION']}")

                try:
                    response = requests.get(producto["imagen"], stream=True)
                    response.raise_for_status()
                    imagen = Image.open(BytesIO(response.content))
                    st.image(imagen, caption=producto["DESCRIPCION"], use_column_width=True)
                except requests.exceptions.RequestException as e:
                    st.error(f"Error al cargar la imagen: {e}")
                except Exception as e:
                    st.error(f"Error al procesar la imagen: {e}")

                cantidad = st.number_input("Cantidad:", min_value=1, value=1)
                precio_individual = float(str(producto["PRECIO CATALOGO"]).replace("$", "").replace(",", ""))
                st.write(f"**Precio individual:** ${precio_individual:.2f}")

                total_producto = cantidad * precio_individual
                total_acumulado += total_producto
                st.write(f"**Total del producto:** ${total_producto:.2f}")
            else:
                st.warning("Producto no encontrado.")

        except Exception as e:
            st.error(f"Error al buscar el producto: {e}")

        st.write(f"**Total acumulado:** ${total_acumulado:.2f}")

elif metodo_busqueda == "Por Imagen":
    imagenes_mostradas = {}  # Diccionario para almacenar las imágenes ya mostradas por ID
    total_acumulado = 0

    st.write("### Galería de Imágenes")

    for index, row in df_productos.iterrows():
        id_producto = row['ID']
        imagen_url = row['imagen'].strip()
        imagen_url = unquote(imagen_url)

        if id_producto not in imagenes_mostradas:  # Verifica si ya se mostró una imagen para este ID
            try:
                response = requests.get(imagen_url, stream=True, timeout=10)
                response.raise_for_status()
                imagen = Image.open(BytesIO(response.content))

                # Crear columnas para mostrar la imagen y el botón
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.image(imagen, caption=row["DESCRIPCION"], use_container_width=True)

                with col2:
                    if st.button(f"Seleccionar {row['ID']}", key=f"btn-{id_producto}"):
                        st.write(f"**Descripción:** {row['DESCRIPCION']}")
                        precio_individual = float(str(row["PRECIO CATALOGO"]).replace("$", "").replace(",", ""))
                        st.write(f"**Precio individual:** ${precio_individual:.2f}")

                imagenes_mostradas[id_producto] = True  # Marca este ID como ya mostrado

            except requests.exceptions.RequestException as e:
                st.error(f"Error al cargar la imagen desde {imagen_url}: {e}")
            except Exception as e:
                st.error(f"Error al procesar la imagen desde {imagen_url}: {e}")
