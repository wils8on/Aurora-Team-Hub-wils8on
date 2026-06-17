import streamlit as st

from utils.auth import exigir_login
from utils.auth import mostrar_usuario_sidebar
from utils.style import aplicar_estilo

aplicar_estilo()
exigir_login()
mostrar_usuario_sidebar()

import pandas as pd

from datetime import date
from datetime import timedelta

from services.dashboard_service import obter_dados_base
from utils.datas import formatar_data_br


st.markdown(
    """
<div style="background:linear-gradient(135deg,#1D4ED8,#2563EB,#38BDF8); padding:26px; border-radius:20px; margin-bottom:26px;">
    <h1 style="color:white;margin-bottom:8px;">📅 Agenda Inteligente</h1>
    <p style="color:#E0F2FE;font-size:16px;margin-bottom:0;">
        Prioridades, vencimentos, aniversários, revisões e acompanhamentos importantes do gestor.
    </p>
</div>
""",
    unsafe_allow_html=True
)


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


st.subheader("📊 Resumo Executivo")

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

def exibir_card_prioridade(item):

    cor = "#1E4E7A"

    if item["Prioridade"] == "Alta":
        cor = "#DC2626"

    elif item["Prioridade"] == "Média":
        cor = "#D97706"

    st.markdown(
        f"""
<div style="
background:#0F172A;
border-left:6px solid {cor};
padding:18px;
border-radius:12px;
margin-bottom:12px;
">
<h4 style="margin:0;color:white;">
{item["Tipo"]}
</h4>

<p style="margin-top:8px;color:#CBD5E1;">
<strong style="color:white;">Colaborador:</strong> {item["Colaborador"]}<br>
<strong style="color:white;">Descrição:</strong> {item["Descrição"]}<br>
<strong style="color:white;">Data:</strong> {item["Data"]}
</p>
</div>
""",
        unsafe_allow_html=True
    )

if prioridades:

    for i in range(0, len(prioridades), 2):

        col1, col2 = st.columns(2)

        with col1:
            exibir_card_prioridade(
                prioridades[i]
            )

        if i + 1 < len(prioridades):

            with col2:
                exibir_card_prioridade(
                    prioridades[i + 1]
                )

else:

    st.success(
        "Nenhuma prioridade crítica para hoje."
    )

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
        plano
        for plano in planos
        if plano["status"] not in ["Concluído", "Cancelado"]
    ]

    if planos_agenda:

        for i in range(0, len(planos_agenda), 2):

            col1, col2 = st.columns(2)

            with col1:

                plano = planos_agenda[i]

                urgencia = classificar_urgencia_prazo(
                    plano["prazo"]
                )

                cor = "#1E4E7A"

                if "Vencido" in urgencia:
                    cor = "#DC2626"

                elif "hoje" in urgencia:
                    cor = "#D97706"

                elif "3 dias" in urgencia:
                    cor = "#CA8A04"

                st.markdown(
                    f"""
<div style="
background:#0F172A;
border-left:6px solid {cor};
padding:18px;
border-radius:12px;
margin-bottom:12px;
">

<h4 style="margin:0;color:white;">
{plano["titulo"]}
</h4>

<p style="margin-top:8px;color:#CBD5E1;">
<strong style="color:white;">Colaborador:</strong> {plano["colaborador_nome"]}<br>
<strong style="color:white;">Prazo:</strong> {formatar_data_br(plano["prazo"])}<br>
<strong style="color:white;">Urgência:</strong> {urgencia}<br>
<strong style="color:white;">Prioridade:</strong> {plano["prioridade"]}<br>
<strong style="color:white;">Status:</strong> {plano["status"]}
</p>

</div>
""",
                    unsafe_allow_html=True
                )

            if i + 1 < len(planos_agenda):

                with col2:

                    plano = planos_agenda[i + 1]

                    urgencia = classificar_urgencia_prazo(
                        plano["prazo"]
                    )

                    cor = "#1E4E7A"

                    if "Vencido" in urgencia:
                        cor = "#DC2626"

                    elif "hoje" in urgencia:
                        cor = "#D97706"

                    elif "3 dias" in urgencia:
                        cor = "#CA8A04"

                    st.markdown(
                        f"""
<div style="
background:#0F172A;
border-left:6px solid {cor};
padding:18px;
border-radius:12px;
margin-bottom:12px;
">

<h4 style="margin:0;color:white;">
{plano["titulo"]}
</h4>

<p style="margin-top:8px;color:#CBD5E1;">
<strong style="color:white;">Colaborador:</strong> {plano["colaborador_nome"]}<br>
<strong style="color:white;">Prazo:</strong> {formatar_data_br(plano["prazo"])}<br>
<strong style="color:white;">Urgência:</strong> {urgencia}<br>
<strong style="color:white;">Prioridade:</strong> {plano["prioridade"]}<br>
<strong style="color:white;">Status:</strong> {plano["status"]}
</p>

</div>
""",
                        unsafe_allow_html=True
                    )

    else:

        st.info(
            "Nenhum plano de ação pendente."
        )


