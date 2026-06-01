import streamlit as st
import pandas as pd

from datetime import date

from services.colaboradores_service import listar_colaboradores
from services.notas_service import criar_nota
from services.notas_service import listar_notas
from services.notas_service import editar_nota
from services.notas_service import excluir_nota

from utils.datas import formatar_data_br


DATA_MINIMA = date(1950, 1, 1)
DATA_MAXIMA = date(2150, 12, 31)


st.title("🗒️ Notas Rápidas")

st.info("Registre anotações rápidas sobre rotina, equipe, ideias e acompanhamentos.")


colaboradores = listar_colaboradores()


with st.expander("➕ Nova Nota", expanded=False):

    with st.form("form_nova_nota"):

        col1, col2 = st.columns(2)

        with col1:
            titulo = st.text_input("Título")

            data_nota = st.date_input(
                "Data",
                value=date.today(),
                min_value=DATA_MINIMA,
                max_value=DATA_MAXIMA,
                format="DD/MM/YYYY"
            )

            categoria = st.selectbox(
                "Categoria",
                [
                    "Geral",
                    "Colaborador",
                    "Reunião",
                    "Feedback",
                    "Plano de ação",
                    "Ideia",
                    "Pendência",
                    "Outro"
                ]
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

        with col2:
            relacionar_colaborador = st.selectbox(
                "Relacionar a colaborador?",
                [
                    "Não",
                    "Sim"
                ]
            )

            colaborador_id = None

            if relacionar_colaborador == "Sim":

                if colaboradores:
                    colaborador = st.selectbox(
                        "Colaborador relacionado",
                        colaboradores,
                        format_func=lambda item: item.nome
                    )

                    colaborador_id = colaborador.id
                else:
                    st.warning("Nenhum colaborador cadastrado.")

            tag = st.text_input("Tag")

        conteudo = st.text_area(
            "Conteúdo da nota",
            height=180
        )

        salvar = st.form_submit_button("Salvar Nota")

        if salvar:

            if not titulo:
                st.error("Informe o título da nota.")
            elif not conteudo:
                st.error("Informe o conteúdo da nota.")
            else:
                dados = {
                    "titulo": titulo,
                    "conteudo": conteudo,
                    "data": data_nota,
                    "categoria": categoria,
                    "colaborador_id": colaborador_id,
                    "prioridade": prioridade,
                    "tag": tag
                }

                criar_nota(dados)

                st.success("Nota cadastrada com sucesso.")
                st.rerun()


st.divider()

st.subheader("Histórico de Notas")

notas = listar_notas()

if notas:

    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        filtro_categoria = st.selectbox(
            "Filtrar por categoria",
            ["Todas"] + sorted(list(set([n["categoria"] for n in notas if n["categoria"]])))
        )

    with col_f2:
        filtro_prioridade = st.selectbox(
            "Filtrar por prioridade",
            ["Todas"] + sorted(list(set([n["prioridade"] for n in notas if n["prioridade"]])))
        )

    with col_f3:
        filtro_colaborador = st.selectbox(
            "Filtrar por colaborador",
            ["Todos"] + sorted(list(set([n["colaborador_nome"] for n in notas if n["colaborador_nome"] != "-"])))
        )

    notas_filtradas = notas

    if filtro_categoria != "Todas":
        notas_filtradas = [
            n for n in notas_filtradas
            if n["categoria"] == filtro_categoria
        ]

    if filtro_prioridade != "Todas":
        notas_filtradas = [
            n for n in notas_filtradas
            if n["prioridade"] == filtro_prioridade
        ]

    if filtro_colaborador != "Todos":
        notas_filtradas = [
            n for n in notas_filtradas
            if n["colaborador_nome"] == filtro_colaborador
        ]

    if notas_filtradas:

        dados_tabela = []

        for nota in notas_filtradas:
            dados_tabela.append(
                {
                    "ID": nota["id"],
                    "Data": formatar_data_br(nota["data"]),
                    "Título": nota["titulo"],
                    "Categoria": nota["categoria"],
                    "Prioridade": nota["prioridade"],
                    "Colaborador": nota["colaborador_nome"],
                    "Tag": nota["tag"]
                }
            )

        df = pd.DataFrame(dados_tabela)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("Ficha da Nota")

        nota_selecionada = st.selectbox(
            "Selecione uma nota",
            notas_filtradas,
            format_func=lambda item: f"{formatar_data_br(item['data'])} | {item['titulo']}"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Categoria", nota_selecionada["categoria"] or "-")

        with col2:
            st.metric("Prioridade", nota_selecionada["prioridade"] or "-")

        with col3:
            st.metric("Colaborador", nota_selecionada["colaborador_nome"] or "-")

        with col4:
            st.metric("Tag", nota_selecionada["tag"] or "-")

        st.write("**Data:**", formatar_data_br(nota_selecionada["data"]))
        st.write("**Título:**", nota_selecionada["titulo"] or "-")

        st.write("**Conteúdo:**")
        st.write(nota_selecionada["conteudo"] or "-")

        st.divider()

        st.subheader("✏️ Editar Nota")

        with st.expander("Editar nota selecionada", expanded=False):

            with st.form("form_editar_nota"):

                col1, col2 = st.columns(2)

                with col1:
                    titulo_editado = st.text_input(
                        "Título",
                        value=nota_selecionada["titulo"] or ""
                    )

                    data_editada = st.date_input(
                        "Data",
                        value=nota_selecionada["data"] or date.today(),
                        min_value=DATA_MINIMA,
                        max_value=DATA_MAXIMA,
                        format="DD/MM/YYYY"
                    )

                    categoria_editada = st.selectbox(
                        "Categoria",
                        [
                            "Geral",
                            "Colaborador",
                            "Reunião",
                            "Feedback",
                            "Plano de ação",
                            "Ideia",
                            "Pendência",
                            "Outro"
                        ],
                        index=[
                            "Geral",
                            "Colaborador",
                            "Reunião",
                            "Feedback",
                            "Plano de ação",
                            "Ideia",
                            "Pendência",
                            "Outro"
                        ].index(nota_selecionada["categoria"])
                        if nota_selecionada["categoria"] in [
                            "Geral",
                            "Colaborador",
                            "Reunião",
                            "Feedback",
                            "Plano de ação",
                            "Ideia",
                            "Pendência",
                            "Outro"
                        ]
                        else 0
                    )

                    prioridade_editada = st.selectbox(
                        "Prioridade",
                        [
                            "Baixa",
                            "Média",
                            "Alta",
                            "Crítica"
                        ],
                        index=[
                            "Baixa",
                            "Média",
                            "Alta",
                            "Crítica"
                        ].index(nota_selecionada["prioridade"])
                        if nota_selecionada["prioridade"] in [
                            "Baixa",
                            "Média",
                            "Alta",
                            "Crítica"
                        ]
                        else 0
                    )

                with col2:
                    opcoes_colaborador = ["Sem colaborador"] + colaboradores

                    indice_colaborador = 0

                    for indice, colaborador in enumerate(opcoes_colaborador):
                        if colaborador != "Sem colaborador":
                            if colaborador.id == nota_selecionada.get("colaborador_id"):
                                indice_colaborador = indice

                    colaborador_editado = st.selectbox(
                        "Colaborador relacionado",
                        opcoes_colaborador,
                        index=indice_colaborador,
                        format_func=lambda item: item if item == "Sem colaborador" else item.nome
                    )

                    colaborador_id_editado = None

                    if colaborador_editado != "Sem colaborador":
                        colaborador_id_editado = colaborador_editado.id

                    tag_editada = st.text_input(
                        "Tag",
                        value=nota_selecionada["tag"] or ""
                    )

                conteudo_editado = st.text_area(
                    "Conteúdo da nota",
                    value=nota_selecionada["conteudo"] or "",
                    height=180
                )

                salvar_edicao = st.form_submit_button("Salvar Alterações")

                if salvar_edicao:

                    if not titulo_editado:
                        st.error("Informe o título da nota.")
                    elif not conteudo_editado:
                        st.error("Informe o conteúdo da nota.")
                    else:
                        dados_editados = {
                            "titulo": titulo_editado,
                            "conteudo": conteudo_editado,
                            "data": data_editada,
                            "categoria": categoria_editada,
                            "prioridade": prioridade_editada,
                            "tag": tag_editada,
                            "colaborador_id": colaborador_id_editado
                        }

                        editar_nota(
                            nota_selecionada["id"],
                            dados_editados
                        )

                        st.success("Nota atualizada com sucesso.")
                        st.rerun()

        st.divider()

        st.subheader("Excluir Nota")

        nota_para_excluir = st.selectbox(
            "Selecione a nota para excluir",
            notas_filtradas,
            format_func=lambda item: f"{formatar_data_br(item['data'])} | {item['titulo']}",
            key="excluir_nota"
        )

        if st.button("Excluir Nota", type="secondary"):

            excluir_nota(nota_para_excluir["id"])

            st.success("Nota excluída com sucesso.")
            st.rerun()

    else:
        st.warning("Nenhuma nota encontrada com os filtros selecionados.")

else:
    st.warning("Nenhuma nota cadastrada ainda.")