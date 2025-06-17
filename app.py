import streamlit as st
import openai

# Si usas secrets.toml
# openai.api_key = st.secrets["openai_api_key"]

# O escribe tu API key directo (NO lo subas a GitHub si lo haces)
openai.api_key = "zuleycacalderonc"

st.set_page_config(page_title="Asistente Escolar", page_icon="📘")
st.title("📘 Asistente Escolar con IA")
st.markdown("Haz una pregunta escolar y la IA te responderá:")

pregunta = st.text_input("📎 Escribe tu pregunta")

if st.button("Responder"):
    if pregunta:
        with st.spinner("Pensando..."):
            respuesta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente escolar que explica con claridad temas escolares."},
                    {"role": "user", "content": pregunta}
                ]
            )
            st.success(respuesta.choices[0].message["content"])
    else:
        st.warning("Por favor, escribe una pregunta.")

