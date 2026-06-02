import streamlit as st
import pandas as pd

from datetime import date
from datetime import timedelta

from services.dashboard_service import obter_dados_base
from utils.datas import formatar_data_br


st.title("📅 Agenda Inteligente")

st.info("Prioridades, vencimentos, aniversários e acompanhamentos importantes.")


hoje = date.today()
limite_7_dias = hoje + timedelta(days=7)
limite_30_dias = hoje + timedelta(days=30)

dados = obter_dados_base()

colaboradores = dados["colaboradores"]
feedbacks = dados["feedbacks"]
planos = dados["planos"]


def formatar_aniversario(data_aniversario):

    if not data_aniversario:
        return "-"

    return data_aniversario.strftime("%d/%m")


def aniversario_no_periodo(data_aniversario, dias_limite):

    if not data_aniversario:
        return False

    aniversario_ano_atual = date(
        hoje.year,
        data_aniversario.month,
        data_aniversario.day
    )

    if aniversario_ano_atual < hoje:
        aniversario_ano_atual = date(
            hoje.year + 1,
            data_aniversario.month,
            data_aniversario.day
        )

    return hoje <= aniversario_ano_atual <= hoje + timedelta(days=dias_limite)


def dias_ate_aniversario(data_aniversario):

    if not data_aniversario:
        return None

    aniversario_ano_atual = date(
        hoje.year,
        data_aniversario.month,
        data_aniversario.day
    )

    if aniversario_ano_atual < hoje:
        aniversario_ano_atual = date(
            hoje.year + 1,
            data_aniversario.month,
            data_aniversario.day
        )

    return (aniversario_ano_atual - hoje).days


def classificar_urgencia_prazo(prazo):

    if not prazo:
        return "Sem prazo"

    if prazo < hoje:
        return "🔴 Vencido"

    if prazo == hoje:
        return "🟠 Vence hoje"

    if prazo <= hoje + timedelta(days=3):
        return "🟡 Vence em até 3 dias"

    if prazo <= limite_7_dias:
        return "🔵 Vence em até 7 dias"

    return "⚪ Futuro"


st.subheader("Resumo Executivo")

col1, col2, col3, col4 = st.columns(4)

planos_vencidos = [
    plano for plano in planos
    if plano["prazo"]
    and plano["prazo"] < hoje
    and plano["status"] not in ["Concluído", "Cancelado"]
]

planos_7_dias = [
    plano for plano in planos
    if plano["prazo"]
    and hoje <= plano["prazo"] <= limite_7_dias
    and plano["status"] not in ["Concluído", "Cancelado"]
]

feedbacks_revisao = [
    feedback for feedback in feedbacks
    if feedback["data_revisao"]
    and feedback["data_revisao"] <= limite_7_dias
    and feedback["status_acompanhamento"] in ["Aberto", "Em acompanhamento"]
]

colaboradores_1_1_vencida = [
    colaborador for colaborador in colaboradores
    if colaborador.status == "Ativo"
    and colaborador.proxima_reuniao_recomendada
    and colaborador.proxima_reuniao_recomendada <= hoje
]

aniversariantes_30_dias = [
    colaborador for colaborador in colaboradores
    if aniversario_no_periodo(colaborador.data_aniversario, 30)
]

with col1:
    st.metric("🔴 Planos vencidos", len(planos_vencidos))

with col2:
    st.metric("📋 Planos 7 dias", len(planos_7_dias))

with col3:
    st.metric("📝 Revisões 7 dias", len(feedbacks_revisao))

with col4:
    st.metric("🤝 1:1 vencidas", len(colaboradores_1_1_vencida))


st.divider()

st.subheader("🔥 Prioridades do Gestor")

prioridades = []

for plano in planos_vencidos:
    prioridades.append(
        {
            "Tipo": "Plano vencido",
            "Prioridade": "Alta",
            "Colaborador": plano["colaborador_nome"],
            "Descrição": plano["titulo"],
            "Data": formatar_data_br(plano["prazo"])
        }
    )

