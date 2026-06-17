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
from services.notas_service import criar_nota
from services.notas_service import listar_notas
from services.notas_service import editar_nota
from services.notas_service import excluir_nota

from utils.datas import formatar_data_br


DATA_MINIMA = date(1950, 1, 1)
DATA_MAXIMA = date(2150, 12, 31)


st.markdown(
    """
<div style="background:linear-gradient(135deg,#1D4ED8,#2563EB,#38BDF8); padding:26px; border-radius:20px; margin-bottom:26px;">
    <h1 style="color:white;margin-bottom:8px;">🗒️ Notas Rápidas</h1>
    <p style="color:#E0F2FE;font-size:16px;margin-bottom:0;">
        Registre observações, ideias, pendências, acompanhamentos e pontos importantes da rotina de gestão.
    </p>
</div>
""",
    unsafe_allow_html=True
)


colaboradores = listar_colaboradores()


st.divider()

st.subheader("Histórico de Notas")

notas = listar_notas()

total_notas = len(notas)

notas_altas = len(
    [
        nota for nota in notas
        if nota["prioridade"] in ["Alta", "Crítica"]
    ]
)

notas_7_dias = len(
    [
        nota for nota in notas
        if nota["data"]
        and (date.today() - nota["data"]).days <= 7
    ]
)

notas_30_dias = len(
    [
        nota for nota in notas
        if nota["data"]
        and (date.today() - nota["data"]).days <= 30
    ]
)

categorias_utilizadas = len(
    set(
        [
            nota["categoria"]
            for nota in notas
            if nota["categoria"]
        ]
    )
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🗒️ Notas", total_notas)

with col2:
    st.metric("🔥 Altas/Críticas", notas_altas)

with col3:
    st.metric("📅 7 dias", notas_7_dias)

with col4:
    st.metric("🗓️ 30 dias", notas_30_dias)

with col5:
    st.metric("📂 Categorias", categorias_utilizadas)

st.divider()

if notas:

    busca = st.text_input(
        "🔎 Buscar nota",
        placeholder="Busque por título, conteúdo, categoria, prioridade ou tag..."
    )

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

    if busca:
        busca_normalizada = busca.strip().lower()

        notas_filtradas = [
            n for n in notas_filtradas
            if busca_normalizada in str(n["titulo"] or "").lower()
            or busca_normalizada in str(n["conteudo"] or "").lower()
            or busca_normalizada in str(n["categoria"] or "").lower()
            or busca_normalizada in str(n["prioridade"] or "").lower()
            or busca_normalizada in str(n["tag"] or "").lower()
            or busca_normalizada in str(n["colaborador_nome"] or "").lower()
        ]

    notas_7_dias = len(
        [
            nota for nota in notas
            if nota["data"] and (date.today() - nota["data"]).days <= 7
        ]
    )

    notas_30_dias = len(
        [
            nota for nota in notas
            if nota["data"] and (date.today() - nota["data"]).days <= 30
        ]
    )

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

for i in range(0, len(dados_tabela), 2):

    col1, col2 = st.columns(2)

    with col1:
        nota = dados_tabela[i]

        st.markdown(
            f"""
<div style="background:#0F172A; border-left:6px solid #1E4E7A; padding:18px; border-radius:12px; margin-bottom:12px;">
    <h4 style="margin:0;color:white;">📝 {nota["Título"]}</h4>
    <p style="margin-top:8px;color:#CBD5E1;">
        <strong style="color:white;">Data:</strong> {nota["Data"]}<br>
        <strong style="color:white;">Categoria:</strong> {nota["Categoria"]}<br>
        <strong style="color:white;">Prioridade:</strong> {nota["Prioridade"]}<br>
        <strong style="color:white;">Colaborador:</strong> {nota["Colaborador"]}<br>
        <strong style="color:white;">Tag:</strong> {nota["Tag"] or "-"}
    </p>
</div>
""",
            unsafe_allow_html=True
        )

    if i + 1 < len(dados_tabela):
        with col2:
            nota = dados_tabela[i + 1]

            st.markdown(
                f"""
<div style="background:#0F172A; border-left:6px solid #1E4E7A; padding:18px; border-radius:12px; margin-bottom:12px;">
    <h4 style="margin:0;color:white;">📝 {nota["Título"]}</h4>
    <p style="margin-top:8px;color:#CBD5E1;">
        <strong style="color:white;">Data:</strong> {nota["Data"]}<br>
        <strong style="color:white;">Categoria:</strong> {nota["Categoria"]}<br>
        <strong style="color:white;">Prioridade:</strong> {nota["Prioridade"]}<br>
        <strong style="color:white;">Colaborador:</strong> {nota["Colaborador"]}<br>
        <strong style="color:white;">Tag:</strong> {nota["Tag"] or "-"}
    </p>
</div>
""",
                unsafe_allow_html=True
            )

        st.divider()

        st.subheader("Ficha da Nota")

        nota_selecionada = st.selectbox(
            "Selecione uma nota",
            notas_filtradas,
            format_func=lambda item: f"{formatar_data_br(item['data'])} | {item['titulo']}"
        )

        st.markdown("### 📄 Detalhes da Nota")

        prioridade = nota_selecionada["prioridade"] or "-"

        cor_prioridade = "#1E4E7A"

        if prioridade == "Alta":
            cor_prioridade = "#D97706"
        elif prioridade == "Crítica":
            cor_prioridade = "#DC2626"
        elif prioridade == "Média":
            cor_prioridade = "#CA8A04"

        badges_html = f"""
<div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
    <span style="background:#0F172A; border:1px solid #1E4E7A; color:white; padding:8px 12px; border-radius:999px;">
        📂 {nota_selecionada["categoria"] or "-"}
    </span>
    <span style="background:{cor_prioridade}; color:white; padding:8px 12px; border-radius:999px;">
        🔥 {prioridade}
    </span>
    <span style="background:#0F172A; border:1px solid #1E4E7A; color:white; padding:8px 12px; border-radius:999px;">
        👤 {nota_selecionada["colaborador_nome"] or "-"}
    </span>
    <span style="background:#0F172A; border:1px solid #1E4E7A; color:white; padding:8px 12px; border-radius:999px;">
        🏷️ {nota_selecionada["tag"] or "-"}
    </span>
</div>
"""

        st.markdown(
            badges_html,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
<div style="background:#0F172A;
            padding:20px;
            border-radius:12px;
            border-left:6px solid #2563EB;
            margin-top:10px;">

<h3 style="color:white;">
📝 {nota_selecionada["titulo"]}
</h3>

<p style="color:#CBD5E1;">
<strong>Data:</strong> {formatar_data_br(nota_selecionada["data"])}
</p>

<hr style="border:1px solid #1E293B;">

<p style="color:#E2E8F0; white-space:pre-wrap;">
{nota_selecionada["conteudo"] or "-"}
</p>

</div>
""",
    unsafe_allow_html=True
)

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