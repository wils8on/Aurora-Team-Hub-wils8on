from utils.auth import exigir_login
from utils.auth import mostrar_usuario_sidebar

exigir_login()
mostrar_usuario_sidebar()

import streamlit as st
import pandas as pd

from datetime import date

from services.colaboradores_service import listar_colaboradores
from services.colaboradores_service import obter_colaborador_360

from utils.datas import formatar_data_br


st.title("👥 Equipe")

st.info("Painel visual da equipe, riscos, planos abertos e acompanhamento gerencial.")


def classificar_risco(valor):

    if valor == "-":
        return "Sem registro"

    if valor >= 4:
        return "🔴 Alto"

    if valor == 3:
        return "🟡 Moderado"

    return "🟢 Baixo"


def calcular_dias_sem_reuniao(data_ultima_reuniao):

    if not data_ultima_reuniao:
        return None

    return (date.today() - data_ultima_reuniao).days


def montar_resumo_colaborador(colaborador):

    dados_360 = obter_colaborador_360(colaborador.id)

    if not dados_360:
        return None

    reunioes = dados_360["reunioes"]
    feedbacks = dados_360["feedbacks"]
    planos = dados_360["planos"]
    radares = dados_360["radares"]

    ultima_reuniao = reunioes[0]["data"] if reunioes else None
    ultimo_feedback = feedbacks[0]["data"] if feedbacks else None
    ultimo_radar = radares[0] if radares else None

    planos_abertos = [
        plano for plano in planos
        if plano["status"] in ["Pendente", "Em andamento"]
    ]

    planos_atrasados = [
        plano for plano in planos_abertos
        if plano["prazo"] and plano["prazo"] < date.today()
    ]

    risco_radar = (
        ultimo_radar["risco_desgaste"]
        if ultimo_radar
        else "-"
    )

    if risco_radar == "-":
        peso_risco = 0
    else:
        peso_risco = risco_radar

    dias_sem_reuniao = calcular_dias_sem_reuniao(ultima_reuniao)

    return {
        "id": colaborador.id,
        "nome": colaborador.nome,
        "cargo": colaborador.cargo,
        "status": colaborador.status,
        "unidade": colaborador.unidade,
        "momento": colaborador.momento_atual,
        "risco_gerencial": colaborador.risco_percebido,
        "ultima_reuniao": ultima_reuniao,
        "ultimo_feedback": ultimo_feedback,
        "planos_abertos": len(planos_abertos),
        "planos_atrasados": len(planos_atrasados),
        "risco_radar": risco_radar,
        "risco_visual": classificar_risco(risco_radar),
        "dias_sem_reuniao": dias_sem_reuniao,
        "peso_risco": peso_risco
    }


colaboradores = listar_colaboradores()

if not colaboradores:
    st.warning("Nenhum colaborador cadastrado ainda.")
    st.stop()


resumos = []

for colaborador in colaboradores:

    resumo = montar_resumo_colaborador(colaborador)

    if resumo:
        resumos.append(resumo)


st.subheader("Indicadores da Equipe")

total_colaboradores = len(resumos)

baixo_risco = len(
    [
        item for item in resumos
        if item["risco_radar"] != "-"
        and item["risco_radar"] <= 2
    ]
)

risco_moderado = len(
    [
        item for item in resumos
        if item["risco_radar"] == 3
    ]
)

alto_risco = len(
    [
        item for item in resumos
        if item["risco_radar"] != "-"
        and item["risco_radar"] >= 4
    ]
)

planos_abertos_total = sum(
    item["planos_abertos"]
    for item in resumos
)

planos_atrasados_total = sum(
    item["planos_atrasados"]
    for item in resumos
)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("👥 Total", total_colaboradores)

with col2:
    st.metric("🟢 Baixo", baixo_risco)

with col3:
    st.metric("🟡 Moderado", risco_moderado)

with col4:
    st.metric("🔴 Alto", alto_risco)

with col5:
    st.metric("📋 Planos abertos", planos_abertos_total)