for colaborador in colaboradores_1_1_vencida:
    prioridades.append(
        {
            "Tipo": "1:1 vencida",
            "Prioridade": "Alta",
            "Colaborador": colaborador.nome,
            "Descrição": "Reunião recomendada pendente",
            "Data": formatar_data_br(colaborador.proxima_reuniao_recomendada)
        }
    )

for feedback in feedbacks_revisao:
    prioridades.append(
        {
            "Tipo": "Revisão de feedback",
            "Prioridade": "Média",
            "Colaborador": feedback["colaborador_nome"],
            "Descrição": feedback["tipo"],
            "Data": formatar_data_br(feedback["data_revisao"])
        }
    )

if prioridades:
    st.dataframe(
        pd.DataFrame(prioridades),
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("Nenhuma prioridade crítica para hoje. Raro, mas acontece.")


st.divider()

aba1, aba2, aba3, aba4 = st.tabs(
    [
        "Planos",
        "1:1",
        "Feedbacks",
        "Aniversários"
    ]
)


with aba1:
    st.subheader("📋 Planos de Ação")

    planos_agenda = [
        plano for plano in planos
        if plano["status"] not in ["Concluído", "Cancelado"]
    ]

    if planos_agenda:
        tabela_planos = []

        for plano in planos_agenda:
            tabela_planos.append(
                {
                    "Prazo": formatar_data_br(plano["prazo"]),
                    "Urgência": classificar_urgencia_prazo(plano["prazo"]),
                    "Colaborador": plano["colaborador_nome"],
                    "Título": plano["titulo"],
                    "Prioridade": plano["prioridade"],
                    "Status": plano["status"]
                }
            )

        st.dataframe(
            pd.DataFrame(tabela_planos),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhum plano de ação pendente.")


with aba2:
    st.subheader("🤝 1:1 Recomendadas")

    tabela_1_1 = []

    for colaborador in colaboradores:
        if colaborador.status != "Ativo":
            continue

        tabela_1_1.append(
            {
                "Colaborador": colaborador.nome,
                "Última 1:1": formatar_data_br(colaborador.data_ultima_reuniao),
                "Próxima recomendada": formatar_data_br(colaborador.proxima_reuniao_recomendada),
                "Frequência": colaborador.frequencia_1_1,
                "Status": (
                    "🔴 Vencida"
                    if colaborador.proxima_reuniao_recomendada
                    and colaborador.proxima_reuniao_recomendada <= hoje
                    else "🟢 Em dia"
                )
            }
        )

    if tabela_1_1:
        st.dataframe(
            pd.DataFrame(tabela_1_1),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhum colaborador ativo encontrado.")


with aba3:
    st.subheader("📝 Feedbacks em Acompanhamento")

    feedbacks_abertos = [
        feedback for feedback in feedbacks
        if feedback["status_acompanhamento"] in ["Aberto", "Em acompanhamento"]
    ]

    if feedbacks_abertos:
        tabela_feedbacks = []

        for feedback in feedbacks_abertos:
            tabela_feedbacks.append(
                {
                    "Revisão": formatar_data_br(feedback["data_revisao"]),
                    "Colaborador": feedback["colaborador_nome"],
                    "Tipo": feedback["tipo"],
                    "Origem": feedback["origem"],
                    "Status": feedback["status_acompanhamento"]
                }
            )

        st.dataframe(
            pd.DataFrame(tabela_feedbacks),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhum feedback em acompanhamento.")


with aba4:
    st.subheader("🎂 Próximos Aniversários")

    aniversariantes = []

    for colaborador in colaboradores:
        if aniversario_no_periodo(colaborador.data_aniversario, 30):
            aniversariantes.append(
                {
                    "Data": formatar_aniversario(colaborador.data_aniversario),
                    "Dias restantes": dias_ate_aniversario(colaborador.data_aniversario),
                    "Colaborador": colaborador.nome,
                    "Cargo": colaborador.cargo,
                    "Unidade": colaborador.unidade
                }
            )

    aniversariantes = sorted(
        aniversariantes,
        key=lambda item: item["Dias restantes"]
    )

    if aniversariantes:
        st.dataframe(
            pd.DataFrame(aniversariantes),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhum aniversário nos próximos 30 dias.")