import streamlit as st

from utils.style import aplicar_estilo

st.set_page_config(
    page_title="Aurora Team Hub",
    page_icon="🌅",
    layout="wide"
)

aplicar_estilo()

st.title("🌅 Aurora Team Hub")

st.markdown("""
### Hub pessoal de liderança, gestão de equipe e acompanhamento individual

Bem-vindo ao seu centro de comando gerencial.

Use o menu lateral para acessar:

- Dashboard Executivo
- Colaboradores
- Reuniões
- Feedbacks
- Planos de Ação
- Agenda
- Radar do Colaborador
- Notas Rápidas
- Configurações
""")

st.info("Sistema em desenvolvimento modular. Próxima etapa: módulo de reuniões.")