with col6:
    st.metric("⚠️ Planos atrasados", planos_atrasados_total)


st.divider()

st.subheader("Filtros")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    filtro_status = st.selectbox(
        "Status",
        ["Todos"] + sorted(list(set([item["status"] for item in resumos if item["status"]])))
    )

with col_f2:
    filtro_unidade = st.selectbox(
        "Unidade",
        ["Todas"] + sorted(list(set([item["unidade"] for item in resumos if item["unidade"]])))
    )

with col_f3:
    filtro_risco = st.selectbox(
        "Risco Radar",
        [
            "Todos",
            "Baixo",
            "Moderado",
            "Alto",
            "Sem registro"
        ]
    )


resumos_filtrados = resumos

if filtro_status != "Todos":
    resumos_filtrados = [
        item for item in resumos_filtrados
        if item["status"] == filtro_status
    ]

if filtro_unidade != "Todas":
    resumos_filtrados = [
        item for item in resumos_filtrados
        if item["unidade"] == filtro_unidade
    ]

if filtro_risco == "Baixo":
    resumos_filtrados = [
        item for item in resumos_filtrados
        if item["risco_radar"] != "-"
        and item["risco_radar"] <= 2
    ]

elif filtro_risco == "Moderado":
    resumos_filtrados = [
        item for item in resumos_filtrados
        if item["risco_radar"] == 3
    ]

elif filtro_risco == "Alto":
    resumos_filtrados = [
        item for item in resumos_filtrados
        if item["risco_radar"] != "-"
        and item["risco_radar"] >= 4
    ]

elif filtro_risco == "Sem registro":
    resumos_filtrados = [
        item for item in resumos_filtrados
        if item["risco_radar"] == "-"
    ]


resumos_filtrados = sorted(
    resumos_filtrados,
    key=lambda item: (
        item["peso_risco"],
        item["planos_atrasados"],
        item["planos_abertos"]
    ),
    reverse=True
)


st.divider()

st.subheader("Cards da Equipe")

if resumos_filtrados:

    for item in resumos_filtrados:

        with st.container(border=True):

            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                st.markdown(f"### {item['nome']}")
                st.write(item["cargo"] or "-")
                st.write(f"**Status:** {item['status'] or '-'}")
                st.write(f"**Unidade:** {item['unidade'] or '-'}")
                st.write(f"**Momento:** {item['momento'] or '-'}")

            with col2:
                st.metric(
                    "Última 1:1",
                    formatar_data_br(item["ultima_reuniao"])
                )

                if item["dias_sem_reuniao"] is not None:
                    st.caption(f"{item['dias_sem_reuniao']} dias desde a última reunião")
                else:
                    st.caption("Sem reunião registrada")

                st.metric(
                    "Último feedback",
                    formatar_data_br(item["ultimo_feedback"])
                )

            with col3:
                st.metric(
                    "Planos abertos",
                    item["planos_abertos"]
                )

                st.metric(
                    "Planos atrasados",
                    item["planos_atrasados"]
                )

                st.write("**Risco Radar:**")
                st.markdown(f"### {item['risco_visual']}")

else:
    st.warning("Nenhum colaborador encontrado com os filtros selecionados.")


st.divider()

st.subheader("Tabela Resumo")

if resumos_filtrados:

    tabela = []

    for item in resumos_filtrados:
        tabela.append(
            {
                "Nome": item["nome"],
                "Cargo": item["cargo"],
                "Status": item["status"],
                "Unidade": item["unidade"],
                "Última 1:1": formatar_data_br(item["ultima_reuniao"]),
                "Último feedback": formatar_data_br(item["ultimo_feedback"]),
                "Planos abertos": item["planos_abertos"],
                "Planos atrasados": item["planos_atrasados"],
                "Risco Radar": item["risco_visual"],
                "Momento": item["momento"]
            }
        )

    st.dataframe(
        pd.DataFrame(tabela),
        use_container_width=True,
        hide_index=True
    )