import streamlit as st
import pandas as pd

from datetime import date

from services.colaboradores_service import listar_colaboradores
from services.planos_service import criar_plano
from services.planos_service import listar_planos
from services.planos_service import editar_plano
from services.planos_service import excluir_plano

from utils.datas import formatar_data_br


DATA_MINIMA = date(1950, 1, 1)
DATA_MAXIMA = date(2150, 12, 31)


def obter_indice(lista, valor, padrao=0):

    if valor in lista:
        return lista.index(valor)

    return padrao


st.title("📋 Planos de Ação")

st.info("Acompanhe ações, prazos, prioridades e evolução dos colaboradores.")


colaboradores = listar_colaboradores()

if not colaboradores:
    st.warning("Cadastre pelo menos um colaborador antes de registrar planos de ação.")
    st.stop()


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


st.divider()

st.subheader("Histórico de Planos de Ação")

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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Colaborador", plano_selecionado["colaborador_nome"] or "-")

    with col2:
        st.metric("Prioridade", plano_selecionado["prioridade"] or "-")

    with col3:
        st.metric("Status", plano_selecionado["status"] or "-")

    with col4:
        st.metric("Prazo", formatar_data_br(plano_selecionado["prazo"]))

    ficha1, ficha2, ficha3 = st.tabs(
        [
            "Resumo",
            "Acompanhamento",
            "Editar"
        ]
    )

    with ficha1:
        st.write("**Título:**", plano_selecionado["titulo"] or "-")
        st.write("**Origem:**", plano_selecionado["origem"] or "-")
        st.write("**Data de criação:**", formatar_data_br(plano_selecionado["data_criacao"]))
        st.write("**Prazo:**", formatar_data_br(plano_selecionado["prazo"]))
        st.write("**Data de conclusão:**", formatar_data_br(plano_selecionado["data_conclusao"]))

        st.write("**Descrição:**")
        st.write(plano_selecionado["descricao"] or "-")

    with ficha2:
        st.write("**Observações do progresso:**")
        st.write(plano_selecionado["observacoes_progresso"] or "-")

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

    st.subheader("Excluir Plano de Ação")

    plano_para_excluir = st.selectbox(
        "Selecione o plano para excluir",
        planos,
        format_func=lambda item: f"{formatar_data_br(item['prazo'])} | {item['colaborador_nome']} | {item['titulo']}",
        key="excluir_plano"
    )

    if st.button("Excluir Plano de Ação", type="secondary"):

        excluir_plano(plano_para_excluir["id"])

        st.success("Plano de ação excluído com sucesso.")
        st.rerun()

else:
    st.warning("Nenhum plano de ação cadastrado ainda.")