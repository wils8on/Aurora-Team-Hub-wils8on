import streamlit as st
import pandas as pd

from datetime import date

from services.colaboradores_service import listar_colaboradores
from services.radar_service import criar_radar
from services.radar_service import listar_radares
from services.radar_service import excluir_radar

from utils.datas import formatar_data_br


DATA_MINIMA = date(1950, 1, 1)
DATA_MAXIMA = date(2150, 12, 31)


st.title("📡 Radar do Colaborador")

st.info("Registre percepções gerenciais sobre motivação, performance, carga, engajamento e risco.")


colaboradores = listar_colaboradores()

if not colaboradores:
    st.warning("Cadastre pelo menos um colaborador antes de registrar o radar.")
    st.stop()


with st.expander("➕ Novo Registro de Radar", expanded=False):

    with st.form("form_novo_radar"):

        col1, col2 = st.columns(2)

        with col1:
            colaborador = st.selectbox(
                "Colaborador",
                colaboradores,
                format_func=lambda item: item.nome
            )

            data_registro = st.date_input(
                "Data do registro",
                value=date.today(),
                min_value=DATA_MINIMA,
                max_value=DATA_MAXIMA,
                format="DD/MM/YYYY"
            )

            motivacao = st.slider("Motivação", 1, 5, 3)
            performance = st.slider("Performance percebida", 1, 5, 3)
            carga_trabalho = st.slider("Carga de trabalho", 1, 5, 3)

        with col2:
            engajamento = st.slider("Engajamento", 1, 5, 3)
            risco_desgaste = st.slider("Risco de desgaste / burnout", 1, 5, 3)
            alinhamento_equipe = st.slider("Alinhamento com a equipe", 1, 5, 3)

            observacoes = st.text_area(
                "Observações",
                height=180
            )

        salvar = st.form_submit_button("Salvar Registro de Radar")

        if salvar:

            dados = {
                "colaborador_id": colaborador.id,
                "data_registro": data_registro,
                "motivacao": motivacao,
                "performance": performance,
                "carga_trabalho": carga_trabalho,
                "engajamento": engajamento,
                "risco_desgaste": risco_desgaste,
                "alinhamento_equipe": alinhamento_equipe,
                "observacoes": observacoes
            }

            criar_radar(dados)

            st.success("Registro de radar cadastrado com sucesso.")
            st.rerun()


st.divider()

st.subheader("Histórico do Radar")

radares = listar_radares()

if radares:

    dados_tabela = []

    for radar in radares:
        dados_tabela.append(
            {
                "ID": radar["id"],
                "Data": formatar_data_br(radar["data_registro"]),
                "Colaborador": radar["colaborador_nome"],
                "Motivação": radar["motivacao"],
                "Performance": radar["performance"],
                "Carga": radar["carga_trabalho"],
                "Engajamento": radar["engajamento"],
                "Risco": radar["risco_desgaste"],
                "Alinhamento": radar["alinhamento_equipe"]
            }
        )

    df = pd.DataFrame(dados_tabela)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Resumo Visual")

    df_metricas = pd.DataFrame(dados_tabela)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Motivação média",
            round(df_metricas["Motivação"].mean(), 2)
        )

    with col2:
        st.metric(
            "Performance média",
            round(df_metricas["Performance"].mean(), 2)
        )

    with col3:
        st.metric(
            "Engajamento médio",
            round(df_metricas["Engajamento"].mean(), 2)
        )

    with col4:
        st.metric(
            "Risco médio",
            round(df_metricas["Risco"].mean(), 2)
        )

    st.divider()

    st.subheader("Ficha do Registro")

    radar_selecionado = st.selectbox(
        "Selecione um registro",
        radares,
        format_func=lambda item: f"{formatar_data_br(item['data_registro'])} | {item['colaborador_nome']}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Motivação", radar_selecionado["motivacao"])

    with col2:
        st.metric("Performance", radar_selecionado["performance"])

    with col3:
        st.metric("Risco", radar_selecionado["risco_desgaste"])

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("Carga", radar_selecionado["carga_trabalho"])

    with col5:
        st.metric("Engajamento", radar_selecionado["engajamento"])

    with col6:
        st.metric("Alinhamento", radar_selecionado["alinhamento_equipe"])

    st.write("**Data:**", formatar_data_br(radar_selecionado["data_registro"]))
    st.write("**Colaborador:**", radar_selecionado["colaborador_nome"])

    st.write("**Observações:**")
    st.write(radar_selecionado["observacoes"] or "-")

    st.divider()

    st.subheader("Excluir Registro de Radar")

    radar_para_excluir = st.selectbox(
        "Selecione o registro para excluir",
        radares,
        format_func=lambda item: f"{formatar_data_br(item['data_registro'])} | {item['colaborador_nome']}",
        key="excluir_radar"
    )

    if st.button("Excluir Registro", type="secondary"):

        excluir_radar(radar_para_excluir["id"])

        st.success("Registro de radar excluído com sucesso.")
        st.rerun()

else:
    st.warning("Nenhum registro de radar cadastrado ainda.")