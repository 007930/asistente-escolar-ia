import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=st.secrets["zuleycacalderonc"])

st.set_page_config(page_title="Asistente Escolar", page_icon="📘")
st.title("📘 Asistente Escolar con IA")
st.markdown("Haz una pregunta escolar y la IA te responderá:")

pregunta = st.text_input("📎 Escribe tu pregunta")

if st.button("Responder"):
    if pregunta:
        with st.spinner("Pensando..."):
            respuesta = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente escolar que explica con claridad temas escolares."},
                    {"role": "user", "content": pregunta}
                ]
            )
            st.success(respuesta.choices[0].message.content)
    else:
        st.warning("Por favor, escribe una pregunta.")


