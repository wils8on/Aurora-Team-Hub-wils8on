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
from services.radar_service import criar_radar
from services.radar_service import listar_radares
from services.radar_service import editar_radar
from services.radar_service import excluir_radar
from services.relatorios_service import gerar_pdf_radar

from utils.datas import formatar_data_br


DATA_MINIMA = date(1950, 1, 1)
DATA_MAXIMA = date(2150, 12, 31)


st.markdown(
    """
<div style="background:linear-gradient(135deg,#1D4ED8,#2563EB,#38BDF8); padding:26px; border-radius:20px; margin-bottom:26px;">
    <h1 style="color:white;margin-bottom:8px;">📡 Radar do Colaborador</h1>
    <p style="color:#E0F2FE;font-size:16px;margin-bottom:0;">
        Acompanhe percepção gerencial, motivação, performance, carga, engajamento, alinhamento e risco de desgaste.
    </p>
</div>
""",
    unsafe_allow_html=True
)


colaboradores = listar_colaboradores()

if not colaboradores:
    st.warning("Cadastre pelo menos um colaborador antes de registrar o radar.")
    st.stop()


st.divider()

st.subheader("Histórico do Radar")

radares = listar_radares()

total_registros = len(radares)

motivacao_media = round(
    sum(r["motivacao"] for r in radares) / total_registros,
    1
) if total_registros else 0

engajamento_medio = round(
    sum(r["engajamento"] for r in radares) / total_registros,
    1
) if total_registros else 0

risco_medio = round(
    sum(r["risco_desgaste"] for r in radares) / total_registros,
    1
) if total_registros else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📡 Registros", total_registros)

with col2:
    st.metric("😀 Motivação", motivacao_media)

with col3:
    st.metric("🚀 Engajamento", engajamento_medio)

with col4:
    st.metric("⚠️ Risco", risco_medio)

st.divider()

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

    st.subheader("Ficha do Registro")

    radar_selecionado = st.selectbox(
        "Selecione um registro",
        radares,
        format_func=lambda item: f"{formatar_data_br(item['data_registro'])} | {item['colaborador_nome']}"
    )

    ficha1, ficha2 = st.tabs(
        [
            "Resumo",
            "Editar"
        ]
    )

    with ficha1:

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
📡 Radar de Colaborador
</h2>

<p style="
color:white;
font-size:24px;
font-weight:600;
margin-bottom:8px;
">
{radar_selecionado["colaborador_nome"]}
</p>

<p style="
color:#CBD5E1;
margin-bottom:16px;
">
Registro realizado em {formatar_data_br(radar_selecionado["data_registro"])}
</p>

<div style="
display:grid;
grid-template-columns:repeat(3,1fr);
gap:12px;
">

<div>
<span style="color:#CBD5E1;">😀 Motivação</span><br>
<strong style="color:white;">
{radar_selecionado["motivacao"]}/5
</strong>
</div>

<div>
<span style="color:#CBD5E1;">🚀 Performance</span><br>
<strong style="color:white;">
{radar_selecionado["performance"]}/5
</strong>
</div>

<div>
<span style="color:#CBD5E1;">⚠️ Risco</span><br>
<strong style="color:white;">
{radar_selecionado["risco_desgaste"]}/5
</strong>
</div>

<div>
<span style="color:#CBD5E1;">📦 Carga</span><br>
<strong style="color:white;">
{radar_selecionado["carga_trabalho"]}/5
</strong>
</div>

<div>
<span style="color:#CBD5E1;">🤝 Engajamento</span><br>
<strong style="color:white;">
{radar_selecionado["engajamento"]}/5
</strong>
</div>

<div>
<span style="color:#CBD5E1;">👥 Alinhamento</span><br>
<strong style="color:white;">
{radar_selecionado["alinhamento_equipe"]}/5
</strong>
</div>

</div>

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
<div style="
background:#0F2138;
border:1px solid #1E4E7A;
border-radius:16px;
padding:18px;
margin-bottom:14px;
">

<h3 style="color:white;">
📝 Observações do Gestor
</h3>

<p style="color:#CBD5E1;">
{radar_selecionado["observacoes"] or "-"}
</p>

</div>
""",
            unsafe_allow_html=True
        )

        motivacao = radar_selecionado["motivacao"]
        performance = radar_selecionado["performance"]
        engajamento = radar_selecionado["engajamento"]
        risco = radar_selecionado["risco_desgaste"]

        resumo = []

        if motivacao >= 4:
            resumo.append(
                f"Motivação elevada ({motivacao}/5)."
            )
        elif motivacao <= 2:
            resumo.append(
                f"Motivação em atenção ({motivacao}/5)."
            )

        if performance >= 4:
            resumo.append(
                f"Performance consistente ({performance}/5)."
            )
        elif performance <= 2:
            resumo.append(
                f"Performance abaixo do esperado ({performance}/5)."
            )

        if engajamento >= 4:
            resumo.append(
                f"Engajamento alto ({engajamento}/5)."
            )
        elif engajamento <= 2:
            resumo.append(
                f"Engajamento reduzido ({engajamento}/5)."
            )

        if risco >= 4:
            resumo.append(
                f"Risco de desgaste elevado ({risco}/5). Recomenda-se acompanhamento próximo."
            )
        elif risco <= 2:
            resumo.append(
                f"Risco de desgaste baixo ({risco}/5)."
            )

        if not resumo:
            resumo.append(
                "Os indicadores apresentam comportamento estável no período avaliado."
            )

        texto_resumo = " ".join(resumo)

        st.markdown(
            f"""
