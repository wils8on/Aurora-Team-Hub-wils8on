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
from services.planos_service import criar_plano
from services.planos_service import listar_planos
from services.planos_service import editar_plano
from services.planos_service import excluir_plano
from services.relatorios_service import gerar_pdf_plano

from utils.datas import formatar_data_br


DATA_MINIMA = date(1950, 1, 1)
DATA_MAXIMA = date(2150, 12, 31)


def obter_indice(lista, valor, padrao=0):

    if valor in lista:
        return lista.index(valor)

    return padrao


st.markdown(
    """
<div style="background:linear-gradient(135deg,#1D4ED8,#2563EB,#38BDF8); padding:26px; border-radius:20px; margin-bottom:26px;">
    <h1 style="color:white;margin-bottom:8px;">📋 Planos de Ação</h1>
    <p style="color:#E0F2FE;font-size:16px;margin-bottom:0;">
        Acompanhe ações, prazos, prioridades, evolução e entregas vinculadas aos colaboradores.
    </p>
</div>
""",
    unsafe_allow_html=True
)


colaboradores = listar_colaboradores()

if not colaboradores:
    st.warning("Cadastre pelo menos um colaborador antes de registrar planos de ação.")
    st.stop()


st.divider()

st.subheader("Histórico de Planos de Ação")

planos = listar_planos()

total_planos = len(planos)

pendentes = len(
    [p for p in planos if p["status"] == "Pendente"]
)

em_andamento = len(
    [p for p in planos if p["status"] == "Em andamento"]
)

