import streamlit as st
import requests
import json

# Configuración de la API de Tune
API_KEY = st.secrets["TUNE_API_KEY"]
API_URL = "https://proxy.tune.app/chat/completions"

# Función para generar la estructura de la novela
def generar_novela(titulo, genero, num_capitulos):
    # Configuración de la solicitud a la API de Tune
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "temperature": 0.8,
        "messages": [
            {
                "role": "system",
                "content": f"Eres un novelista. Crea una novela con el título '{titulo}' y del género '{genero}'. La novela debe tener {num_capitulos} capítulos."
            }
        ],
        "model": "meta/llama-3.1-8b-instruct",
        "stream": False,
        "frequency_penalty": 1.04,
        "max_tokens": 3898
    }

    # Envío de la solicitud a la API de Tune
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    # Procesamiento de la respuesta
    if response.status_code == 200:
        respuesta = response.json()
        sinopsis = respuesta["choices"][0]["message"]["content"]

        # Verificar si hay más respuestas
        if len(respuesta["choices"]) > 1:
            trama = respuesta["choices"][1]["message"]["content"]
            personajes = respuesta["choices"][2]["message"]["content"]
            ambientacion = respuesta["choices"][3]["message"]["content"]
            tecnica_narrativa = respuesta["choices"][4]["message"]["content"]
            tabla_contenidos = respuesta["choices"][5]["message"]["content"]
        else:
            trama = ""
            personajes = ""
            ambientacion = ""
            tecnica_narrativa = ""
            tabla_contenidos = ""

        # Presentación de la estructura de la novela
        st.write("Sinopsis:")
        st.write(sinopsis)
        st.write("Trama:")
        st.write(trama)
        st.write("Personajes:")
        st.write(personajes)
        st.write("Ambientación:")
        st.write(ambientacion)
        st.write("Técnica narrativa:")
        st.write(tecnica_narrativa)
        st.write("Tabla de contenidos:")
        st.write(tabla_contenidos)

        # Botón para generar capítulos
        if st.button("Generar Capítulos"):
            # Lógica para generar capítulos
            pass

        # Opción para exportar la novela a Docx
        if st.button("Exportar a Docx"):
            # Lógica para exportar la novela a Docx
            pass

    else:
        st.error("Error al generar la novela")

# Interfaz de usuario
st.title("Generador de Novelas")
titulo = st.text_input("Ingrese el título de la novela")
genero = st.selectbox("Seleccione el género de la novela", ["Aventuras", "Ciencia Ficción", "Fantasía", "Misterio", "Romance"])
num_capitulos = st.number_input("Ingrese el número de capítulos", min_value=1, max_value=100)

if st.button("Generar Novela"):
    generar_novela(titulo, genero, num_capitulos)
