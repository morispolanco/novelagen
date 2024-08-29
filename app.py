import streamlit as st
import requests
import json
import time
from docx import Document
from io import BytesIO

# Configuración de la API de Together
API_URL = "https://api.together.xyz/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {st.secrets['TOGETHER_API_KEY']}",
    "Content-Type": "application/json"
}

def generate_novel_element(prompt, max_tokens=500):
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
    
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        st.error(f"Error en la API: {response.status_code}")
        return None

def generate_chapter(chapter_number, title, genre, synopsis, characters, max_tokens=2000):
    prompt = f"""Escribe el capítulo {chapter_number} de una novela con las siguientes características:
    Título: {title}
    Género: {genre}
    Sinopsis: {synopsis}
    Personajes principales: {', '.join(characters)}
    
    El capítulo debe tener aproximadamente 5 páginas. Usa la raya (—) para los diálogos de los personajes.
    
    Capítulo {chapter_number}:
    """
    return generate_novel_element(prompt, max_tokens)

def export_to_docx(title, genre, novel_elements, chapters):
    doc = Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(f"Género: {genre}")
    
    for element_title, content in novel_elements.items():
        doc.add_heading(element_title, level=1)
        doc.add_paragraph(content)
    
    for i, chapter in enumerate(chapters, 1):
        doc.add_heading(f"Capítulo {i}", level=1)
        doc.add_paragraph(chapter)
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def main():
    st.title("Generador de Novelas")
    
    title = st.text_input("Título de la novela:")
    genre = st.text_input("Género de la novela:")
    num_chapters = st.number_input("Número de capítulos (máximo 24):", min_value=1, max_value=24, value=1)
    
    novel_elements = {}
    chapters = []
    
    if st.button("Generar esquema de la novela"):
        with st.spinner("Generando elementos de la novela..."):
            novel_elements['Sinopsis'] = generate_novel_element(f"Escribe una sinopsis para una novela titulada '{title}' del género {genre}.")
            novel_elements['Trama'] = generate_novel_element(f"Describe la trama principal de una novela titulada '{title}' del género {genre}.")
            novel_elements['Personajes'] = generate_novel_element(f"Enumera y describe brevemente los personajes principales de una novela titulada '{title}' del género {genre}.")
            novel_elements['Ambiente'] = generate_novel_element(f"Describe el ambiente y escenario de una novela titulada '{title}' del género {genre}.")
            novel_elements['Técnica Narrativa'] = generate_novel_element(f"Explica la técnica narrativa utilizada en una novela titulada '{title}' del género {genre}.")
            novel_elements['Tabla de Contenidos'] = generate_novel_element(f"Crea una tabla de contenidos con {num_chapters} capítulos para una novela titulada '{title}' del género {genre}.")
            
            for element_title, content in novel_elements.items():
                if content:
                    st.subheader(element_title)
                    st.write(content)
    
    if st.button("Generar capítulos"):
        characters_list = novel_elements.get('Personajes', '').split(',')
        synopsis = novel_elements.get('Sinopsis', '')
        
        for chapter in range(1, num_chapters + 1):
            with st.spinner(f"Generando capítulo {chapter}..."):
                chapter_content = generate_chapter(chapter, title, genre, synopsis, characters_list)
                if chapter_content:
                    chapters.append(chapter_content)
                    st.subheader(f"Capítulo {chapter}")
                    st.write(chapter_content)
                time.sleep(1)  # Pausa para evitar sobrecargar la API
        
        st.success("¡Todos los capítulos han sido generados!")
    
    if novel_elements and chapters:
        docx_buffer = export_to_docx(title, genre, novel_elements, chapters)
        st.download_button(
            label="Descargar novela en DOCX",
            data=docx_buffer,
            file_name=f"{title}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

if __name__ == "__main__":
    main()
