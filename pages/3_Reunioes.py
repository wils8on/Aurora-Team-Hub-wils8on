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
from services.colaboradores_service import atualizar_datas_reuniao_colaborador
from services.reunioes_service import criar_reuniao
from services.reunioes_service import listar_reunioes
from services.reunioes_service import editar_reuniao
from services.reunioes_service import excluir_reuniao

from utils.datas import formatar_data_br
from services.relatorios_service import gerar_pdf_reuniao


DATA_MINIMA = date(1950, 1, 1)
DATA_MAXIMA = date(2150, 12, 31)


def obter_indice(lista, valor, padrao=0):

    if valor in lista:
        return lista.index(valor)

    return padrao


st.markdown(
    """
<div style="background:linear-gradient(135deg,#1D4ED8,#2563EB,#38BDF8); padding:26px; border-radius:20px; margin-bottom:26px;">
    <h1 style="color:white;margin-bottom:8px;">🤝 Gestão de Reuniões</h1>
    <p style="color:#E0F2FE;font-size:16px;margin-bottom:0;">
        Registro, acompanhamento e histórico das reuniões 1:1, alinhamentos e conversas de desenvolvimento.
    </p>
</div>
""",
    unsafe_allow_html=True
)


colaboradores = listar_colaboradores()

if not colaboradores:
    st.warning("Cadastre pelo menos um colaborador antes de registrar reuniões.")
    st.stop()





st.divider()

st.subheader("Histórico de Reuniões")

reunioes = listar_reunioes()

