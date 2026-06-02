import streamlit as st

from datetime import datetime

from utils.style import aplicar_estilo

from services.dashboard_service import obter_indicadores_dashboard
from services.dashboard_service import obter_alertas_dashboard
from services.dashboard_service import obter_saude_equipe


st.set_page_config(
    page_title="Aurora Team Hub",
    page_icon="🌅",
    layout="wide"
)

aplicar_estilo()


def obter_saudacao():

    hora = datetime.now().hour

    if hora < 12:
        return "Bom dia"

    if hora < 18:
        return "Boa tarde"

    return "Boa noite"


def interpretar_indicador(valor):

    if valor == "-":
        return "Sem dados"

    if valor >= 4.5:
        return "🟢 Excelente"

    if valor >= 3.5:
        return "🟡 Bom"

    if valor >= 2.5:
        return "🟠 Atenção"

    return "🔴 Crítico"


def interpretar_risco(valor):

    if valor == "-":
        return "Sem dados"

    if valor >= 4:
        return "🔴 Elevado"

    if valor >= 3:
        return "🟠 Moderado"

    return "🟢 Controlado"


st.markdown(
    """
    <style>
        div[data-testid="stMetric"] {
            background-color: #111827 !important;
            border: 1px solid #374151 !important;
            padding: 18px;
            border-radius: 14px;
            color: white !important;
        }

        div[data-testid="stMetric"] label {
            color: #cbd5e1 !important;
        }

        div[data-testid="stMetricValue"] {
            color: white !important;
        }

        .aurora-header {
            padding: 18px 0 8px 0;
        }

        .aurora-subtitle {
            color: #cbd5e1;
            font-size: 18px;
            margin-top: -8px;
        }

        .aurora-small {
            color: #94a3b8;
            font-size: 14px;
        }

        .aurora-footer {
            color: #94a3b8;
            font-size: 13px;
            line-height: 1.7;
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown('<div class="aurora-header">', unsafe_allow_html=True)
st.title("🌅 Aurora Team Hub")
st.markdown(
    f"""
    <h2>👋 {obter_saudacao()}, Wilson</h2>
    <p class="aurora-subtitle">
        Centro inteligente de liderança, gestão de equipes e acompanhamento individual.
    </p>
    <p class="aurora-small">
        Seu painel pessoal para acompanhar pessoas, reuniões, feedbacks, planos, radar e inteligência gerencial.
    </p>
    """,
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

st.divider()


indicadores = obter_indicadores_dashboard()
alertas = obter_alertas_dashboard()
saude = obter_saude_equipe()


st.subheader("Resumo Executivo")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Colaboradores Ativos",
        indicadores.get("colaboradores_ativos", 0)
    )

with col2:
    st.metric(
        "🤝 Reuniões 30 dias",
        indicadores.get("reunioes_30_dias", 0)
    )

with col3:
    st.metric(
        "📋 Planos em andamento",
        indicadores.get("planos_andamento", 0)
    )

with col4:
    st.metric(
        "⚠️ Alertas",
        len(alertas)
    )


st.divider()

st.subheader("🔥 O que precisa da sua atenção hoje")

prioridades = []

if indicadores.get("planos_andamento", 0) > 0:
    prioridades.append(
        f"📋 Existem {indicadores.get('planos_andamento', 0)} plano(s) em andamento."
    )

if len(alertas) > 0:
    prioridades.append(
        f"⚠️ Existem {len(alertas)} alerta(s) gerenciais recentes."
    )

if indicadores.get("reunioes_30_dias", 0) == 0:
    prioridades.append(
        "🤝 Nenhuma reunião registrada nos últimos 30 dias."
    )

if not prioridades:
    prioridades.append(
        "✅ Nenhuma pendência crítica identificada."
    )

for prioridade in prioridades:
    st.info(prioridade)


st.divider()

st.subheader("Acesso Rápido")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### 📊 Dashboard Executivo")
        st.write("Indicadores, alertas, saúde da equipe e insights.")
        st.page_link(
            "pages/1_Dashboard.py",
            label="Abrir Dashboard",
            icon="📊"
        )

    with st.container(border=True):
        st.markdown("### 🤝 Reuniões")
        st.write("Registre 1:1, alinhamentos, decisões e follow-ups.")
        st.page_link(
            "pages/3_Reunioes.py",
            label="Abrir Reuniões",
            icon="🤝"
        )

    with st.container(border=True):
        st.markdown("### 📅 Agenda Inteligente")
        st.write("Prioridades, vencimentos, aniversários e revisões.")
        st.page_link(
            "pages/7_Agenda.py",
            label="Abrir Agenda",
            icon="📅"
        )

with col2:
    with st.container(border=True):
        st.markdown("### 👥 Equipe")
        st.write("Cards visuais com risco, planos e acompanhamento.")
        st.page_link(
            "pages/10_Equipe.py",
            label="Abrir Equipe",
            icon="👥"
        )

    with st.container(border=True):
        st.markdown("### 📝 Feedbacks")
        st.write("Acompanhe feedbacks, revisões e planos de melhoria.")
        st.page_link(
            "pages/4_Feedbacks.py",
            label="Abrir Feedbacks",
            icon="📝"
        )

    with st.container(border=True):
        st.markdown("### 📡 Radar")
        st.write("Motivação, performance, engajamento e risco.")
        st.page_link(
            "pages/6_Radar.py",
            label="Abrir Radar",
            icon="📡"
        )

with col3:
    with st.container(border=True):
        st.markdown("### 👤 Colaboradores 360°")
        st.write("Ficha completa, histórico, tendências e PDF 360°.")
        st.page_link(
            "pages/2_Colaboradores.py",
            label="Abrir Colaboradores",
            icon="👤"
        )

    with st.container(border=True):
        st.markdown("### 📋 Planos de Ação")
        st.write("Ações, prazos, status, progresso e acompanhamento.")
        st.page_link(
            "pages/5_Planos_Acao.py",
            label="Abrir Planos",
            icon="📋"
        )

    with st.container(border=True):
        st.markdown("### 🗒️ Notas Rápidas")
        st.write("Registros livres, observações e pontos de atenção.")
        st.page_link(
            "pages/8_Notas.py",
            label="Abrir Notas",
            icon="🗒️"
        )


st.divider()

st.subheader("Saúde Geral da Equipe")

if saude:
    col1, col2, col3, col4, col5 = st.columns(5)

    motivacao = saude.get("motivacao", "-")
    performance = saude.get("performance", "-")
    engajamento = saude.get("engajamento", "-")
    risco = saude.get("risco", "-")
    alinhamento = saude.get("alinhamento", "-")

    with col1:
        st.metric("Motivação", motivacao)
        st.caption(interpretar_indicador(motivacao))

    with col2:
        st.metric("Performance", performance)
        st.caption(interpretar_indicador(performance))

    with col3:
        st.metric("Engajamento", engajamento)
        st.caption(interpretar_indicador(engajamento))

    with col4:
        st.metric("Risco", risco)
        st.caption(interpretar_risco(risco))

    with col5:
        st.metric("Alinhamento", alinhamento)
        st.caption(interpretar_indicador(alinhamento))

else:
    st.info("Ainda não há registros suficientes no Radar.")


st.divider()

st.subheader("Alertas Recentes")

if alertas:
    for alerta in alertas[:5]:
        st.warning(alerta)
else:
    st.success("Nenhum alerta crítico no momento.")


st.divider()

st.markdown(
    f"""
    <div class="aurora-footer">
        <strong>Aurora Team Hub v1.0</strong><br>
        Desenvolvido por Wilson Santos Jesus<br>
        Coordenador de TI • Business Intelligence<br>
        Última atualização: {datetime.now().strftime('%d/%m/%Y')}
    </div>
    """,
    unsafe_allow_html=True
)