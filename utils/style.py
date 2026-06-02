import streamlit as st


def aplicar_estilo():

    st.markdown(
        """
        <style>

        /* ===========================
           Layout Geral
        ============================ */

        .main {
            padding-top: 1rem;
        }

        .block-container {
            padding-top: 1rem;
            max-width: 95%;
        }

        /* ===========================
           Cards de KPI
        ============================ */

        div[data-testid="stMetric"] {
            background-color: #111827;
            border: 1px solid #374151;
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }

        div[data-testid="stMetricLabel"] {
            color: #cbd5e1;
            font-weight: 500;
        }

        div[data-testid="stMetricValue"] {
            color: white;
            font-weight: 700;
        }

        /* ===========================
           Containers
        ============================ */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 14px;
        }

        /* ===========================
           Títulos
        ============================ */

        h1 {
            font-weight: 700;
        }

        h2 {
            font-weight: 600;
        }

        h3 {
            font-weight: 600;
        }

        /* ===========================
           Dataframes
        ============================ */

        .stDataFrame {
            border-radius: 14px;
            overflow: hidden;
        }

        /* ===========================
           Tabs
        ============================ */

        button[data-baseweb="tab"] {
            border-radius: 10px;
            font-weight: 600;
        }

        /* ===========================
           Alertas
        ============================ */

        div[data-testid="stAlert"] {
            border-radius: 12px;
        }

        /* ===========================
           Botões
        ============================ */

        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
        }

        /* ===========================
           Cards Aurora
        ============================ */

        .aurora-card {
            background-color: #111827;
            border: 1px solid #374151;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 12px;
        }

        .aurora-card-title {
            font-size: 18px;
            font-weight: 700;
            color: white;
        }

        .aurora-card-value {
            font-size: 32px;
            font-weight: 700;
            color: white;
        }

        .aurora-card-subtitle {
            color: #cbd5e1;
            font-size: 14px;
        }

        /* ===========================
           Seções
        ============================ */

        .aurora-section {
            padding-top: 8px;
            padding-bottom: 8px;
        }

        .aurora-section-title {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        /* ===========================
           Scrollbars
        ============================ */

        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        ::-webkit-scrollbar-thumb {
            border-radius: 20px;
            background: #4b5563;
        }

        </style>
        """,
        unsafe_allow_html=True
    )