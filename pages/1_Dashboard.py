from utils.auth import exigir_login
from utils.auth import mostrar_usuario_sidebar

exigir_login()
mostrar_usuario_sidebar()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from services.dashboard_service import (
    obter_dados_base,
    obter_indicadores_dashboard,
    obter_alertas_dashboard,
    obter_saude_equipe,
    obter_ultimas_reunioes,
    obter_ultimos_feedbacks,
    obter_planos_pendentes,
    obter_radares_recentes
)

from services.insights_service import gerar_insights_dashboard
from utils.datas import formatar_data_br


st.title("📊 Dashboard Estratégico")

st.info("Cockpit gerencial do Aurora Team Hub: indicadores, riscos, prioridades e saúde da equipe.")


dados = obter_dados_base()
indicadores = obter_indicadores_dashboard()
alertas = obter_alertas_dashboard()
saude = obter_saude_equipe()
insights = gerar_insights_dashboard()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👥 Colaboradores Ativos", indicadores["colaboradores_ativos"])

with col2:
    st.metric("🤝 Reuniões 30 dias", indicadores["reunioes_30_dias"])

with col3:
    st.metric("📝 Feedbacks Abertos", indicadores["feedbacks_abertos"])

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("📋 Planos em Andamento", indicadores["planos_andamento"])

with col5:
    st.metric("⚠️ Planos Atrasados", indicadores["planos_atrasados"])

with col6:
    st.metric("📡 Radar 30 dias", indicadores["radares_30_dias"])


st.divider()

st.subheader("🔥 Prioridades Estratégicas")

prioridades = []

for insight in insights:
    if insight["nivel"] in ["Crítico", "Atenção"]:
        prioridades.append(
            {
                "Nível": insight["nivel"],
                "Colaborador": insight["colaborador_nome"],
                "Motivação": insight["motivacao"],
                "Performance": insight["performance"],
                "Engajamento": insight["engajamento"],
                "Risco": insight["risco_desgaste"],
                "Recomendação": insight["recomendacao"]
            }
        )

if prioridades:
    st.dataframe(
        pd.DataFrame(prioridades),
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("Nenhuma prioridade crítica identificada no momento.")


st.divider()

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("📋 Distribuição dos Planos")

    planos = dados["planos"]

    if planos:
        df_planos = pd.DataFrame(planos)

        distribuicao_planos = (
            df_planos["status"]
            .value_counts()
            .reset_index()
        )

        distribuicao_planos.columns = ["Status", "Quantidade"]

        fig_planos = px.pie(
            distribuicao_planos,
            names="Status",
            values="Quantidade",
            hole=0.45
        )

        fig_planos.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=350
        )

        st.plotly_chart(
            fig_planos,
            use_container_width=True
        )
    else:
        st.info("Nenhum plano cadastrado.")


with col_g2:
    st.subheader("📡 Radar Geral da Equipe")

    if saude:
        categorias = [
            "Motivação",
            "Performance",
            "Engajamento",
            "Risco",
            "Alinhamento"
        ]

        valores = [
            saude["motivacao"],
            saude["performance"],
            saude["engajamento"],
            saude["risco"],
            saude["alinhamento"]
        ]

        fig_radar = go.Figure()

        fig_radar.add_trace(
            go.Scatterpolar(
                r=valores,
                theta=categorias,
                fill="toself",
                name="Saúde da Equipe"
            )
        )

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )
            ),
            showlegend=False,
            height=350,
            margin=dict(t=10, b=10, l=10, r=10)
        )

        st.plotly_chart(
            fig_radar,
            use_container_width=True
        )
    else:
        st.info("Ainda não há dados suficientes no Radar.")


st.divider()

st.subheader("🏆 Destaques e Atenções")

radares = dados["radares"]

ultimos_por_colaborador = {}

for radar in radares:
    colaborador_id = radar["colaborador_id"]

    if colaborador_id not in ultimos_por_colaborador:
        ultimos_por_colaborador[colaborador_id] = radar

destaques = []
atencao = []

for radar in ultimos_por_colaborador.values():

    if (
        radar["motivacao"] >= 4
        and radar["performance"] >= 4
        and radar["engajamento"] >= 4
        and radar["risco_desgaste"] <= 2
    ):
        destaques.append(
            {
                "Colaborador": radar["colaborador_nome"],
                "Motivação": radar["motivacao"],
                "Performance": radar["performance"],
                "Engajamento": radar["engajamento"],
                "Risco": radar["risco_desgaste"],
                "Leitura": "Excelente momento profissional"
            }
        )

    if (
        radar["risco_desgaste"] >= 4
        or radar["motivacao"] <= 2
        or radar["engajamento"] <= 2
    ):
        atencao.append(
            {
                "Colaborador": radar["colaborador_nome"],
                "Motivação": radar["motivacao"],
                "Performance": radar["performance"],
                "Engajamento": radar["engajamento"],
                "Risco": radar["risco_desgaste"],
                "Leitura": "Recomendado acompanhamento próximo"
            }
        )

col_d1, col_d2 = st.columns(2)

with col_d1:
    st.markdown("### 🏆 Destaques")

    if destaques:
        st.dataframe(
            pd.DataFrame(destaques),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhum destaque identificado no radar atual.")

with col_d2:
    st.markdown("### ⚠️ Em Atenção")

    if atencao:
        st.dataframe(
            pd.DataFrame(atencao),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("Nenhum colaborador em atenção crítica.")


st.divider()

st.subheader("🧠 Insights da Equipe")

if insights:

    for insight in insights:

        texto = (
            f"**{insight['colaborador_nome']}** — "
            f"{insight['mensagem']}\n\n"
            f"**Recomendação:** {insight['recomendacao']}"
        )

        if insight["nivel"] == "Crítico":
            st.error(texto)

        elif insight["nivel"] == "Atenção":
            st.warning(texto)

        elif insight["nivel"] == "Positivo":
            st.success(texto)

        else:
            st.info(texto)

else:
    st.info("Ainda não há dados suficientes para gerar insights.")


st.divider()

st.subheader("⚠️ Alertas Gerenciais")

if alertas:
    for alerta in alertas:
        st.warning(alerta)
else:
    st.success("Nenhum alerta crítico no momento.")


st.divider()

aba1, aba2, aba3, aba4 = st.tabs(
    [
        "Últimas Reuniões",
        "Feedbacks Recentes",
        "Planos Pendentes",
        "Radar Recente"
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
                    "Status": r["status"],
                    "Assunto": r["assunto_principal"]
                }
            )

        st.dataframe(
            pd.DataFrame(tabela),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhuma reunião registrada.")

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
    else:
        st.info("Nenhum feedback registrado.")

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
                    "Prioridade": p["prioridade"],
                    "Status": p["status"]
                }
            )

        st.dataframe(
            pd.DataFrame(tabela),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhum plano pendente.")

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
                    "Engajamento": r["engajamento"],
                    "Risco": r["risco_desgaste"]
                }
            )

        st.dataframe(
            pd.DataFrame(tabela),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhum registro de radar.")