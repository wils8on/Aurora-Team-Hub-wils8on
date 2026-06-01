import streamlit as st
import pandas as pd

from datetime import date

from services.colaboradores_service import listar_colaboradores
from services.feedbacks_service import criar_feedback
from services.feedbacks_service import listar_feedbacks
from services.feedbacks_service import editar_feedback
from services.feedbacks_service import excluir_feedback

from utils.datas import formatar_data_br


DATA_MINIMA = date(1950, 1, 1)
DATA_MAXIMA = date(2150, 12, 31)


def obter_indice(lista, valor, padrao=0):

    if valor in lista:
        return lista.index(valor)

    return padrao


st.title("📝 Feedbacks")

st.info("Registre, acompanhe e revise feedbacks da equipe.")


colaboradores = listar_colaboradores()

if not colaboradores:
    st.warning("Cadastre pelo menos um colaborador antes de registrar feedbacks.")
    st.stop()


with st.expander("➕ Novo Feedback", expanded=False):

    with st.form("form_novo_feedback"):

        aba1, aba2, aba3 = st.tabs(
            [
                "Dados do Feedback",
                "Análise",
                "Acompanhamento"
            ]
        )

        with aba1:
            col1, col2 = st.columns(2)

            with col1:
                colaborador = st.selectbox(
                    "Colaborador",
                    colaboradores,
                    format_func=lambda item: item.nome
                )

                data_feedback = st.date_input(
                    "Data do feedback",
                    value=date.today(),
                    min_value=DATA_MINIMA,
                    max_value=DATA_MAXIMA,
                    format="DD/MM/YYYY"
                )

                origem = st.selectbox(
                    "Origem",
                    [
                        "Reunião",
                        "Observação",
                        "Entrega",
                        "Alinhamento",
                        "Situação específica"
                    ]
                )

            with col2:
                tipo = st.selectbox(
                    "Tipo de feedback",
                    [
                        "Positivo",
                        "Desenvolvimento",
                        "Correção de rota",
                        "Reconhecimento",
                        "Alinhamento"
                    ]
                )

                status_acompanhamento = st.selectbox(
                    "Status do acompanhamento",
                    [
                        "Aberto",
                        "Em acompanhamento",
                        "Revisado",
                        "Concluído",
                        "Cancelado"
                    ]
                )

                data_revisao = st.date_input(
                    "Data de revisão",
                    value=date.today(),
                    min_value=DATA_MINIMA,
                    max_value=DATA_MAXIMA,
                    format="DD/MM/YYYY"
                )

            contexto = st.text_area(
                "Contexto",
                height=120
            )

            comportamento_observado = st.text_area(
                "Comportamento observado",
                height=120
            )

        with aba2:
            impacto_percebido = st.text_area(
                "Impacto percebido",
                height=120
            )

            leitura_gestor = st.text_area(
                "Leitura do gestor",
                height=120
            )

            orientacao_dada = st.text_area(
                "Orientação dada",
                height=120
            )

            reacao_colaborador = st.text_area(
                "Reação do colaborador",
                height=120
            )

        with aba3:
            plano_melhoria = st.text_area(
                "Plano de melhoria / acompanhamento",
                height=160
            )

        salvar = st.form_submit_button("Salvar Feedback")

        if salvar:

            if not contexto:
                st.error("Informe ao menos o contexto do feedback.")
            else:
                dados = {
                    "colaborador_id": colaborador.id,
                    "data": data_feedback,
                    "origem": origem,
                    "tipo": tipo,
                    "contexto": contexto,
                    "comportamento_observado": comportamento_observado,
                    "impacto_percebido": impacto_percebido,
                    "leitura_gestor": leitura_gestor,
                    "orientacao_dada": orientacao_dada,
                    "reacao_colaborador": reacao_colaborador,
                    "plano_melhoria": plano_melhoria,
                    "data_revisao": data_revisao,
                    "status_acompanhamento": status_acompanhamento
                }

                criar_feedback(dados)

                st.success("Feedback cadastrado com sucesso.")
                st.rerun()


