from services.radar_service import listar_radares
from services.planos_service import listar_planos
from services.reunioes_service import listar_reunioes
from services.colaboradores_service import listar_colaboradores


def gerar_preparacao_1_1(dados_360):

    resumo = []
    perguntas = []
    riscos = []
    proximos_passos = []

    if not dados_360:

        return {
            "resumo": ["Sem dados suficientes para preparação."],
            "riscos": [],
            "perguntas": ["Quais pontos você gostaria de trazer para esta conversa?"],
            "proximos_passos": ["Registrar novos dados do colaborador após a reunião."]
        }

    radar = (
        dados_360["radares"][0]
        if dados_360.get("radares")
        else None
    )

    planos = dados_360.get("planos", [])
    feedbacks = dados_360.get("feedbacks", [])

    if radar:

        motivacao = radar.get("motivacao", 0)
        performance = radar.get("performance", 0)
        engajamento = radar.get("engajamento", 0)
        risco = radar.get("risco_desgaste", 0)

        if performance >= 4:
            resumo.append("Apresenta performance elevada.")

        if motivacao <= 3:
            riscos.append("Motivação abaixo do ideal.")
            perguntas.append(
                "Como você está se sentindo em relação ao trabalho nas últimas semanas?"
            )

        if engajamento <= 3:
            riscos.append("Engajamento moderado ou baixo.")
            perguntas.append(
                "Existe algo dificultando sua conexão com a equipe ou atividades?"
            )

        if risco >= 4:
            riscos.append("Risco elevado de desgaste.")
            perguntas.append("Como está sua carga de trabalho atualmente?")
            proximos_passos.append("Avaliar redistribuição de atividades.")

    planos_abertos = [
        plano for plano in planos
        if plano["status"] in ["Pendente", "Em andamento"]
    ]

    if planos_abertos:

        resumo.append(
            f"Possui {len(planos_abertos)} plano(s) de ação em aberto."
        )

        perguntas.append(
            "Como está o andamento dos planos definidos anteriormente?"
        )

        proximos_passos.append(
            "Revisar andamento dos planos de ação."
        )

    feedbacks_abertos = [
        feedback for feedback in feedbacks
        if feedback["status_acompanhamento"] in ["Aberto", "Em acompanhamento"]
    ]

    if feedbacks_abertos:

        resumo.append(
            f"Possui {len(feedbacks_abertos)} feedback(s) em acompanhamento."
        )

        proximos_passos.append(
            "Validar evolução após feedbacks recentes."
        )

    if not resumo:
        resumo.append("Sem indicadores críticos identificados.")

    if not proximos_passos:
        proximos_passos.append("Manter rotina normal de acompanhamento.")

    resumo = list(dict.fromkeys(resumo))
    riscos = list(dict.fromkeys(riscos))
    perguntas = list(dict.fromkeys(perguntas))
    proximos_passos = list(dict.fromkeys(proximos_passos))

    return {
        "resumo": resumo,
        "riscos": riscos,
        "perguntas": perguntas,
        "proximos_passos": proximos_passos
    }


def gerar_pauta_1_1(dados_360):

    if not dados_360:

        return {
            "pauta": [
                "Realizar acompanhamento geral do colaborador.",
                "Atualizar registros após a conversa."
            ],
            "objetivo": [
                "Coletar informações suficientes para acompanhamento gerencial."
            ],
            "assuntos_sensiveis": []
        }

    radar = (
        dados_360["radares"][0]
        if dados_360.get("radares")
        else None
    )

    planos = dados_360.get("planos", [])
    feedbacks = dados_360.get("feedbacks", [])

    pauta = []
    assuntos_sensiveis = []
    objetivo = []

    if radar:

        motivacao = radar.get("motivacao", 0)
        performance = radar.get("performance", 0)
        engajamento = radar.get("engajamento", 0)
        risco = radar.get("risco_desgaste", 0)

        if motivacao <= 3:
            pauta.append("Conversar sobre motivação e satisfação atual.")
            assuntos_sensiveis.append("Motivação abaixo do ideal.")
            objetivo.append(
                "Compreender fatores que impactam energia, satisfação e engajamento."
            )

        if risco >= 4:
            pauta.append("Avaliar carga de trabalho e risco de desgaste.")
            assuntos_sensiveis.append("Risco elevado de desgaste.")
            objetivo.append(
                "Identificar formas de reduzir sobrecarga e prevenir desgaste."
            )

        if engajamento <= 3:
            pauta.append("Explorar fatores que afetam o engajamento.")
            objetivo.append(
                "Entender se existem barreiras de conexão, clareza ou motivação."
            )

        if performance >= 4:
            pauta.append("Reconhecer pontos positivos de performance.")
            objetivo.append(
                "Reforçar comportamentos positivos e oportunidades de crescimento."
            )

    planos_abertos = [
        plano for plano in planos
        if plano["status"] in ["Pendente", "Em andamento"]
    ]

    if planos_abertos:

        pauta.append("Revisar andamento dos planos de ação.")
        objetivo.append(
            "Garantir execução dos compromissos definidos."
        )

    feedbacks_abertos = [
        feedback for feedback in feedbacks
        if feedback["status_acompanhamento"] in ["Aberto", "Em acompanhamento"]
    ]

    if feedbacks_abertos:

        pauta.append("Validar evolução após feedbacks recentes.")
        objetivo.append(
            "Confirmar se houve avanço nos pontos acompanhados."
        )

    if not pauta:
        pauta.append("Realizar acompanhamento geral do colaborador.")
        pauta.append("Verificar bem-estar, prioridades e expectativas atuais.")

    if not objetivo:
        objetivo.append("Manter alinhamento e acompanhamento contínuo.")

    pauta = list(dict.fromkeys(pauta))
    objetivo = list(dict.fromkeys(objetivo))
    assuntos_sensiveis = list(dict.fromkeys(assuntos_sensiveis))

    return {
        "pauta": pauta,
        "objetivo": objetivo,
        "assuntos_sensiveis": assuntos_sensiveis
    }


def colaboradores_em_atencao():

    radares = listar_radares()
    resultado = []
    vistos = set()

    for radar in radares:

        colaborador_id = radar["colaborador_id"]

        if colaborador_id in vistos:
            continue

        vistos.add(colaborador_id)

        if radar["risco_desgaste"] >= 4:
            resultado.append(
                {
                    "nome": radar["colaborador_nome"],
                    "motivo": "Risco elevado",
                    "recomendacao": "Realizar conversa individual."
                }
            )

        elif radar["motivacao"] <= 2:
            resultado.append(
                {
                    "nome": radar["colaborador_nome"],
                    "motivo": "Motivação baixa",
                    "recomendacao": "Investigar fatores de desmotivação."
                }
            )

    return resultado


def colaboradores_sem_1_1():

    reunioes = listar_reunioes()
    colaboradores = listar_colaboradores()

    ids_com_reuniao = {
        reuniao["colaborador_id"]
        for reuniao in reunioes
        if reuniao["colaborador_id"]
    }

    resultado = []

    for colaborador in colaboradores:

        if colaborador.status != "Ativo":
            continue

        if colaborador.id not in ids_com_reuniao:
            resultado.append(
                {
                    "nome": colaborador.nome,
                    "status": colaborador.status
                }
            )

    return resultado


def planos_pendentes_copilot():

    planos = listar_planos()

    return [
        plano for plano in planos
        if plano["status"] not in ["Concluído", "Cancelado"]
    ]


def resumo_equipe():

    radares = listar_radares()

    if not radares:
        return "Não existem dados suficientes para gerar resumo da equipe."

    media_motivacao = sum(r["motivacao"] for r in radares) / len(radares)
    media_performance = sum(r["performance"] for r in radares) / len(radares)
    media_risco = sum(r["risco_desgaste"] for r in radares) / len(radares)

    return f"""
Equipe analisada com {len(radares)} registro(s) de radar.

Motivação média: {round(media_motivacao, 1)}
Performance média: {round(media_performance, 1)}
Risco médio: {round(media_risco, 1)}

Recomendação:
Acompanhar colaboradores com risco elevado e reforçar ações de engajamento.
"""