<div style="
background:#0F2138;
border:1px solid #1E4E7A;
border-radius:16px;
padding:18px;
margin-bottom:14px;
">

<h3 style="color:white;">
📋 Resumo Executivo Aurora
</h3>

<p style="color:#CBD5E1;">
{texto_resumo}
</p>

</div>
""",
            unsafe_allow_html=True
        )


        pdf_radar = gerar_pdf_radar(radar_selecionado)

        nome_arquivo_radar = (
            f"relatorio_radar_"
            f"{radar_selecionado['colaborador_nome'].replace(' ', '_').lower()}_"
            f"{radar_selecionado['data_registro']}.pdf"
        )

        st.markdown(
            """
<div style="background:#111827; border:1px solid #374151; border-radius:16px; padding:18px; margin-bottom:12px;">
    <h4 style="margin:0;color:white;">📄 Relatório do Radar</h4>
    <p style="margin-top:8px;color:#CBD5E1;font-size:14px;">
        Gere uma versão em PDF com os principais indicadores deste registro de radar.
    </p>
</div>
""",
            unsafe_allow_html=True
        )

        st.download_button(
            label="📥 Baixar Radar PDF",
            data=pdf_radar,
            file_name=nome_arquivo_radar,
            mime="application/pdf",
            use_container_width=True
        )

    with ficha2:
        st.subheader("✏️ Editar Registro de Radar")

        with st.form("form_editar_radar"):

            col1, col2 = st.columns(2)

            with col1:
                indice_colaborador = 0

                for indice, colaborador_item in enumerate(colaboradores):
                    if colaborador_item.id == radar_selecionado["colaborador_id"]:
                        indice_colaborador = indice

                colaborador_editado = st.selectbox(
                    "Colaborador",
                    colaboradores,
                    index=indice_colaborador,
                    format_func=lambda item: item.nome
                )

                data_registro_editada = st.date_input(
                    "Data do registro",
                    value=radar_selecionado["data_registro"] or date.today(),
                    min_value=DATA_MINIMA,
                    max_value=DATA_MAXIMA,
                    format="DD/MM/YYYY"
                )

                motivacao_editada = st.slider(
                    "Motivação",
                    1,
                    5,
                    int(radar_selecionado["motivacao"] or 3)
                )

                performance_editada = st.slider(
                    "Performance percebida",
                    1,
                    5,
                    int(radar_selecionado["performance"] or 3)
                )

                carga_trabalho_editada = st.slider(
                    "Carga de trabalho",
                    1,
                    5,
                    int(radar_selecionado["carga_trabalho"] or 3)
                )

            with col2:
                engajamento_editado = st.slider(
                    "Engajamento",
                    1,
                    5,
                    int(radar_selecionado["engajamento"] or 3)
                )

                risco_desgaste_editado = st.slider(
                    "Risco de desgaste / burnout",
                    1,
                    5,
                    int(radar_selecionado["risco_desgaste"] or 3)
                )

                alinhamento_equipe_editado = st.slider(
                    "Alinhamento com a equipe",
                    1,
                    5,
                    int(radar_selecionado["alinhamento_equipe"] or 3)
                )

                observacoes_editadas = st.text_area(
                    "Observações",
                    value=radar_selecionado["observacoes"] or "",
                    height=180
                )

            salvar_edicao = st.form_submit_button("Salvar Alterações")

            if salvar_edicao:

                dados_editados = {
                    "colaborador_id": colaborador_editado.id,
                    "data_registro": data_registro_editada,
                    "motivacao": motivacao_editada,
                    "performance": performance_editada,
                    "carga_trabalho": carga_trabalho_editada,
                    "engajamento": engajamento_editado,
                    "risco_desgaste": risco_desgaste_editado,
                    "alinhamento_equipe": alinhamento_equipe_editado,
                    "observacoes": observacoes_editadas
                }

                editar_radar(
                    radar_selecionado["id"],
                    dados_editados
                )

                st.success("Registro de radar atualizado com sucesso.")
                st.rerun()
                
        st.divider()

        st.markdown("### 🗑 Zona de Perigo")

        st.warning(
            "Excluir este registro removerá permanentemente o histórico deste radar."
        )

        confirmar_exclusao = st.checkbox(
            "Confirmo que desejo excluir este registro.",
            key=f"confirmar_exclusao_radar_{radar_selecionado['id']}"
        )

        if st.button(
            "🗑 Excluir Registro",
            type="secondary",
            use_container_width=True,
            disabled=not confirmar_exclusao
        ):

            excluir_radar(
                radar_selecionado["id"]
            )

            st.success(
                "Registro excluído com sucesso."
            )

            st.rerun()
    
else:
    st.warning("Nenhum registro de radar cadastrado ainda.")

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