import streamlit as st
import pandas as pd

from services.dashboard_service import (
    obter_indicadores_dashboard,
    obter_ultimas_reunioes,
    obter_ultimos_feedbacks,
    obter_planos_pendentes,
    obter_radares_recentes
)

from utils.datas import formatar_data_br


st.title("📊 Dashboard Executivo")

st.info(
    "Visão geral da liderança, equipe e acompanhamentos."
)

indicadores = obter_indicadores_dashboard()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👥 Colaboradores Ativos",
        indicadores["colaboradores_ativos"]
    )

with col2:
    st.metric(
        "🤝 Reuniões no Mês",
        indicadores["reunioes_mes"]
    )

with col3:
    st.metric(
        "📝 Feedbacks no Mês",
        indicadores["feedbacks_mes"]
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "📋 Planos Pendentes",
        indicadores["planos_pendentes"]
    )

with col5:
    st.metric(
        "⚠️ Em Atenção",
        indicadores["colaboradores_atencao"]
    )

with col6:
    st.metric(
        "🔥 Destaque",
        indicadores["colaboradores_destaque"]
    )

st.divider()

aba1, aba2, aba3, aba4 = st.tabs(
    [
        "Reuniões",
        "Feedbacks",
        "Planos",
        "Radar"
    ]
)

with aba1:

    reunioes = obter_ultimas_reunioes()

    if reunioes:

        tabela = []

        for r in reunioes:

            tabela.append(
                {
                    "Data": formatar_data_br(r["data"]),
                    "Colaborador": r["colaborador_nome"],
                    "Tipo": r["tipo"],
                    "Status": r["status"]
                }
            )

        st.dataframe(
            pd.DataFrame(tabela),
            use_container_width=True,
            hide_index=True
        )

with aba2:

    feedbacks = obter_ultimos_feedbacks()

    if feedbacks:

        tabela = []

        for f in feedbacks:

            tabela.append(
                {
                    "Data": formatar_data_br(f["data"]),
                    "Colaborador": f["colaborador_nome"],
                    "Tipo": f["tipo"],
                    "Status": f["status_acompanhamento"]
                }
            )

        st.dataframe(
            pd.DataFrame(tabela),
            use_container_width=True,
            hide_index=True
        )

with aba3:

    planos = obter_planos_pendentes()

    if planos:

        tabela = []

        for p in planos:

            tabela.append(
                {
                    "Prazo": formatar_data_br(p["prazo"]),
                    "Colaborador": p["colaborador_nome"],
                    "Título": p["titulo"],
                    "Status": p["status"]
                }
            )

        st.dataframe(
            pd.DataFrame(tabela),
            use_container_width=True,
            hide_index=True
        )

with aba4:

    radares = obter_radares_recentes()

    if radares:

        tabela = []

        for r in radares:

            tabela.append(
                {
                    "Data": formatar_data_br(r["data_registro"]),
                    "Colaborador": r["colaborador_nome"],
                    "Motivação": r["motivacao"],
                    "Performance": r["performance"],
                    "Risco": r["risco_desgaste"]
                }
            )

        st.dataframe(
            pd.DataFrame(tabela),
            use_container_width=True,
            hide_index=True
        )