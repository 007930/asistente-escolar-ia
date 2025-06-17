import streamlit as st
import openai

# Configuración de la app
st.set_page_config(page_title="Asistente Escolar con IA", page_icon="🎓")
st.title("🎓 Asistente Escolar con IA")

# Input para la API Key
api_key = st.text_input("🔑 Introduce tu API Key de OpenAI", type="password")

# Modo de interacción
modo = st.selectbox("Selecciona el modo:", ["🎒 Estudiante", "👨‍🏫 Profesor", "🧪 Modo Test"])

# Inicializar historial
if "historial" not in st.session_state:
    st.session_state["historial"] = []

# ------------------- MODO CHAT (Estudiante / Profesor) -------------------
if api_key and modo in ["🎒 Estudiante", "👨‍🏫 Profesor"]:
    openai.api_key = api_key
    pregunta = st.text_input("💬 Escribe tu pregunta:")

    if pregunta:
        if modo == "🎒 Estudiante":
            prompt = f"Eres un asistente amigable que ayuda a estudiantes de secundaria. Responde de forma clara y sencilla. Pregunta: {pregunta}"
        else:
            prompt = f"Eres un asistente que ayuda a profesores a explicar temas a estudiantes. Da sugerencias didácticas. Pregunta: {pregunta}"

        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en educación y tecnología."},
                {"role": "user", "content": prompt}
            ]
        )

        contenido = respuesta["choices"][0]["message"]["content"]
        st.session_state["historial"].append((pregunta, contenido))

    # Mostrar historial
    for user_msg, ai_msg in reversed(st.session_state["historial"]):
        st.markdown(f"🧑 Tú:** {user_msg}")
        st.markdown(f"🤖 IA:** {ai_msg}")
        st.markdown("---")

# ------------------- MODO TEST INTERACTIVO -------------------
elif api_key and modo == "🧪 Modo Test":
    openai.api_key = api_key
    st.subheader("🧪 Modo Test Interactivo")

    # Elegir materia
    materia = st.selectbox("📚 Elige la materia del test:", ["Matemáticas", "Historia", "Ciencias", "Lengua"])

    # Generar preguntas
    if st.button("🎲 Generar preguntas del test"):
        prompt_test = (
            f"Actúa como profesor de {materia}. Crea un test interactivo de 3 preguntas simples para estudiantes de secundaria. "
            "Escríbelas una por una numeradas (1, 2, 3), sin incluir las respuestas. Luego pide al estudiante que las responda."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un profesor creativo y claro."},
                {"role": "user", "content": prompt_test}
            ]
        )

        preguntas_test = response["choices"][0]["message"]["content"]
        st.session_state["preguntas_test"] = preguntas_test
        st.session_state["respuestas_usuario"] = []

    # Mostrar preguntas generadas
    if "preguntas_test" in st.session_state:
        st.markdown("### 📋 Preguntas del Test:")
        st.markdown(st.session_state["preguntas_test"])

        st.markdown("### ✍ Escribe tus respuestas:")
        r1 = st.text_input("Respuesta 1")
        r2 = st.text_input("Respuesta 2")
        r3 = st.text_input("Respuesta 3")

        if st.button("✅ Enviar respuestas y evaluar"):
            respuestas_usuario = f"1. {r1}\n2. {r2}\n3. {r3}"
            prompt_eval = (
                f"Estas son las preguntas del test:\n{st.session_state['preguntas_test']}\n"
                f"Y estas son las respuestas del estudiante:\n{respuestas_usuario}\n"
                "Evalúa cada respuesta (correcta o incorrecta), da un comentario breve y una nota final del 1 al 10."
            )

            evaluacion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un profesor justo y motivador."},
                    {"role": "user", "content": prompt_eval}
                ]
            )

            resultado = evaluacion["choices"][0]["message"]["content"]
            st.markdown("### 📊 Evaluación del Test:")
            st.markdown(resultado)
