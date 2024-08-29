import streamlit as st
import requests
import json

# Configuración de la API de Tune
API_KEY = st.secrets["TUNE_API_KEY"]
API_URL = "https://proxy.tune.app/chat/completions"

# Función para generar la novela
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
                "content": f"Eres un novelista. Crea una novela con el título '{titulo}' y del género '{genero}'. La novela debe tener {num_capitulos} capítulos largos."
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
        novela = respuesta["choices"][0]["message"]["content"]

        # Presentación de la novela
        st.write(novela)

        # Opción para exportar la novela a Docx
        if st.button("Exportar a Docx"):
            # Lógica para exportar la novela a Docx
            pass

    else:
        st.error("Error al generar la novela")

# Interfaz de usuario
st.title("Generador de Novelas")
titulo = st.text_input("Ingrese el título de la novela")
genero = st.selectbox("Seleccione el género de la novela", [
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
num_capitulos = 12

if st.button("Generar Novela"):
    generar_novela(titulo, genero, num_capitulos)