if reunioes:

    dados_tabela = []

    for reuniao in reunioes:
        dados_tabela.append(
            {
                "ID": reuniao["id"],
                "Data": formatar_data_br(reuniao["data"]),
                "Colaborador": reuniao["colaborador_nome"],
                "Tipo": reuniao["tipo"],
                "Status": reuniao["status"],
                "Formato": reuniao["formato"],
                "Assunto": reuniao["assunto_principal"],
                "Follow-up": reuniao["follow_up"],
                "Prioridade": reuniao["prioridade"]
            }
        )

    df = pd.DataFrame(dados_tabela)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Ficha da Reunião")

    reuniao_selecionada = st.selectbox(
        "Selecione uma reunião",
        reunioes,
        format_func=lambda item: f"{formatar_data_br(item['data'])} | {item['colaborador_nome']} | {item['assunto_principal']}"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Colaborador", reuniao_selecionada["colaborador_nome"] or "-")

    with col2:
        st.metric("Tipo", reuniao_selecionada["tipo"] or "-")

    with col3:
        st.metric("Status", reuniao_selecionada["status"] or "-")

    with col4:
        st.metric("Prioridade", reuniao_selecionada["prioridade"] or "-")

    ficha1, ficha2, ficha3, ficha4 = st.tabs(
        [
            "Resumo",
            "Condução",
            "Acompanhamento",
            "Editar"
        ]
    )

    with ficha1:
        st.write("**Data:**", formatar_data_br(reuniao_selecionada["data"]))
        st.write("**Formato:**", reuniao_selecionada["formato"] or "-")
        st.write("**Assunto principal:**", reuniao_selecionada["assunto_principal"] or "-")

        st.write("**Pauta:**")
        st.write(reuniao_selecionada["pauta"] or "-")

        st.write("**Resumo final:**")
        st.write(reuniao_selecionada["resumo_final"] or "-")

        st.divider()

        pdf_reuniao = gerar_pdf_reuniao(reuniao_selecionada)

        nome_arquivo_pdf = (
            f"relatorio_reuniao_"
            f"{reuniao_selecionada['colaborador_nome'].replace(' ', '_').lower()}_"
            f"{reuniao_selecionada['data']}.pdf"
        )

        st.download_button(
            label="📄 Baixar Relatório da Reunião em PDF",
            data=pdf_reuniao,
            file_name=nome_arquivo_pdf,
            mime="application/pdf"
        )

    with ficha2:
        st.write("**Humor percebido:**", reuniao_selecionada["humor_percebido"] or "-")

        st.write("**Situação atual:**")
        st.write(reuniao_selecionada["situacao_atual"] or "-")

        st.write("**Dificuldades relatadas:**")
        st.write(reuniao_selecionada["dificuldades_relatadas"] or "-")

        st.write("**Pontos positivos:**")
        st.write(reuniao_selecionada["pontos_positivos"] or "-")

        st.write("**Feedback recebido pelo gestor:**")
        st.write(reuniao_selecionada["feedback_recebido"] or "-")

        st.write("**Feedback dado ao colaborador:**")
        st.write(reuniao_selecionada["feedback_dado"] or "-")

    with ficha3:
        st.write("**Decisões tomadas:**")
        st.write(reuniao_selecionada["decisoes_tomadas"] or "-")

        st.write("**Combinados:**")
        st.write(reuniao_selecionada["combinados"] or "-")

        st.write("**Próximos passos:**")
        st.write(reuniao_selecionada["proximos_passos"] or "-")

        st.write("**Precisa follow-up?:**", reuniao_selecionada["follow_up"] or "-")

    with ficha4:
        st.subheader("✏️ Editar Reunião")

        with st.form("form_editar_reuniao"):

            aba_ed1, aba_ed2, aba_ed3, aba_ed4 = st.tabs(
                [
                    "Dados da Reunião",
                    "Condução",
                    "Feedbacks e Decisões",
                    "Acompanhamento"
                ]
            )

            with aba_ed1:
                col1, col2 = st.columns(2)

                with col1:
                    indice_colaborador = 0

                    for indice, colaborador_item in enumerate(colaboradores):
                        if colaborador_item.id == reuniao_selecionada["colaborador_id"]:
                            indice_colaborador = indice

                    colaborador_editado = st.selectbox(
                        "Colaborador",
                        colaboradores,
                        index=indice_colaborador,
                        format_func=lambda item: item.nome
                    )

                    data_editada = st.date_input(
                        "Data da reunião",
                        value=reuniao_selecionada["data"] or date.today(),
                        min_value=DATA_MINIMA,
                        max_value=DATA_MAXIMA,
                        format="DD/MM/YYYY"
                    )

                    tipos = [
                        "1:1",
                        "Alinhamento",
                        "Feedback",
                        "Acompanhamento",
                        "Desenvolvimento",
                        "Informal"
                    ]

                    tipo_editado = st.selectbox(
                        "Tipo de reunião",
                        tipos,
                        index=obter_indice(tipos, reuniao_selecionada["tipo"])
                    )

                with col2:
                    status_opcoes = [
                        "Agendada",
                        "Realizada",
                        "Cancelada",
                        "Reagendada"
                    ]

                    status_editado = st.selectbox(
                        "Status",
                        status_opcoes,
                        index=obter_indice(status_opcoes, reuniao_selecionada["status"])
                    )

                    formatos = [
                        "Presencial",
                        "Online",
                        "Híbrido"
                    ]

                    formato_editado = st.selectbox(
                        "Formato",
                        formatos,
                        index=obter_indice(formatos, reuniao_selecionada["formato"])
                    )

                    prioridades = [
                        "Baixa",
                        "Média",
                        "Alta",
                        "Crítica"
                    ]

                    prioridade_editada = st.selectbox(
                        "Prioridade do acompanhamento",
                        prioridades,
                        index=obter_indice(prioridades, reuniao_selecionada["prioridade"])
                    )

                assunto_principal_editado = st.text_input(
                    "Assunto principal",
                    value=reuniao_selecionada["assunto_principal"] or ""
                )

                pauta_editada = st.text_area(
                    "Pauta da reunião",
                    value=reuniao_selecionada["pauta"] or "",
                    height=150
                )

            with aba_ed2:
                humores = [
                    "Não avaliado",
                    "Tranquilo",
                    "Motivado",
                    "Sobrecarregado",
                    "Preocupado",
                    "Desmotivado",
                    "Irritado",
                    "Entusiasmado"
                ]

                humor_percebido_editado = st.selectbox(
                    "Humor percebido do colaborador",
                    humores,
                    index=obter_indice(humores, reuniao_selecionada["humor_percebido"])
                )

                situacao_atual_editada = st.text_area(
                    "Como o colaborador se encontra no momento?",
                    value=reuniao_selecionada["situacao_atual"] or "",
                    height=120
                )

                dificuldades_relatadas_editada = st.text_area(
                    "Dificuldades relatadas",
                    value=reuniao_selecionada["dificuldades_relatadas"] or "",
                    height=120
                )

                pontos_positivos_editado = st.text_area(
                    "Pontos positivos relatados",
                    value=reuniao_selecionada["pontos_positivos"] or "",
                    height=120
                )

            with aba_ed3:
                feedback_recebido_editado = st.text_area(
                    "Feedback recebido pelo gestor",
                    value=reuniao_selecionada["feedback_recebido"] or "",
                    height=120
                )

                feedback_dado_editado = st.text_area(
                    "Feedback dado ao colaborador",
                    value=reuniao_selecionada["feedback_dado"] or "",
                    height=120
                )

                decisoes_tomadas_editada = st.text_area(
                    "Decisões tomadas",
                    value=reuniao_selecionada["decisoes_tomadas"] or "",
                    height=120
                )

                combinados_editado = st.text_area(
                    "Combinados definidos",
                    value=reuniao_selecionada["combinados"] or "",
                    height=120
                )

            with aba_ed4:
                proximos_passos_editado = st.text_area(
                    "Próximos passos",
                    value=reuniao_selecionada["proximos_passos"] or "",
                    height=120
                )

                resumo_final_editado = st.text_area(
                    "Resumo final da reunião",
                    value=reuniao_selecionada["resumo_final"] or "",
                    height=150
                )

                follow_opcoes = [
                    "Não",
                    "Sim"
                ]

                follow_up_editado = st.selectbox(
                    "Precisa follow-up?",
                    follow_opcoes,
                    index=obter_indice(follow_opcoes, reuniao_selecionada["follow_up"])
                )

            salvar_edicao = st.form_submit_button("Salvar Alterações")

            if salvar_edicao:

                if not assunto_principal_editado:
                    st.error("Informe o assunto principal da reunião.")
                else:
                    dados_editados = {
                        "colaborador_id": colaborador_editado.id,
                        "data": data_editada,
                        "tipo": tipo_editado,
                        "status": status_editado,
                        "formato": formato_editado,
                        "assunto_principal": assunto_principal_editado,
                        "pauta": pauta_editada,
                        "humor_percebido": humor_percebido_editado,
                        "situacao_atual": situacao_atual_editada,
                        "dificuldades_relatadas": dificuldades_relatadas_editada,
                        "pontos_positivos": pontos_positivos_editado,
                        "feedback_recebido": feedback_recebido_editado,
                        "feedback_dado": feedback_dado_editado,
                        "decisoes_tomadas": decisoes_tomadas_editada,
                        "combinados": combinados_editado,
                        "proximos_passos": proximos_passos_editado,
                        "resumo_final": resumo_final_editado,
                        "follow_up": follow_up_editado,
                        "prioridade": prioridade_editada
                    }

                    editar_reuniao(
                        reuniao_selecionada["id"],
                        dados_editados
                    )

                    if status_editado == "Realizada":
                        atualizar_datas_reuniao_colaborador(
                            colaborador_editado.id,
                            data_editada
                        )

                    st.success("Reunião atualizada com sucesso.")
                    st.rerun()

    st.divider()

    st.subheader("Excluir Reunião")

    reuniao_para_excluir = st.selectbox(
        "Selecione a reunião para excluir",
        reunioes,
        format_func=lambda item: f"{formatar_data_br(item['data'])} | {item['colaborador_nome']} | {item['assunto_principal']}",
        key="excluir_reuniao"
    )

    if st.button("Excluir Reunião", type="secondary"):

        excluir_reuniao(reuniao_para_excluir["id"])

        st.success("Reunião excluída com sucesso.")
        st.rerun()

else:
    st.warning("Nenhuma reunião cadastrada ainda.")

st.divider()

with st.expander("➕ Nova Reunião", expanded=False):

    with st.form("form_nova_reuniao"):

        aba1, aba2, aba3, aba4 = st.tabs(
            [
                "Dados da Reunião",
                "Condução",
                "Feedbacks e Decisões",
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

                data_reuniao = st.date_input(
                    "Data da reunião",
                    value=date.today(),
                    min_value=DATA_MINIMA,
                    max_value=DATA_MAXIMA,
                    format="DD/MM/YYYY"
                )

                tipo = st.selectbox(
                    "Tipo de reunião",
                    [
                        "1:1",
                        "Alinhamento",
                        "Feedback",
                        "Acompanhamento",
                        "Desenvolvimento",
                        "Informal"
                    ]
                )

            with col2:
                status = st.selectbox(
                    "Status",
                    [
                        "Agendada",
                        "Realizada",
                        "Cancelada",
                        "Reagendada"
                    ]
                )

                formato = st.selectbox(
                    "Formato",
                    [
                        "Presencial",
                        "Online",
                        "Híbrido"
                    ]
                )

                prioridade = st.selectbox(
                    "Prioridade do acompanhamento",
                    [
                        "Baixa",
                        "Média",
                        "Alta",
                        "Crítica"
                    ]
                )

            assunto_principal = st.text_input("Assunto principal")

            pauta = st.text_area(
                "Pauta da reunião",
                height=150
            )

        with aba2:
            humor_percebido = st.selectbox(
                "Humor percebido do colaborador",
                [
                    "Não avaliado",
                    "Tranquilo",
                    "Motivado",
                    "Sobrecarregado",
                    "Preocupado",
                    "Desmotivado",
                    "Irritado",
                    "Entusiasmado"
                ]
            )

            situacao_atual = st.text_area(
                "Como o colaborador se encontra no momento?",
                height=120
            )

            dificuldades_relatadas = st.text_area(
                "Dificuldades relatadas",
                height=120
            )

            pontos_positivos = st.text_area(
                "Pontos positivos relatados",
                height=120
            )

        with aba3:
            feedback_recebido = st.text_area(
                "Feedback recebido pelo gestor",
                height=120
            )

            feedback_dado = st.text_area(
                "Feedback dado ao colaborador",
                height=120
            )

            decisoes_tomadas = st.text_area(
                "Decisões tomadas",
                height=120
            )

            combinados = st.text_area(
                "Combinados definidos",
                height=120
            )

        with aba4:
            proximos_passos = st.text_area(
                "Próximos passos",
                height=120
            )

            resumo_final = st.text_area(
                "Resumo final da reunião",
                height=150
            )

            follow_up = st.selectbox(
                "Precisa follow-up?",
                [
                    "Não",
                    "Sim"
                ]
            )

        salvar = st.form_submit_button("Salvar Reunião")

        if salvar:

            if not assunto_principal:
                st.error("Informe o assunto principal da reunião.")
            else:
                dados = {
                    "colaborador_id": colaborador.id,
                    "data": data_reuniao,
                    "tipo": tipo,
                    "status": status,
                    "formato": formato,
                    "assunto_principal": assunto_principal,
                    "pauta": pauta,
                    "humor_percebido": humor_percebido,
                    "situacao_atual": situacao_atual,
                    "dificuldades_relatadas": dificuldades_relatadas,
                    "pontos_positivos": pontos_positivos,
                    "feedback_recebido": feedback_recebido,
                    "feedback_dado": feedback_dado,
                    "decisoes_tomadas": decisoes_tomadas,
                    "combinados": combinados,
                    "proximos_passos": proximos_passos,
                    "resumo_final": resumo_final,
                    "follow_up": follow_up,
                    "prioridade": prioridade
                }

                criar_reuniao(dados)

                if status == "Realizada":
                    atualizar_datas_reuniao_colaborador(
                        colaborador.id,
                        data_reuniao
                    )

                st.success("Reunião cadastrada com sucesso.")
                st.rerun()