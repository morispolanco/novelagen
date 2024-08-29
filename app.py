import streamlit as st
import requests
import json
import time
from docx import Document
from io import BytesIO

# Configurar la clave de API de Together
TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]

def generate_text(prompt, max_tokens=1000):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["<|eot_id|>", "<|eom_id|>"]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Error al generar texto: {str(e)}")
        return ""

def generate_novel_outline(title, genre):
    prompt = f"Genera una sinopsis, trama, personajes, ambiente, técnica narrativa y tabla de contenidos para una novela titulada '{title}' del género '{genre}'."
    return generate_text(prompt, max_tokens=1000)

def generate_chapter(title, genre, chapter_number, total_chapters):
    prompt = f"Escribe el capítulo {chapter_number} de {total_chapters} para una novela titulada '{title}' del género '{genre}'. El capítulo debe tener aproximadamente 5 páginas. Usa la raya (—) para los diálogos de los personajes."
    return generate_text(prompt, max_tokens=2000)

def export_to_docx(title, content):
    doc = Document()
    doc.add_heading(title, 0)
    
    for line in content.split('\n'):
        if line.startswith('Capítulo'):
            doc.add_heading(line, level=1)
        else:
            doc.add_paragraph(line)
    
    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    return doc_io

st.title("Generador de Novelas")

title = st.text_input("Título de la novela:")
genre = st.text_input("Género de la novela:")

if st.button("Generar Esquema de la Novela"):
    if title and genre:
        with st.spinner("Generando esquema de la novela..."):
            novel_outline = generate_novel_outline(title, genre)
            st.write(novel_outline)
    else:
        st.warning("Por favor, introduce el título y el género de la novela.")

num_chapters = st.number_input("Número de capítulos (máximo 24):", min_value=1, max_value=24, value=1)

if st.button("Generar Capítulos"):
    if title and genre:
        novel_content = ""
        progress_bar = st.progress(0)
        for i in range(1, num_chapters + 1):
            with st.spinner(f"Generando capítulo {i}..."):
                chapter_content = generate_chapter(title, genre, i, num_chapters)
                novel_content += f"\n\nCapítulo {i}\n\n{chapter_content}"
                progress_bar.progress(i / num_chapters)
                time.sleep(1)  # Para evitar sobrecargar la API
        
        st.write("Novela generada:")
        st.text_area("Contenido de la novela:", novel_content, height=500)
        
        # Botón para exportar a DOCX
        if st.button("Exportar a DOCX"):
            docx_file = export_to_docx(title, novel_content)
            st.download_button(
                label="Descargar DOCX",
                data=docx_file,
                file_name=f"{title}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    else:
        st.warning("Por favor, introduce el título y el género de la novela.")
