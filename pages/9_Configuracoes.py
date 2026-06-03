from utils.auth import exigir_login
from utils.auth import mostrar_usuario_sidebar

exigir_login()
mostrar_usuario_sidebar()

import streamlit as st

st.title("⚙️ Configurações")

st.info(
    "Personalize o funcionamento do Aurora Team Hub."
)

st.subheader("Configurações Gerais")

st.info(
    "Parâmetros do sistema serão exibidos aqui."
)

st.subheader("Integrações")

st.info(
    "Google Calendar, Gmail e IA serão configurados aqui."
)