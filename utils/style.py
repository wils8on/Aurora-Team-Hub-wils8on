import streamlit as st


def aplicar_estilo():

    st.markdown(
        """
        <style>

        .main {
            padding-top: 1rem;
        }

        .stMetric {
            border-radius: 12px;
            padding: 12px;
            background-color: #f8f9fa;
        }

        div[data-testid="stMetric"] {
            border: 1px solid #e6e6e6;
            padding: 15px;
            border-radius: 12px;
        }

        .block-container {
            padding-top: 1rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )