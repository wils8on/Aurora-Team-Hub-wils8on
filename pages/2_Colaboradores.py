import streamlit as st
import pandas as pd

from datetime import date

from services.colaboradores_service import criar_colaborador
from services.colaboradores_service import listar_colaboradores
from services.colaboradores_service import editar_colaborador
from services.colaboradores_service import excluir_colaborador

from services.evolucoes_service import criar_evolucao
from services.evolucoes_service import listar_evolucoes_colaborador

from utils.datas import formatar_data_br


DATA_MINIMA = date(1950, 1, 1)
DATA_MAXIMA = date(2150, 12, 31)


def formatar_aniversario(data):

    if not data:
        return "-"

    return data.strftime("%d/%m")


def obter_indice(lista, valor, padrao=0):

    if valor in lista:
        return lista.index(valor)

    return padrao


st.title("👥 Colaboradores")

st.info("Cadastro completo e acompanhamento gerencial dos colaboradores.")


with st.expander("➕ Novo Colaborador", expanded=False):

    with st.form("form_novo_colaborador"):

        aba1, aba2, aba3, aba4, aba5 = st.tabs(
            [
                "Dados Básicos",
                "Operacional",
                "Desenvolvimento",
                "Gestão",
                "Observações"
            ]
        )

        with aba1:
            col1, col2 = st.columns(2)

            with col1:
                nome = st.text_input("Nome completo")
                nome_social = st.text_input("Nome social")
                cargo = st.text_input("Cargo atual")
                email = st.text_input("E-mail corporativo")
                email_pessoal = st.text_input("E-mail pessoal")
                telefone = st.text_input("Telefone corporativo")
                telefone_pessoal = st.text_input("Telefone pessoal")

            with col2:
                unidade = st.selectbox(
                    "Unidade / Filial",
                    [
                        "Matriz",
                        "São Caetano do Sul",
                        "Belém",
                        "Outro"
                    ]
                )

                data_admissao = st.date_input(
                    "Data de admissão",
                    value=date.today(),
                    min_value=DATA_MINIMA,
                    max_value=DATA_MAXIMA,
                    format="DD/MM/YYYY"
                )

                st.caption("Aniversário cadastrado apenas como dia e mês.")

                col_dia, col_mes = st.columns(2)

                with col_dia:
                    aniversario_dia = st.number_input(
                        "Dia do aniversário",
                        min_value=1,
                        max_value=31,
                        value=1,
                        step=1
                    )

                with col_mes:
                    aniversario_mes = st.number_input(
                        "Mês do aniversário",
                        min_value=1,
                        max_value=12,
                        value=1,
                        step=1
                    )

                try:
                    data_aniversario = date(
                        2000,
                        int(aniversario_mes),
                        int(aniversario_dia)
                    )
                except ValueError:
                    data_aniversario = None
                    st.warning("Dia e mês de aniversário inválidos.")

                tipo_contrato = st.selectbox(
                    "Tipo de contrato atual",
                    [
                        "CLT",
                        "Estágio",
                        "PJ",
                        "Temporário",
                        "Outro"
                    ]
                )

                gestor_direto = st.text_input("Gestor direto")
                area_equipe = st.text_input("Área / Equipe")

                status = st.selectbox(
                    "Status",
                    [
                        "Ativo",
                        "Férias",
                        "Afastado",
                        "Desligado"
                    ]
                )

        with aba2:
            principais_responsabilidades = st.text_area("Principais responsabilidades")
            projetos_atuais = st.text_area("Projetos atuais")
            prioridades_atuais = st.text_area("Prioridades atuais")
            entregas_responsabilidade = st.text_area("Entregas sob responsabilidade")
            observacoes_operacionais = st.text_area("Observações operacionais")

        with aba3:
            pontos_fortes = st.text_area("Pontos fortes")
            pontos_desenvolvimento = st.text_area("Pontos de desenvolvimento")
            perfil_comportamental = st.text_area("Perfil comportamental")
            interesses_desenvolvimento = st.text_area("Interesses de desenvolvimento")
            objetivos_profissionais = st.text_area("Objetivos profissionais")
            competencias_desenvolver = st.text_area("Competências a desenvolver")

        with aba4:
            col1, col2 = st.columns(2)

            with col1:
                frequencia_1_1 = st.selectbox(
                    "Frequência ideal de 1:1",
                    [
                        "Semanal",
                        "Quinzenal",
                        "Mensal",
                        "Sob demanda"
                    ]
                )

                data_ultima_reuniao = st.date_input(
                    "Data da última reunião",
                    value=date.today(),
                    min_value=DATA_MINIMA,
                    max_value=DATA_MAXIMA,
                    format="DD/MM/YYYY"
                )

                proxima_reuniao_recomendada = st.date_input(
                    "Próxima reunião recomendada",
                    value=date.today(),
                    min_value=DATA_MINIMA,
                    max_value=DATA_MAXIMA,
                    format="DD/MM/YYYY"
                )

            with col2:
                satisfacao_percebida = st.selectbox(
                    "Nível de satisfação percebido",
                    [
                        "Não avaliado",
                        "Baixo",
                        "Médio",
                        "Alto"
                    ]
                )

                risco_percebido = st.selectbox(
                    "Risco percebido",
                    [
                        "Baixo",
                        "Médio",
                        "Alto"
                    ]
                )

                momento_atual = st.selectbox(
                    "Momento atual",
                    [
                        "Estável",
                        "Sobrecarregado",
                        "Em evolução",
                        "Desmotivado",
                        "Destaque"
                    ]
                )

        with aba5:
            observacoes_gerais = st.text_area(
                "Observações gerais",
                height=220
            )

        salvar = st.form_submit_button("Salvar Colaborador")

        if salvar:

            if not nome:
                st.error("Informe o nome do colaborador.")
            elif data_aniversario is None:
                st.error("Informe uma data de aniversário válida.")
            else:
                dados = {
                    "nome": nome,
                    "nome_social": nome_social,
                    "cargo": cargo,
                    "email": email,
                    "email_pessoal": email_pessoal,
                    "telefone": telefone,
                    "telefone_pessoal": telefone_pessoal,
                    "unidade": unidade,
                    "data_admissao": data_admissao,
                    "data_aniversario": data_aniversario,
                    "tipo_contrato": tipo_contrato,
                    "gestor_direto": gestor_direto,
                    "area_equipe": area_equipe,
                    "status": status,
                    "principais_responsabilidades": principais_responsabilidades,
                    "projetos_atuais": projetos_atuais,
                    "prioridades_atuais": prioridades_atuais,
                    "entregas_responsabilidade": entregas_responsabilidade,
                    "observacoes_operacionais": observacoes_operacionais,
                    "pontos_fortes": pontos_fortes,
                    "pontos_desenvolvimento": pontos_desenvolvimento,
                    "perfil_comportamental": perfil_comportamental,
                    "interesses_desenvolvimento": interesses_desenvolvimento,
                    "objetivos_profissionais": objetivos_profissionais,
                    "competencias_desenvolver": competencias_desenvolver,
                    "frequencia_1_1": frequencia_1_1,
                    "data_ultima_reuniao": data_ultima_reuniao,
                    "proxima_reuniao_recomendada": proxima_reuniao_recomendada,
                    "satisfacao_percebida": satisfacao_percebida,
                    "risco_percebido": risco_percebido,
                    "momento_atual": momento_atual,
                    "observacoes_gerais": observacoes_gerais
                }

                criar_colaborador(dados)

                st.success("Colaborador cadastrado com sucesso.")
                st.rerun()


