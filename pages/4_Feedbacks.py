import streamlit as st

from utils.auth import exigir_login
from utils.auth import mostrar_usuario_sidebar
from utils.style import aplicar_estilo

aplicar_estilo()
exigir_login()
mostrar_usuario_sidebar()

import pandas as pd

from datetime import date

from services.colaboradores_service import listar_colaboradores
from services.feedbacks_service import criar_feedback
from services.feedbacks_service import listar_feedbacks
from services.feedbacks_service import editar_feedback
from services.feedbacks_service import excluir_feedback

from utils.datas import formatar_data_br
from services.relatorios_service import gerar_pdf_feedback


DATA_MINIMA = date(1950, 1, 1)
DATA_MAXIMA = date(2150, 12, 31)


def obter_indice(lista, valor, padrao=0):

    if valor in lista:
        return lista.index(valor)

    return padrao


st.markdown(
    """
<div style="background:linear-gradient(135deg,#1D4ED8,#2563EB,#38BDF8); padding:26px; border-radius:20px; margin-bottom:26px;">
    <h1 style="color:white;margin-bottom:8px;">📝 Gestão de Feedbacks</h1>
    <p style="color:#E0F2FE;font-size:16px;margin-bottom:0;">
        Registre, acompanhe e revise feedbacks, reconhecimentos e pontos de desenvolvimento da equipe.
    </p>
</div>
""",
    unsafe_allow_html=True
)


colaboradores = listar_colaboradores()

if not colaboradores:
    st.warning("Cadastre pelo menos um colaborador antes de registrar feedbacks.")
    st.stop()

st.divider()

st.subheader("Histórico de Feedbacks")

feedbacks = listar_feedbacks()

total_feedbacks = len(feedbacks)

total_reconhecimentos = len(
    [
        f for f in feedbacks
        if f["tipo"] == "Reconhecimento"
    ]
)

total_desenvolvimento = len(
    [
        f for f in feedbacks
        if f["tipo"] == "Desenvolvimento"
    ]
)

total_abertos = len(
    [
        f for f in feedbacks
        if f["status_acompanhamento"] in [
            "Aberto",
            "Em acompanhamento"
        ]
    ]
)

col_k1, col_k2, col_k3, col_k4 = st.columns(4)

with col_k1:
    st.metric(
        "Feedbacks",
        total_feedbacks
    )

with col_k2:
    st.metric(
        "Reconhecimentos",
        total_reconhecimentos
    )

with col_k3:
    st.metric(
        "Desenvolvimento",
        total_desenvolvimento
    )

with col_k4:
    st.metric(
        "Pendentes",
        total_abertos
    )

