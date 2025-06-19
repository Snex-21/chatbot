import streamlit as st
from groq import Groq
st.set_page_config(page_title='Mi IA', page_icon='', layout='centered')
# 🤪
st.title('mi chatbot')

nombre = st.text_input('tu nombre? ')

if st.button('saludar'):
    st.write(f'hola {nombre}')

modelos_ia = ['llama3-8b-8192', 'llama3-70b-8192', 'gemma2-9b-it']

def configuracion_pag():
    st.title('chat')
    st.sidebar.title('opciones de modelos')
    eleccion_modelo = st.sidebar.selectbox('elegi un modelo', options=modelos_ia, index=0)
    return eleccion_modelo

def usuario_groq():
    clave_secreta = st.secrets['api_key']
    return Groq(api_key=clave_secreta)

def confi_modelo(cliente, modelo, prompt):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{'role':'user', 'content': prompt}],
        stream=True
    )

def inicializar():
    if 'mensajes' not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({
        'rol':rol,
        'contenido':contenido,
        'avatar':avatar
    })

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje['rol'], avatar=mensaje['avatar']):
            st.markdown(mensaje['contenido'])

def area_chat():
    contenedor_del_chat = st.container(height=300, border=True)
    with contenedor_del_chat:
        mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = ''
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    modelo = configuracion_pag()
    cliente_usuario = usuario_groq()
    inicializar()
    area_chat()
    
    mensaje = st.chat_input('escribi tu mensaje')
    if mensaje:
        actualizar_historial('user',mensaje, '\U0001F9D1')
        chat_completo = confi_modelo(cliente_usuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message('assistant'):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial('assistant', respuesta_completa, '\U0001F916')

main()    
