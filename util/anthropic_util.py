import streamlit as st
from anthropic import Anthropic

def initialize_claude():
    """Inicializa el cliente de Claude con la API key"""
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    return Anthropic(api_key=api_key)

def get_claude_response(client, question, context=""):
    """
    Obtiene una respuesta de Claude
    Args:
        client: Cliente de Anthropic
        question: Pregunta del usuario
        context: Contexto adicional opcional
    """
    try:
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.7,
            system="Eres un asistente experto en finanzas y mercados. Proporciona respuestas concisas y precisas.",
            messages=[
                {
                    "role": "user",
                    "content": f"Contexto: {context}\nPregunta: {question}"
                }
            ]
        )
        # Extraer solo el texto de la respuesta
        clean_response = message.content[0].text
        return clean_response
    except Exception as e:
        return f"Error al obtener respuesta: {str(e)}"

def display_chat_interface():
    st.subheader("💬 Consulta con IA")
    
    # Inicializar el historial de chat si no existe
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar mensajes anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input del usuario
    if prompt := st.chat_input("Escribe tu pregunta aquí..."):
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Obtener y mostrar respuesta de Claude
        with st.chat_message("assistant"):
            client = initialize_claude()
            response = get_claude_response(client, prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            