st.divider()

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

    st.markdown(
        f"""
<div style="background:#132F4C; border:1px solid #1E4E7A; border-radius:18px; padding:24px; margin-bottom:18px;">
    <h2 style="color:white;margin-bottom:8px;">📝 {feedback_selecionado["tipo"] or "Feedback"}</h2>
    <p style="color:white;font-size:24px;font-weight:600;margin-bottom:8px;">{feedback_selecionado["colaborador_nome"] or "-"}</p>
    <p style="color:#CBD5E1;margin-bottom:16px;">{formatar_data_br(feedback_selecionado["data"])}</p>
    <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:12px;">
        <div><span style="color:#CBD5E1;">📋 Tipo</span><br><strong style="color:white;">{feedback_selecionado["tipo"] or "-"}</strong></div>
        <div><span style="color:#CBD5E1;">📍 Origem</span><br><strong style="color:white;">{feedback_selecionado["origem"] or "-"}</strong></div>
        <div><span style="color:#CBD5E1;">📅 Revisão</span><br><strong style="color:white;">{formatar_data_br(feedback_selecionado["data_revisao"])}</strong></div>
        <div><span style="color:#CBD5E1;">🔄 Status</span><br><strong style="color:white;">{feedback_selecionado["status_acompanhamento"] or "-"}</strong></div>
    </div>
</div>
""",
        unsafe_allow_html=True
    )

    pdf_feedback = gerar_pdf_feedback(feedback_selecionado)

    nome_arquivo_feedback = (
        f"relatorio_feedback_"
        f"{feedback_selecionado['colaborador_nome'].replace(' ', '_').lower()}_"
        f"{feedback_selecionado['data']}.pdf"
    )

    st.markdown(
        """
<div style="background:#111827; border:1px solid #374151; border-radius:16px; padding:18px; margin-bottom:12px;">
    <h4 style="margin:0;color:white;">📄 Relatório do Feedback</h4>
    <p style="margin-top:8px;color:#CBD5E1;font-size:14px;">
        Gere uma versão em PDF com os principais dados deste feedback.
    </p>
</div>
""",
        unsafe_allow_html=True
    )

    st.download_button(
        label="📥 Baixar Feedback PDF",
        data=pdf_feedback,
        file_name=nome_arquivo_feedback,
        mime="application/pdf",
        use_container_width=True
    )

    ficha1, ficha2, ficha3, ficha4 = st.tabs(
        [
            "Resumo",
            "Análise",
            "Acompanhamento",
            "Editar"
        ]
    )

    with ficha1:
        st.markdown(
            f"""
<div style="background:#0F2138; border:1px solid #1E4E7A; border-radius:16px; padding:18px; margin-bottom:14px;">
    <h3 style="color:white;">📌 Dados do Feedback</h3>
    <p style="color:#CBD5E1;"><strong style="color:white;">Data:</strong> {formatar_data_br(feedback_selecionado["data"])}</p>
    <p style="color:#CBD5E1;"><strong style="color:white;">Revisão:</strong> {formatar_data_br(feedback_selecionado["data_revisao"])}</p>
</div>

<div style="background:#0F2138; border:1px solid #1E4E7A; border-radius:16px; padding:18px; margin-bottom:14px;">
    <h3 style="color:white;">📖 Contexto</h3>
    <p style="color:#CBD5E1;">{feedback_selecionado["contexto"] or "-"}</p>
</div>

<div style="background:#0F2138; border:1px solid #1E4E7A; border-radius:16px; padding:18px; margin-bottom:14px;">
    <h3 style="color:white;">👀 Comportamento Observado</h3>
    <p style="color:#CBD5E1;">{feedback_selecionado["comportamento_observado"] or "-"}</p>
</div>
""",
            unsafe_allow_html=True
        )

    with ficha2:
        st.markdown(
            f"""
<div style="background:#0F2138; border:1px solid #1E4E7A; border-radius:16px; padding:18px; margin-bottom:14px;">
    <h3 style="color:white;">📈 Impacto Percebido</h3>
    <p style="color:#CBD5E1;">{feedback_selecionado["impacto_percebido"] or "-"}</p>
</div>

<div style="background:#0F2138; border:1px solid #1E4E7A; border-radius:16px; padding:18px; margin-bottom:14px;">
    <h3 style="color:white;">🧠 Leitura do Gestor</h3>
    <p style="color:#CBD5E1;">{feedback_selecionado["leitura_gestor"] or "-"}</p>
</div>

<div style="background:#0F2138; border:1px solid #1E4E7A; border-radius:16px; padding:18px; margin-bottom:14px;">
    <h3 style="color:white;">🎯 Orientação Dada</h3>
    <p style="color:#CBD5E1;">{feedback_selecionado["orientacao_dada"] or "-"}</p>
</div>

<div style="background:#0F2138; border:1px solid #1E4E7A; border-radius:16px; padding:18px; margin-bottom:14px;">
    <h3 style="color:white;">💬 Reação do Colaborador</h3>
    <p style="color:#CBD5E1;">{feedback_selecionado["reacao_colaborador"] or "-"}</p>
</div>
""",
            unsafe_allow_html=True
        )

    with ficha3:
        st.markdown(
            f"""
<div style="background:#0F2138; border:1px solid #1E4E7A; border-radius:16px; padding:18px; margin-bottom:14px;">
    <h3 style="color:white;">🚀 Plano de Desenvolvimento</h3>
    <p style="color:#CBD5E1;">{feedback_selecionado["plano_melhoria"] or "-"}</p>
</div>

<div style="background:#0F2138; border:1px solid #1E4E7A; border-radius:16px; padding:18px; margin-bottom:14px;">
    <h3 style="color:white;">🔄 Status do Acompanhamento</h3>
    <p style="color:#CBD5E1;">{feedback_selecionado["status_acompanhamento"] or "-"}</p>
</div>
""",
            unsafe_allow_html=True
        )

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