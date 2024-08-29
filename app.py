import streamlit as st
import requests
import json

# Configuración de la API de Tune
API_KEY = st.secrets["TUNE_API_KEY"]
API_URL = "https://proxy.tune.app/chat/completions"

# Función para generar el cuento
def generar_cuento(titulo, autor, genero):
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
                "content": f"Eres un escritor latinoamericano. Crea un cuento largo en el estilo de {autor} con el título '{titulo}' y del género '{genero}'."
            }
        ],
        "model": "meta/llama-3.1-8b-instruct",
        "stream": False,
        "frequency_penalty": 1.04,
        "max_tokens": 10000
    }

    # Envío de la solicitud a la API de Tune
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    # Procesamiento de la respuesta
    if response.status_code == 200:
        respuesta = response.json()
        cuento = respuesta["choices"][0]["message"]["content"]

        # Presentación del cuento
        st.write(cuento)

        # Opción para exportar el cuento a Docx
        if st.button("Exportar a Docx"):
            # Lógica para exportar el cuento a Docx
            pass

    else:
        st.error("Error al generar el cuento")

# Interfaz de usuario
st.title("Generador de Cuentos")
titulo = st.text_input("Ingrese el título del cuento")
autor = st.selectbox("Seleccione el autor latinoamericano que imitará el estilo del cuento", [
    "Gabriel García Márquez",
    "Isabel Allende",
    "Mario Vargas Llosa",
    "Julio Cortázar",
    "Jorge Luis Borges"
])
genero = st.selectbox("Seleccione el género del cuento", [
    "Aventuras",
    "Ciencia Ficción",
    "Fantasía",
    "Misterio",
    "Romance",
    "Terror",
    "Drama",
    "Comedia",
    "Historia",
    "Ficción histórica",
    "Ficción científica",
    "Ficción de aventuras",
    "Ficción de misterio",
    "Ficción de terror"
])

if st.button("Generar Cuento"):
    generar_cuento(titulo, autor, genero)