st.divider()

st.subheader("Lista de Colaboradores")

colaboradores = listar_colaboradores()

if colaboradores:

    dados_tabela = []

    for colaborador in colaboradores:
        dados_tabela.append(
            {
                "ID": colaborador.id,
                "Nome": colaborador.nome,
                "Nome social": colaborador.nome_social,
                "Cargo": colaborador.cargo,
                "E-mail": colaborador.email,
                "Telefone": colaborador.telefone,
                "Unidade": colaborador.unidade,
                "Área": colaborador.area_equipe,
                "Admissão": formatar_data_br(colaborador.data_admissao),
                "Aniversário": formatar_aniversario(colaborador.data_aniversario),
                "Contrato": colaborador.tipo_contrato,
                "Status": colaborador.status,
                "Momento": colaborador.momento_atual,
                "Risco": colaborador.risco_percebido
            }
        )

    df = pd.DataFrame(dados_tabela)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Ficha Gerencial")

    colaborador_selecionado = st.selectbox(
        "Selecione um colaborador para visualizar a ficha",
        colaboradores,
        format_func=lambda colaborador: colaborador.nome
    )

    st.markdown(f"## {colaborador_selecionado.nome}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Cargo", colaborador_selecionado.cargo or "-")

    with col2:
        st.metric("Contrato", colaborador_selecionado.tipo_contrato or "-")

    with col3:
        st.metric("Momento", colaborador_selecionado.momento_atual or "-")

    with col4:
        st.metric("Risco", colaborador_selecionado.risco_percebido or "-")

    ficha1, ficha2, ficha3, ficha4, ficha5, ficha6, ficha7 = st.tabs(
        [
            "Resumo",
            "Operacional",
            "Desenvolvimento",
            "Gestão",
            "Evoluções",
            "Editar",
            "Observações"
        ]
    )

    with ficha1:
        st.write("**Nome social:**", colaborador_selecionado.nome_social or "-")
        st.write("**E-mail corporativo:**", colaborador_selecionado.email or "-")
        st.write("**E-mail pessoal:**", colaborador_selecionado.email_pessoal or "-")
        st.write("**Telefone corporativo:**", colaborador_selecionado.telefone or "-")
        st.write("**Telefone pessoal:**", colaborador_selecionado.telefone_pessoal or "-")
        st.write("**Unidade:**", colaborador_selecionado.unidade or "-")
        st.write("**Data de admissão:**", formatar_data_br(colaborador_selecionado.data_admissao))
        st.write("**Aniversário:**", formatar_aniversario(colaborador_selecionado.data_aniversario))
        st.write("**Cargo atual:**", colaborador_selecionado.cargo or "-")
        st.write("**Tipo de contrato atual:**", colaborador_selecionado.tipo_contrato or "-")
        st.write("**Gestor direto:**", colaborador_selecionado.gestor_direto or "-")
        st.write("**Área / Equipe:**", colaborador_selecionado.area_equipe or "-")
        st.write("**Status:**", colaborador_selecionado.status or "-")

    with ficha2:
        st.write("**Principais responsabilidades:**")
        st.write(colaborador_selecionado.principais_responsabilidades or "-")

        st.write("**Projetos atuais:**")
        st.write(colaborador_selecionado.projetos_atuais or "-")

        st.write("**Prioridades atuais:**")
        st.write(colaborador_selecionado.prioridades_atuais or "-")

        st.write("**Entregas sob responsabilidade:**")
        st.write(colaborador_selecionado.entregas_responsabilidade or "-")

    with ficha3:
        st.write("**Pontos fortes:**")
        st.write(colaborador_selecionado.pontos_fortes or "-")

        st.write("**Pontos de desenvolvimento:**")
        st.write(colaborador_selecionado.pontos_desenvolvimento or "-")

        st.write("**Perfil comportamental:**")
        st.write(colaborador_selecionado.perfil_comportamental or "-")

        st.write("**Interesses de desenvolvimento:**")
        st.write(colaborador_selecionado.interesses_desenvolvimento or "-")

        st.write("**Objetivos profissionais:**")
        st.write(colaborador_selecionado.objetivos_profissionais or "-")

        st.write("**Competências a desenvolver:**")
        st.write(colaborador_selecionado.competencias_desenvolver or "-")

    with ficha4:
        st.write("**Frequência ideal de 1:1:**", colaborador_selecionado.frequencia_1_1 or "-")

        st.write(
            "**Data da última reunião:**",
            formatar_data_br(colaborador_selecionado.data_ultima_reuniao)
        )

        st.write(
            "**Próxima reunião recomendada:**",
            formatar_data_br(colaborador_selecionado.proxima_reuniao_recomendada)
        )

        st.write("**Satisfação percebida:**", colaborador_selecionado.satisfacao_percebida or "-")
        st.write("**Risco percebido:**", colaborador_selecionado.risco_percebido or "-")
        st.write("**Momento atual:**", colaborador_selecionado.momento_atual or "-")

    with ficha5:
        st.subheader("Histórico de Evoluções")

        with st.expander("➕ Registrar Evolução", expanded=False):

            with st.form("form_evolucao_colaborador"):

                data_evolucao = st.date_input(
                    "Data da evolução",
                    value=date.today(),
                    min_value=DATA_MINIMA,
                    max_value=DATA_MAXIMA,
                    format="DD/MM/YYYY"
                )

                tipo_evolucao = st.selectbox(
                    "Tipo de evolução",
                    [
                        "Mudança de cargo",
                        "Mudança de contrato",
                        "Promoção",
                        "Alteração de função",
                        "Outro"
                    ]
                )

                col1, col2 = st.columns(2)

                with col1:
                    cargo_anterior = st.text_input(
                        "Cargo anterior",
                        value=colaborador_selecionado.cargo or ""
                    )

                    contrato_anterior = st.text_input(
                        "Contrato anterior",
                        value=colaborador_selecionado.tipo_contrato or ""
                    )

                with col2:
                    cargo_novo = st.text_input("Novo cargo")
                    contrato_novo = st.text_input("Novo tipo de contrato")

                motivo = st.text_area("Motivo da evolução")
                observacoes = st.text_area("Observações")

                salvar_evolucao = st.form_submit_button("Salvar Evolução")

                if salvar_evolucao:

                    if not cargo_novo and not contrato_novo:
                        st.error("Informe ao menos novo cargo ou novo tipo de contrato.")
                    else:
                        dados_evolucao = {
                            "colaborador_id": colaborador_selecionado.id,
                            "data": data_evolucao,
                            "tipo_evolucao": tipo_evolucao,
                            "cargo_anterior": cargo_anterior,
                            "cargo_novo": cargo_novo,
                            "contrato_anterior": contrato_anterior,
                            "contrato_novo": contrato_novo,
                            "motivo": motivo,
                            "observacoes": observacoes
                        }

                        criar_evolucao(dados_evolucao)

                        dados_atualizacao = {}

                        if cargo_novo:
                            dados_atualizacao["cargo"] = cargo_novo

                        if contrato_novo:
                            dados_atualizacao["tipo_contrato"] = contrato_novo

                        if dados_atualizacao:
                            editar_colaborador(
                                colaborador_selecionado.id,
                                dados_atualizacao
                            )

                        st.success("Evolução registrada com sucesso.")
                        st.rerun()

        evolucoes = listar_evolucoes_colaborador(colaborador_selecionado.id)

        if evolucoes:

            dados_evolucoes = []

            for evolucao in evolucoes:
                dados_evolucoes.append(
                    {
                        "Data": formatar_data_br(evolucao["data"]),
                        "Tipo": evolucao["tipo_evolucao"],
                        "Cargo anterior": evolucao["cargo_anterior"],
                        "Novo cargo": evolucao["cargo_novo"],
                        "Contrato anterior": evolucao["contrato_anterior"],
                        "Novo contrato": evolucao["contrato_novo"],
                        "Motivo": evolucao["motivo"],
                        "Observações": evolucao["observacoes"]
                    }
                )

            df_evolucoes = pd.DataFrame(dados_evolucoes)

            st.dataframe(
                df_evolucoes,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("Nenhuma evolução registrada para este colaborador.")

    with ficha6:
        st.subheader("✏️ Editar Colaborador")

        with st.form("form_editar_colaborador"):

            aba_ed1, aba_ed2, aba_ed3, aba_ed4, aba_ed5 = st.tabs(
                [
                    "Dados Básicos",
                    "Operacional",
                    "Desenvolvimento",
                    "Gestão",
                    "Observações"
                ]
            )

            with aba_ed1:
                col1, col2 = st.columns(2)

                with col1:
                    nome_editado = st.text_input(
                        "Nome completo",
                        value=colaborador_selecionado.nome or ""
                    )

                    nome_social_editado = st.text_input(
                        "Nome social",
                        value=colaborador_selecionado.nome_social or ""
                    )

                    cargo_editado = st.text_input(
                        "Cargo atual",
                        value=colaborador_selecionado.cargo or ""
                    )

                    email_editado = st.text_input(
                        "E-mail corporativo",
                        value=colaborador_selecionado.email or ""
                    )

                    email_pessoal_editado = st.text_input(
                        "E-mail pessoal",
                        value=colaborador_selecionado.email_pessoal or ""
                    )

                    telefone_editado = st.text_input(
                        "Telefone corporativo",
                        value=colaborador_selecionado.telefone or ""
                    )

                    telefone_pessoal_editado = st.text_input(
                        "Telefone pessoal",
                        value=colaborador_selecionado.telefone_pessoal or ""
                    )

                with col2:
                    unidades = [
                        "Matriz",
                        "São Caetano do Sul",
                        "Belém",
                        "Outro"
                    ]

                    unidade_editada = st.selectbox(
                        "Unidade / Filial",
                        unidades,
                        index=obter_indice(unidades, colaborador_selecionado.unidade)
                    )

                    data_admissao_editada = st.date_input(
                        "Data de admissão",
                        value=colaborador_selecionado.data_admissao or date.today(),
                        min_value=DATA_MINIMA,
                        max_value=DATA_MAXIMA,
                        format="DD/MM/YYYY"
                    )

                    aniversario_atual = colaborador_selecionado.data_aniversario

                    st.caption("Aniversário cadastrado apenas como dia e mês.")

                    col_dia_ed, col_mes_ed = st.columns(2)

                    with col_dia_ed:
                        aniversario_dia_editado = st.number_input(
                            "Dia do aniversário",
                            min_value=1,
                            max_value=31,
                            value=aniversario_atual.day if aniversario_atual else 1,
                            step=1,
                            key="editar_aniversario_dia"
                        )

                    with col_mes_ed:
                        aniversario_mes_editado = st.number_input(
                            "Mês do aniversário",
                            min_value=1,
                            max_value=12,
                            value=aniversario_atual.month if aniversario_atual else 1,
                            step=1,
                            key="editar_aniversario_mes"
                        )

                    try:
                        data_aniversario_editada = date(
                            2000,
                            int(aniversario_mes_editado),
                            int(aniversario_dia_editado)
                        )
                    except ValueError:
                        data_aniversario_editada = None
                        st.warning("Dia e mês de aniversário inválidos.")

                    contratos = [
                        "CLT",
                        "Estágio",
                        "PJ",
                        "Temporário",
                        "Outro"
                    ]

                    tipo_contrato_editado = st.selectbox(
                        "Tipo de contrato atual",
                        contratos,
                        index=obter_indice(contratos, colaborador_selecionado.tipo_contrato)
                    )

                    gestor_direto_editado = st.text_input(
                        "Gestor direto",
                        value=colaborador_selecionado.gestor_direto or ""
                    )

                    area_equipe_editada = st.text_input(
                        "Área / Equipe",
                        value=colaborador_selecionado.area_equipe or ""
                    )

                    status_opcoes = [
                        "Ativo",
                        "Férias",
                        "Afastado",
                        "Desligado"
                    ]

                    status_editado = st.selectbox(
                        "Status",
                        status_opcoes,
                        index=obter_indice(status_opcoes, colaborador_selecionado.status)
                    )

            with aba_ed2:
                principais_responsabilidades_editado = st.text_area(
                    "Principais responsabilidades",
                    value=colaborador_selecionado.principais_responsabilidades or ""
                )

                projetos_atuais_editado = st.text_area(
                    "Projetos atuais",
                    value=colaborador_selecionado.projetos_atuais or ""
                )

                prioridades_atuais_editado = st.text_area(
                    "Prioridades atuais",
                    value=colaborador_selecionado.prioridades_atuais or ""
                )

                entregas_responsabilidade_editado = st.text_area(
                    "Entregas sob responsabilidade",
                    value=colaborador_selecionado.entregas_responsabilidade or ""
                )

                observacoes_operacionais_editado = st.text_area(
                    "Observações operacionais",
                    value=colaborador_selecionado.observacoes_operacionais or ""
                )

            with aba_ed3:
                pontos_fortes_editado = st.text_area(
                    "Pontos fortes",
                    value=colaborador_selecionado.pontos_fortes or ""
                )

                pontos_desenvolvimento_editado = st.text_area(
                    "Pontos de desenvolvimento",
                    value=colaborador_selecionado.pontos_desenvolvimento or ""
                )

                perfil_comportamental_editado = st.text_area(
                    "Perfil comportamental",
                    value=colaborador_selecionado.perfil_comportamental or ""
                )

                interesses_desenvolvimento_editado = st.text_area(
                    "Interesses de desenvolvimento",
                    value=colaborador_selecionado.interesses_desenvolvimento or ""
                )

                objetivos_profissionais_editado = st.text_area(
                    "Objetivos profissionais",
                    value=colaborador_selecionado.objetivos_profissionais or ""
                )

                competencias_desenvolver_editado = st.text_area(
                    "Competências a desenvolver",
                    value=colaborador_selecionado.competencias_desenvolver or ""
                )

            with aba_ed4:
                col1, col2 = st.columns(2)

                with col1:
                    frequencias = [
                        "Semanal",
                        "Quinzenal",
                        "Mensal",
                        "Sob demanda"
                    ]

                    frequencia_1_1_editado = st.selectbox(
                        "Frequência ideal de 1:1",
                        frequencias,
                        index=obter_indice(frequencias, colaborador_selecionado.frequencia_1_1)
                    )

                    data_ultima_reuniao_editada = st.date_input(
                        "Data da última reunião",
                        value=colaborador_selecionado.data_ultima_reuniao or date.today(),
                        min_value=DATA_MINIMA,
                        max_value=DATA_MAXIMA,
                        format="DD/MM/YYYY"
                    )

                    proxima_reuniao_recomendada_editada = st.date_input(
                        "Próxima reunião recomendada",
                        value=colaborador_selecionado.proxima_reuniao_recomendada or date.today(),
                        min_value=DATA_MINIMA,
                        max_value=DATA_MAXIMA,
                        format="DD/MM/YYYY"
                    )

                with col2:
                    satisfacoes = [
                        "Não avaliado",
                        "Baixo",
                        "Médio",
                        "Alto"
                    ]

                    satisfacao_percebida_editada = st.selectbox(
                        "Nível de satisfação percebido",
                        satisfacoes,
                        index=obter_indice(satisfacoes, colaborador_selecionado.satisfacao_percebida)
                    )

                    riscos = [
                        "Baixo",
                        "Médio",
                        "Alto"
                    ]

                    risco_percebido_editado = st.selectbox(
                        "Risco percebido",
                        riscos,
                        index=obter_indice(riscos, colaborador_selecionado.risco_percebido)
                    )

                    momentos = [
                        "Estável",
                        "Sobrecarregado",
                        "Em evolução",
                        "Desmotivado",
                        "Destaque"
                    ]

                    momento_atual_editado = st.selectbox(
                        "Momento atual",
                        momentos,
                        index=obter_indice(momentos, colaborador_selecionado.momento_atual)
                    )

            with aba_ed5:
                observacoes_gerais_editado = st.text_area(
                    "Observações gerais",
                    value=colaborador_selecionado.observacoes_gerais or "",
                    height=220
                )

            salvar_edicao = st.form_submit_button("Salvar Alterações")

            if salvar_edicao:

                if not nome_editado:
                    st.error("Informe o nome do colaborador.")
                elif data_aniversario_editada is None:
                    st.error("Informe uma data de aniversário válida.")
                else:
                    dados_editados = {
                        "nome": nome_editado,
                        "nome_social": nome_social_editado,
                        "cargo": cargo_editado,
                        "email": email_editado,
                        "email_pessoal": email_pessoal_editado,
                        "telefone": telefone_editado,
                        "telefone_pessoal": telefone_pessoal_editado,
                        "unidade": unidade_editada,
                        "data_admissao": data_admissao_editada,
                        "data_aniversario": data_aniversario_editada,
                        "tipo_contrato": tipo_contrato_editado,
                        "gestor_direto": gestor_direto_editado,
                        "area_equipe": area_equipe_editada,
                        "status": status_editado,
                        "principais_responsabilidades": principais_responsabilidades_editado,
                        "projetos_atuais": projetos_atuais_editado,
                        "prioridades_atuais": prioridades_atuais_editado,
                        "entregas_responsabilidade": entregas_responsabilidade_editado,
                        "observacoes_operacionais": observacoes_operacionais_editado,
                        "pontos_fortes": pontos_fortes_editado,
                        "pontos_desenvolvimento": pontos_desenvolvimento_editado,
                        "perfil_comportamental": perfil_comportamental_editado,
                        "interesses_desenvolvimento": interesses_desenvolvimento_editado,
                        "objetivos_profissionais": objetivos_profissionais_editado,
                        "competencias_desenvolver": competencias_desenvolver_editado,
                        "frequencia_1_1": frequencia_1_1_editado,
                        "data_ultima_reuniao": data_ultima_reuniao_editada,
                        "proxima_reuniao_recomendada": proxima_reuniao_recomendada_editada,
                        "satisfacao_percebida": satisfacao_percebida_editada,
                        "risco_percebido": risco_percebido_editado,
                        "momento_atual": momento_atual_editado,
                        "observacoes_gerais": observacoes_gerais_editado
                    }

                    editar_colaborador(
                        colaborador_selecionado.id,
                        dados_editados
                    )

                    st.success("Colaborador atualizado com sucesso.")
                    st.rerun()

    with ficha7:
        st.write(colaborador_selecionado.observacoes_gerais or "-")

    st.divider()

    st.subheader("Excluir Colaborador")

    colaborador_para_excluir = st.selectbox(
        "Selecione o colaborador",
        colaboradores,
        format_func=lambda colaborador: colaborador.nome,
        key="excluir_colaborador"
    )

    if st.button("Excluir", type="secondary"):

        excluir_colaborador(colaborador_para_excluir.id)

        st.success("Colaborador excluído com sucesso.")
        st.rerun()

else:
    st.warning("Nenhum colaborador cadastrado ainda.")