with aba2:

    st.subheader("🤝 1:1 Recomendadas")

    tabela_1_1 = []

    for colaborador in colaboradores:

        if colaborador.status != "Ativo":
            continue

        status_1_1 = (
            "🔴 Vencida"
            if colaborador.proxima_reuniao_recomendada
            and colaborador.proxima_reuniao_recomendada <= hoje
            else "🟢 Em dia"
        )

        tabela_1_1.append(
            {
                "Colaborador": colaborador.nome,
                "Última 1:1": formatar_data_br(colaborador.data_ultima_reuniao),
                "Próxima recomendada": formatar_data_br(colaborador.proxima_reuniao_recomendada),
                "Frequência": colaborador.frequencia_1_1,
                "Status": status_1_1
            }
        )

    if tabela_1_1:

        for i in range(0, len(tabela_1_1), 2):

            col1, col2 = st.columns(2)

            with col1:

                item = tabela_1_1[i]

                cor = "#1E4E7A"

                if "Vencida" in item["Status"]:
                    cor = "#DC2626"

                st.markdown(
                    f"""
<div style="background:#0F172A; border-left:6px solid {cor}; padding:18px; border-radius:12px; margin-bottom:12px;">
    <h4 style="margin:0;color:white;">{item["Colaborador"]}</h4>
    <p style="margin-top:8px;color:#CBD5E1;">
        <strong style="color:white;">Última 1:1:</strong> {item["Última 1:1"]}<br>
        <strong style="color:white;">Próxima recomendada:</strong> {item["Próxima recomendada"]}<br>
        <strong style="color:white;">Frequência:</strong> {item["Frequência"]}<br>
        <strong style="color:white;">Status:</strong> {item["Status"]}
    </p>
</div>
""",
                    unsafe_allow_html=True
                )

            if i + 1 < len(tabela_1_1):

                with col2:

                    item = tabela_1_1[i + 1]

                    cor = "#1E4E7A"

                    if "Vencida" in item["Status"]:
                        cor = "#DC2626"

                    st.markdown(
                        f"""
<div style="background:#0F172A; border-left:6px solid {cor}; padding:18px; border-radius:12px; margin-bottom:12px;">
    <h4 style="margin:0;color:white;">{item["Colaborador"]}</h4>
    <p style="margin-top:8px;color:#CBD5E1;">
        <strong style="color:white;">Última 1:1:</strong> {item["Última 1:1"]}<br>
        <strong style="color:white;">Próxima recomendada:</strong> {item["Próxima recomendada"]}<br>
        <strong style="color:white;">Frequência:</strong> {item["Frequência"]}<br>
        <strong style="color:white;">Status:</strong> {item["Status"]}
    </p>
</div>
""",
                        unsafe_allow_html=True
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

        for i in range(0, len(feedbacks_abertos), 2):

            col1, col2 = st.columns(2)

            with col1:

                feedback = feedbacks_abertos[i]

                cor = "#1E4E7A"

                if feedback["data_revisao"] and feedback["data_revisao"] <= hoje:
                    cor = "#DC2626"
                elif feedback["data_revisao"] and feedback["data_revisao"] <= limite_7_dias:
                    cor = "#D97706"

                st.markdown(
                    f"""
<div style="background:#0F172A; border-left:6px solid {cor}; padding:18px; border-radius:12px; margin-bottom:12px;">
    <h4 style="margin:0;color:white;">{feedback["tipo"]}</h4>
    <p style="margin-top:8px;color:#CBD5E1;">
        <strong style="color:white;">Colaborador:</strong> {feedback["colaborador_nome"]}<br>
        <strong style="color:white;">Origem:</strong> {feedback["origem"]}<br>
        <strong style="color:white;">Revisão:</strong> {formatar_data_br(feedback["data_revisao"])}<br>
        <strong style="color:white;">Status:</strong> {feedback["status_acompanhamento"]}
    </p>
</div>
""",
                    unsafe_allow_html=True
                )

            if i + 1 < len(feedbacks_abertos):

                with col2:

                    feedback = feedbacks_abertos[i + 1]

                    cor = "#1E4E7A"

                    if feedback["data_revisao"] and feedback["data_revisao"] <= hoje:
                        cor = "#DC2626"
                    elif feedback["data_revisao"] and feedback["data_revisao"] <= limite_7_dias:
                        cor = "#D97706"

                    st.markdown(
                        f"""
<div style="background:#0F172A; border-left:6px solid {cor}; padding:18px; border-radius:12px; margin-bottom:12px;">
    <h4 style="margin:0;color:white;">{feedback["tipo"]}</h4>
    <p style="margin-top:8px;color:#CBD5E1;">
        <strong style="color:white;">Colaborador:</strong> {feedback["colaborador_nome"]}<br>
        <strong style="color:white;">Origem:</strong> {feedback["origem"]}<br>
        <strong style="color:white;">Revisão:</strong> {formatar_data_br(feedback["data_revisao"])}<br>
        <strong style="color:white;">Status:</strong> {feedback["status_acompanhamento"]}
    </p>
</div>
""",
                        unsafe_allow_html=True
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

        for i in range(0, len(aniversariantes), 2):

            col1, col2 = st.columns(2)

            with col1:
                item = aniversariantes[i]

                st.markdown(
                    f"""
<div style="background:#0F172A; border-left:6px solid #D97706; padding:18px; border-radius:12px; margin-bottom:12px;">
    <h4 style="margin:0;color:white;">🎂 {item["Colaborador"]}</h4>
    <p style="margin-top:8px;color:#CBD5E1;">
        <strong style="color:white;">Data:</strong> {item["Data"]}<br>
        <strong style="color:white;">Dias restantes:</strong> {item["Dias restantes"]}<br>
        <strong style="color:white;">Cargo:</strong> {item["Cargo"] or "-"}<br>
        <strong style="color:white;">Unidade:</strong> {item["Unidade"] or "-"}
    </p>
</div>
""",
                    unsafe_allow_html=True
                )

            if i + 1 < len(aniversariantes):

                with col2:
                    item = aniversariantes[i + 1]

                    st.markdown(
                        f"""
<div style="background:#0F172A; border-left:6px solid #D97706; padding:18px; border-radius:12px; margin-bottom:12px;">
    <h4 style="margin:0;color:white;">🎂 {item["Colaborador"]}</h4>
    <p style="margin-top:8px;color:#CBD5E1;">
        <strong style="color:white;">Data:</strong> {item["Data"]}<br>
        <strong style="color:white;">Dias restantes:</strong> {item["Dias restantes"]}<br>
        <strong style="color:white;">Cargo:</strong> {item["Cargo"] or "-"}<br>
        <strong style="color:white;">Unidade:</strong> {item["Unidade"] or "-"}
    </p>
</div>
""",
                        unsafe_allow_html=True
                    )

    else:

        st.info("Nenhum aniversário nos próximos 30 dias.")