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
            border-radius: 16px;
            padding: 18px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.18);
        }

        div[data-testid="stMetricValue"] {
            color: white;
            font-weight: 500;
        }

        div[data-testid="stMetricValue"] {
            color: #0F172A;
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

/* ===========================
   Sidebar Premium
============================ */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E3A5F 0%, #243B53 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC;
}

section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
    color: #CBD5E1;
}

section[data-testid="stSidebar"] a {
    border-radius: 12px;
    padding: 8px 10px;
    transition: all .2s ease;
}

section[data-testid="stSidebar"] a:hover {
    background-color: rgba(255,255,255,0.10);
}

section[data-testid="stSidebar"] button {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    background-color: rgba(255,255,255,0.06) !important;
    color: #F8FAFC !important;
}

section[data-testid="stSidebar"] button:hover {
    background-color: rgba(255,255,255,0.14) !important;
}

        </style>
        """,
        unsafe_allow_html=True
    )