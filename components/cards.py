import streamlit as st


def card_indicador(
    titulo,
    valor,
    ajuda=None
):
    st.metric(
        label=titulo,
        value=valor,
        help=ajuda
    )