st.divider()

st.subheader("Histórico de Feedbacks")

feedbacks = listar_feedbacks()

if feedbacks:

    dados_tabela = []

    for feedback in feedbacks:
        dados_tabela.append(
            {
                "ID": feedback["id"],
                "Data": formatar_data_br(feedback["data"]),
                "Colaborador": feedback["colaborador_nome"],
                "Origem": feedback["origem"],
                "Tipo": feedback["tipo"],
                "Status": feedback["status_acompanhamento"],
                "Revisão": formatar_data_br(feedback["data_revisao"])
            }
        )

    df = pd.DataFrame(dados_tabela)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Ficha do Feedback")

    feedback_selecionado = st.selectbox(
        "Selecione um feedback",
        feedbacks,
        format_func=lambda item: f"{formatar_data_br(item['data'])} | {item['colaborador_nome']} | {item['tipo']}"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Colaborador", feedback_selecionado["colaborador_nome"] or "-")

    with col2:
        st.metric("Tipo", feedback_selecionado["tipo"] or "-")

    with col3:
        st.metric("Origem", feedback_selecionado["origem"] or "-")

    with col4:
        st.metric("Status", feedback_selecionado["status_acompanhamento"] or "-")

    ficha1, ficha2, ficha3, ficha4 = st.tabs(
        [
            "Resumo",
            "Análise",
            "Acompanhamento",
            "Editar"
        ]
    )

    with ficha1:
        st.write("**Data:**", formatar_data_br(feedback_selecionado["data"]))
        st.write("**Data de revisão:**", formatar_data_br(feedback_selecionado["data_revisao"]))

        st.write("**Contexto:**")
        st.write(feedback_selecionado["contexto"] or "-")

        st.write("**Comportamento observado:**")
        st.write(feedback_selecionado["comportamento_observado"] or "-")

    with ficha2:
        st.write("**Impacto percebido:**")
        st.write(feedback_selecionado["impacto_percebido"] or "-")

        st.write("**Leitura do gestor:**")
        st.write(feedback_selecionado["leitura_gestor"] or "-")

        st.write("**Orientação dada:**")
        st.write(feedback_selecionado["orientacao_dada"] or "-")

        st.write("**Reação do colaborador:**")
        st.write(feedback_selecionado["reacao_colaborador"] or "-")

    with ficha3:
        st.write("**Plano de melhoria / acompanhamento:**")
        st.write(feedback_selecionado["plano_melhoria"] or "-")

        st.write("**Status do acompanhamento:**", feedback_selecionado["status_acompanhamento"] or "-")

    with ficha4:
        st.subheader("✏️ Editar Feedback")

        with st.form("form_editar_feedback"):

            aba_ed1, aba_ed2, aba_ed3 = st.tabs(
                [
                    "Dados do Feedback",
                    "Análise",
                    "Acompanhamento"
                ]
            )

            with aba_ed1:
                col1, col2 = st.columns(2)

                with col1:
                    indice_colaborador = 0

                    for indice, colaborador_item in enumerate(colaboradores):
                        if colaborador_item.id == feedback_selecionado["colaborador_id"]:
                            indice_colaborador = indice

                    colaborador_editado = st.selectbox(
                        "Colaborador",
                        colaboradores,
                        index=indice_colaborador,
                        format_func=lambda item: item.nome
                    )

                    data_feedback_editada = st.date_input(
                        "Data do feedback",
                        value=feedback_selecionado["data"] or date.today(),
                        min_value=DATA_MINIMA,
                        max_value=DATA_MAXIMA,
                        format="DD/MM/YYYY"
                    )

                    origens = [
                        "Reunião",
                        "Observação",
                        "Entrega",
                        "Alinhamento",
                        "Situação específica"
                    ]

                    origem_editada = st.selectbox(
                        "Origem",
                        origens,
                        index=obter_indice(origens, feedback_selecionado["origem"])
                    )

                with col2:
                    tipos = [
                        "Positivo",
                        "Desenvolvimento",
                        "Correção de rota",
                        "Reconhecimento",
                        "Alinhamento"
                    ]

                    tipo_editado = st.selectbox(
                        "Tipo de feedback",
                        tipos,
                        index=obter_indice(tipos, feedback_selecionado["tipo"])
                    )

                    status_opcoes = [
                        "Aberto",
                        "Em acompanhamento",
                        "Revisado",
                        "Concluído",
                        "Cancelado"
                    ]

                    status_acompanhamento_editado = st.selectbox(
                        "Status do acompanhamento",
                        status_opcoes,
                        index=obter_indice(
                            status_opcoes,
                            feedback_selecionado["status_acompanhamento"]
                        )
                    )

                    data_revisao_editada = st.date_input(
                        "Data de revisão",
                        value=feedback_selecionado["data_revisao"] or date.today(),
                        min_value=DATA_MINIMA,
                        max_value=DATA_MAXIMA,
                        format="DD/MM/YYYY"
                    )

                contexto_editado = st.text_area(
                    "Contexto",
                    value=feedback_selecionado["contexto"] or "",
                    height=120
                )

                comportamento_observado_editado = st.text_area(
                    "Comportamento observado",
                    value=feedback_selecionado["comportamento_observado"] or "",
                    height=120
                )

            with aba_ed2:
                impacto_percebido_editado = st.text_area(
                    "Impacto percebido",
                    value=feedback_selecionado["impacto_percebido"] or "",
                    height=120
                )

                leitura_gestor_editada = st.text_area(
                    "Leitura do gestor",
                    value=feedback_selecionado["leitura_gestor"] or "",
                    height=120
                )

                orientacao_dada_editada = st.text_area(
                    "Orientação dada",
                    value=feedback_selecionado["orientacao_dada"] or "",
                    height=120
                )

                reacao_colaborador_editada = st.text_area(
                    "Reação do colaborador",
                    value=feedback_selecionado["reacao_colaborador"] or "",
                    height=120
                )

            with aba_ed3:
                plano_melhoria_editado = st.text_area(
                    "Plano de melhoria / acompanhamento",
                    value=feedback_selecionado["plano_melhoria"] or "",
                    height=160
                )

            salvar_edicao = st.form_submit_button("Salvar Alterações")

            if salvar_edicao:

                if not contexto_editado:
                    st.error("Informe ao menos o contexto do feedback.")
                else:
                    dados_editados = {
                        "colaborador_id": colaborador_editado.id,
                        "data": data_feedback_editada,
                        "origem": origem_editada,
                        "tipo": tipo_editado,
                        "contexto": contexto_editado,
                        "comportamento_observado": comportamento_observado_editado,
                        "impacto_percebido": impacto_percebido_editado,
                        "leitura_gestor": leitura_gestor_editada,
                        "orientacao_dada": orientacao_dada_editada,
                        "reacao_colaborador": reacao_colaborador_editada,
                        "plano_melhoria": plano_melhoria_editado,
                        "data_revisao": data_revisao_editada,
                        "status_acompanhamento": status_acompanhamento_editado
                    }

                    editar_feedback(
                        feedback_selecionado["id"],
                        dados_editados
                    )

                    st.success("Feedback atualizado com sucesso.")
                    st.rerun()

    st.divider()

    st.subheader("Excluir Feedback")

    feedback_para_excluir = st.selectbox(
        "Selecione o feedback para excluir",
        feedbacks,
        format_func=lambda item: f"{formatar_data_br(item['data'])} | {item['colaborador_nome']} | {item['tipo']}",
        key="excluir_feedback"
    )

    if st.button("Excluir Feedback", type="secondary"):

        excluir_feedback(feedback_para_excluir["id"])

        st.success("Feedback excluído com sucesso.")
        st.rerun()

else:
    st.warning("Nenhum feedback cadastrado ainda.")