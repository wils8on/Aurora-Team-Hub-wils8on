from utils.auth import exigir_login
from utils.auth import mostrar_usuario_sidebar

exigir_login()
mostrar_usuario_sidebar()

import streamlit as st
import pandas as pd

from services.colaboradores_service import listar_colaboradores
from services.colaboradores_service import obter_colaborador_360

from services.copilot_service import (
    colaboradores_em_atencao,
    colaboradores_sem_1_1,
    planos_pendentes_copilot,
    resumo_equipe,
    gerar_resumo_colaborador,
    gerar_analise_equipe
)


st.title("🤖 Aurora Copilot")

st.info("Assistente inteligente de liderança e gestão baseado nos dados do Aurora Team Hub.")

opcao = st.selectbox(
    "O que deseja analisar?",
    [
        "Quem precisa da minha atenção?",
        "Quem está sem 1:1?",
        "Quais planos estão pendentes?",
        "Resumo da equipe",
        "Resumo Executivo do Colaborador",
        "Análise Executiva da Equipe"
    ]
)

st.divider()

if opcao == "Quem precisa da minha atenção?":

    dados = colaboradores_em_atencao()

    if not dados:
        st.success("Nenhum colaborador requer atenção imediata.")
    else:
        for item in dados:
            st.warning(
                f"""
**{item['nome']}**

Motivo: {item['motivo']}

Recomendação: {item['recomendacao']}
"""
            )

elif opcao == "Quem está sem 1:1?":

    dados = colaboradores_sem_1_1()

    if not dados:
        st.success("Todos os colaboradores ativos possuem reuniões registradas.")
    else:
        st.dataframe(
            pd.DataFrame(dados),
            use_container_width=True,
            hide_index=True
        )

elif opcao == "Quais planos estão pendentes?":

    dados = planos_pendentes_copilot()

    if not dados:
        st.success("Nenhum plano pendente.")
    else:
        st.dataframe(
            pd.DataFrame(dados),
            use_container_width=True,
            hide_index=True
        )

elif opcao == "Resumo da equipe":

    st.markdown(resumo_equipe())

elif opcao == "Resumo Executivo do Colaborador":

    colaboradores = listar_colaboradores()

    if not colaboradores:
        st.warning("Nenhum colaborador cadastrado.")
    else:
        colaborador = st.selectbox(
            "Selecione o colaborador",
            colaboradores,
            format_func=lambda item: item.nome
        )

        dados_360 = obter_colaborador_360(colaborador.id)

        st.subheader("🧠 Resumo Executivo do Colaborador")

        st.markdown(
            gerar_resumo_colaborador(dados_360)
        )

elif opcao == "Análise Executiva da Equipe":

    st.subheader("📊 Análise Executiva da Equipe")

    st.markdown(
        gerar_analise_equipe()
    )