def gerar_resumo_colaborador(dados_360):

    if not dados_360:
        return "Colaborador não encontrado ou sem dados suficientes."

    colaborador = dados_360.get("colaborador")

    if not colaborador:
        return "Colaborador não encontrado."

    nome = colaborador.get("nome", "-")

    radar = (
        dados_360["radares"][0]
        if dados_360.get("radares")
        else None
    )

    planos = dados_360.get("planos", [])
    feedbacks = dados_360.get("feedbacks", [])
    reunioes = dados_360.get("reunioes", [])

    texto = []

    texto.append(f"### Colaborador: {nome}")
    texto.append("")

    texto.append("#### Situação Atual")

    if radar:

        motivacao = radar.get("motivacao", 0)
        performance = radar.get("performance", 0)
        engajamento = radar.get("engajamento", 0)
        risco = radar.get("risco_desgaste", 0)
        alinhamento = radar.get("alinhamento_equipe", 0)

        if performance >= 4:
            texto.append("- Apresenta desempenho acima da média.")

        if motivacao <= 3:
            texto.append("- Demonstra sinais de redução de motivação.")

        if risco >= 4:
            texto.append("- Possui risco elevado de desgaste.")

        if engajamento >= 4:
            texto.append("- Mantém bom nível de engajamento.")

        if alinhamento >= 4:
            texto.append("- Apresenta bom alinhamento com a equipe.")

        if not any([
            performance >= 4,
            motivacao <= 3,
            risco >= 4,
            engajamento >= 4,
            alinhamento >= 4
        ]):
            texto.append("- Sem sinais críticos ou destaques expressivos no último radar.")

    else:
        texto.append("- Ainda não há registro de radar para este colaborador.")

    planos_abertos = [
        plano for plano in planos
        if plano["status"] in ["Pendente", "Em andamento"]
    ]

    feedbacks_abertos = [
        feedback for feedback in feedbacks
        if feedback["status_acompanhamento"] in ["Aberto", "Em acompanhamento"]
    ]

    texto.append("")
    texto.append("#### Indicadores de Acompanhamento")
    texto.append(f"- Reuniões registradas: {len(reunioes)}")
    texto.append(f"- Feedbacks registrados: {len(feedbacks)}")
    texto.append(f"- Feedbacks em acompanhamento: {len(feedbacks_abertos)}")
    texto.append(f"- Planos em aberto: {len(planos_abertos)}")

    texto.append("")
    texto.append("#### Recomendação")

    if radar and radar.get("risco_desgaste", 0) >= 4:
        texto.append("- Priorizar acompanhamento individual e revisar carga de trabalho.")
    elif radar and radar.get("motivacao", 0) <= 3:
        texto.append("- Investigar fatores de motivação e reforçar reconhecimento.")
    elif planos_abertos:
        texto.append("- Acompanhar execução dos planos de ação em andamento.")
    else:
        texto.append("- Manter acompanhamento regular e registrar novas evoluções.")

    return "\n".join(texto)


def gerar_analise_equipe():

    radares = listar_radares()

    if not radares:
        return "Não existem dados suficientes para gerar análise da equipe."

    media_motivacao = sum(r["motivacao"] for r in radares) / len(radares)
    media_performance = sum(r["performance"] for r in radares) / len(radares)
    media_engajamento = sum(r["engajamento"] for r in radares) / len(radares)
    media_risco = sum(r["risco_desgaste"] for r in radares) / len(radares)
    media_alinhamento = sum(r["alinhamento_equipe"] for r in radares) / len(radares)

    alto_risco = [
        r for r in radares
        if r["risco_desgaste"] >= 4
    ]

    motivacao_baixa = [
        r for r in radares
        if r["motivacao"] <= 2
    ]

    texto = []

    texto.append("### Análise Executiva da Equipe")
    texto.append("")
    texto.append("#### Médias Gerais")
    texto.append(f"- Motivação média: {round(media_motivacao, 1)}")
    texto.append(f"- Performance média: {round(media_performance, 1)}")
    texto.append(f"- Engajamento médio: {round(media_engajamento, 1)}")
    texto.append(f"- Risco médio: {round(media_risco, 1)}")
    texto.append(f"- Alinhamento médio: {round(media_alinhamento, 1)}")

    texto.append("")
    texto.append("#### Leitura Executiva")

    if media_risco >= 4:
        texto.append("- A equipe apresenta risco médio elevado de desgaste.")
    elif media_risco >= 3:
        texto.append("- Existe atenção moderada para desgaste.")
    else:
        texto.append("- O risco geral da equipe está controlado.")

    if media_performance >= 4:
        texto.append("- A equipe apresenta boa performance geral.")

    if media_motivacao <= 3:
        texto.append("- Recomenda-se reforçar ações de engajamento e reconhecimento.")

    texto.append("")
    texto.append("#### Pontos de Atenção")
    texto.append(f"- Colaboradores com risco elevado: {len(alto_risco)}")
    texto.append(f"- Colaboradores com motivação baixa: {len(motivacao_baixa)}")

    texto.append("")
    texto.append("#### Recomendação")
    texto.append(
        "- Priorizar conversas individuais com colaboradores em risco e acompanhar tendências do radar."
    )

    return "\n".join(texto)