concluidos = len(
    [p for p in planos if p["status"] == "Concluído"]
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📋 Planos", total_planos)

with col2:
    st.metric("⏳ Pendentes", pendentes)

with col3:
    st.metric("🚀 Em andamento", em_andamento)

with col4:
    st.metric("✅ Concluídos", concluidos)

st.divider()

planos = listar_planos()

if planos:

    dados_tabela = []

    for plano in planos:
        dados_tabela.append(
            {
                "ID": plano["id"],
                "Prazo": formatar_data_br(plano["prazo"]),
                "Colaborador": plano["colaborador_nome"],
                "Título": plano["titulo"],
                "Origem": plano["origem"],
                "Prioridade": plano["prioridade"],
                "Status": plano["status"],
                "Conclusão": formatar_data_br(plano["data_conclusao"])
            }
        )

    df = pd.DataFrame(dados_tabela)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Ficha do Plano de Ação")

    plano_selecionado = st.selectbox(
        "Selecione um plano de ação",
        planos,
        format_func=lambda item: f"{formatar_data_br(item['prazo'])} | {item['colaborador_nome']} | {item['titulo']}"
    )

    st.markdown(
    f"""
<div style="
    background:#16385C;
    border:1px solid #1E5A8A;
    border-radius:18px;
    padding:24px;
    margin-bottom:18px;
">

<h2 style="color:white;margin-bottom:8px;">
📋 {plano_selecionado["titulo"]}
</h2>

<p style="
    color:white;
    font-size:24px;
    font-weight:600;
    margin-bottom:8px;
">
    {plano_selecionado["colaborador_nome"]}
</p>

<p style="
    color:#CBD5E1;
    margin-bottom:16px;
">
    Origem: {plano_selecionado["origem"]}
</p>

<div style="
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:12px;
">

<div>
<span style="color:#CBD5E1;">⭐ Prioridade</span><br>
<strong style="color:white;">
{plano_selecionado["prioridade"]}
</strong>
</div>

<div>
<span style="color:#CBD5E1;">🚀 Status</span><br>
<strong style="color:white;">
{plano_selecionado["status"]}
</strong>
</div>

<div>
<span style="color:#CBD5E1;">📅 Prazo</span><br>
<strong style="color:white;">
{formatar_data_br(plano_selecionado["prazo"])}
</strong>
</div>

<div>
<span style="color:#CBD5E1;">✅ Conclusão</span><br>
<strong style="color:white;">
{formatar_data_br(plano_selecionado["data_conclusao"])}
</strong>
</div>

</div>

</div>
""",
    unsafe_allow_html=True
)

    pdf_plano = gerar_pdf_plano(plano_selecionado)

    nome_arquivo_plano = (
        f"relatorio_plano_"
        f"{plano_selecionado['colaborador_nome'].replace(' ', '_').lower()}_"
        f"{plano_selecionado['prazo']}.pdf"
    )

    st.markdown(
        """
<div style="background:#111827; border:1px solid #374151; border-radius:16px; padding:18px; margin-bottom:12px;">
    <h4 style="margin:0;color:white;">📄 Relatório do Plano de Ação</h4>
    <p style="margin-top:8px;color:#CBD5E1;font-size:14px;">
        Gere uma versão em PDF com os principais dados deste plano.
    </p>
</div>
""",
        unsafe_allow_html=True
    )

    st.download_button(
        label="📥 Baixar Plano PDF",
        data=pdf_plano,
        file_name=nome_arquivo_plano,
        mime="application/pdf",
        use_container_width=True
    )

    ficha1, ficha2, ficha3 = st.tabs(
        [
            "Resumo",
            "Acompanhamento",
            "Editar"
        ]
    )

    with ficha1:
        st.markdown(
            f"""
<div style="background:#0F2138; border:1px solid #1E4E7A; border-radius:16px; padding:18px; margin-bottom:14px;">
    <h3 style="color:white;">📌 Dados do Plano</h3>
    <p style="color:#CBD5E1;"><strong style="color:white;">Título:</strong> {plano_selecionado["titulo"] or "-"}</p>
    <p style="color:#CBD5E1;"><strong style="color:white;">Origem:</strong> {plano_selecionado["origem"] or "-"}</p>
    <p style="color:#CBD5E1;"><strong style="color:white;">Criação:</strong> {formatar_data_br(plano_selecionado["data_criacao"])}</p>
    <p style="color:#CBD5E1;"><strong style="color:white;">Prazo:</strong> {formatar_data_br(plano_selecionado["prazo"])}</p>
    <p style="color:#CBD5E1;"><strong style="color:white;">Conclusão:</strong> {formatar_data_br(plano_selecionado["data_conclusao"])}</p>
</div>

<div style="background:#0F2138; border:1px solid #1E4E7A; border-radius:16px; padding:18px; margin-bottom:14px;">
    <h3 style="color:white;">📝 Descrição</h3>
    <p style="color:#CBD5E1;">{plano_selecionado["descricao"] or "-"}</p>
</div>
""",
            unsafe_allow_html=True
        )

    with ficha2:
        st.markdown(
            f"""
<div style="background:#0F2138; border:1px solid #1E4E7A; border-radius:16px; padding:18px; margin-bottom:14px;">
    <h3 style="color:white;">📈 Observações do Progresso</h3>
    <p style="color:#CBD5E1;">{plano_selecionado["observacoes_progresso"] or "-"}</p>
</div>
""",
            unsafe_allow_html=True
        )

    with ficha3:
        st.subheader("✏️ Editar Plano de Ação")

        with st.form("form_editar_plano"):

            aba_ed1, aba_ed2 = st.tabs(
                [
                    "Dados do Plano",
                    "Acompanhamento"
                ]
            )

            with aba_ed1:
                col1, col2 = st.columns(2)

                with col1:
                    indice_colaborador = 0

                    for indice, colaborador_item in enumerate(colaboradores):
                        if colaborador_item.id == plano_selecionado["colaborador_id"]:
                            indice_colaborador = indice

                    colaborador_editado = st.selectbox(
                        "Colaborador responsável",
                        colaboradores,
                        index=indice_colaborador,
                        format_func=lambda item: item.nome
                    )

                    titulo_editado = st.text_input(
                        "Título",
                        value=plano_selecionado["titulo"] or ""
                    )

                    origens = [
                        "Reunião",
                        "Feedback",
                        "Demanda do setor",
                        "Observação do gestor",
                        "Outro"
                    ]

                    origem_editada = st.selectbox(
                        "Origem da ação",
                        origens,
                        index=obter_indice(origens, plano_selecionado["origem"])
                    )

                    data_criacao_editada = st.date_input(
                        "Data de criação",
                        value=plano_selecionado["data_criacao"] or date.today(),
                        min_value=DATA_MINIMA,
                        max_value=DATA_MAXIMA,
                        format="DD/MM/YYYY"
                    )

                with col2:
                    prazo_editado = st.date_input(
                        "Prazo",
                        value=plano_selecionado["prazo"] or date.today(),
                        min_value=DATA_MINIMA,
                        max_value=DATA_MAXIMA,
                        format="DD/MM/YYYY"
                    )

                    prioridades = [
                        "Baixa",
                        "Média",
                        "Alta",
                        "Crítica"
                    ]

                    prioridade_editada = st.selectbox(
                        "Prioridade",
                        prioridades,
                        index=obter_indice(prioridades, plano_selecionado["prioridade"])
                    )

                    status_opcoes = [
                        "Pendente",
                        "Em andamento",
                        "Concluído",
                        "Cancelado"
                    ]

                    status_editado = st.selectbox(
                        "Status",
                        status_opcoes,
                        index=obter_indice(status_opcoes, plano_selecionado["status"])
                    )

                    data_conclusao_editada = st.date_input(
                        "Data de conclusão",
                        value=plano_selecionado["data_conclusao"] or date.today(),
                        min_value=DATA_MINIMA,
                        max_value=DATA_MAXIMA,
                        format="DD/MM/YYYY"
                    )

                descricao_editada = st.text_area(
                    "Descrição",
                    value=plano_selecionado["descricao"] or "",
                    height=140
                )

            with aba_ed2:
                observacoes_progresso_editada = st.text_area(
                    "Observações do progresso",
                    value=plano_selecionado["observacoes_progresso"] or "",
                    height=180
                )

            salvar_edicao = st.form_submit_button("Salvar Alterações")

            if salvar_edicao:

                if not titulo_editado:
                    st.error("Informe o título do plano de ação.")
                else:
                    dados_editados = {
                        "colaborador_id": colaborador_editado.id,
                        "titulo": titulo_editado,
                        "descricao": descricao_editada,
                        "origem": origem_editada,
                        "data_criacao": data_criacao_editada,
                        "prazo": prazo_editado,
                        "prioridade": prioridade_editada,
                        "status": status_editado,
                        "observacoes_progresso": observacoes_progresso_editada,
                        "data_conclusao": data_conclusao_editada
                    }

                    editar_plano(
                        plano_selecionado["id"],
                        dados_editados
                    )

                    st.success("Plano de ação atualizado com sucesso.")
                    st.rerun()

                    st.divider()

        st.markdown("### 🗑 Zona de Perigo")

        st.warning(
            "Excluir este plano de ação remove o registro definitivamente."
        )

        confirmar_exclusao = st.checkbox(
            "Confirmo que desejo excluir este plano de ação.",
            key=f"confirmar_exclusao_plano_{plano_selecionado['id']}"
        )

        if st.button(
            "🗑 Excluir Plano de Ação",
            type="secondary",
            use_container_width=True,
            disabled=not confirmar_exclusao
        ):

            excluir_plano(plano_selecionado["id"])

            st.success("Plano de ação excluído com sucesso.")
            st.rerun()
    
else:
    st.warning("Nenhum plano de ação cadastrado ainda.")

with st.expander("➕ Novo Plano de Ação", expanded=False):

    with st.form("form_novo_plano"):

        aba1, aba2 = st.tabs(
            [
                "Dados do Plano",
                "Acompanhamento"
            ]
        )

        with aba1:
            col1, col2 = st.columns(2)

            with col1:
                colaborador = st.selectbox(
                    "Colaborador responsável",
                    colaboradores,
                    format_func=lambda item: item.nome
                )

                titulo = st.text_input("Título")

                origem = st.selectbox(
                    "Origem da ação",
                    [
                        "Reunião",
                        "Feedback",
                        "Demanda do setor",
                        "Observação do gestor",
                        "Outro"
                    ]
                )

                data_criacao = st.date_input(
                    "Data de criação",
                    value=date.today(),
                    min_value=DATA_MINIMA,
                    max_value=DATA_MAXIMA,
                    format="DD/MM/YYYY"
                )

            with col2:
                prazo = st.date_input(
                    "Prazo",
                    value=date.today(),
                    min_value=DATA_MINIMA,
                    max_value=DATA_MAXIMA,
                    format="DD/MM/YYYY"
                )

                prioridade = st.selectbox(
                    "Prioridade",
                    [
                        "Baixa",
                        "Média",
                        "Alta",
                        "Crítica"
                    ]
                )

                status = st.selectbox(
                    "Status",
                    [
                        "Pendente",
                        "Em andamento",
                        "Concluído",
                        "Cancelado"
                    ]
                )

                progresso = st.slider(
                    "Percentual de progresso",
                    min_value=0,
                    max_value=100,
                    value=0,
                    step=5
                )

                data_conclusao = st.date_input(
                    "Data de conclusão",
                    value=None,
                    min_value=DATA_MINIMA,
                    max_value=DATA_MAXIMA,
                    format="DD/MM/YYYY"
                )

            descricao = st.text_area(
                "Descrição",
                height=140
            )

        with aba2:
            observacoes_progresso = st.text_area(
                "Observações do progresso",
                height=180
            )

        salvar = st.form_submit_button("Salvar Plano de Ação")

        if salvar:

            if not titulo:
                st.error("Informe o título do plano de ação.")
            else:
                dados = {
                    "colaborador_id": colaborador.id,
                    "titulo": titulo,
                    "descricao": descricao,
                    "origem": origem,
                    "data_criacao": data_criacao,
                    "prazo": prazo,
                    "prioridade": prioridade,
                    "status": status,
                    "observacoes_progresso": f"Progresso: {progresso}%\n\n{observacoes_progresso}",
                    "data_conclusao": data_conclusao
                }

                criar_plano(dados)

                st.success("Plano de ação cadastrado com sucesso.")
                st.rerun()
