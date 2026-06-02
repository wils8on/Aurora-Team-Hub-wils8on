def gerar_resumo_colaborador(dados_360):

    radar = dados_360.get("ultimo_radar")
    planos_abertos = dados_360.get("planos_abertos", 0)

    if not radar:

        return {
            "diagnostico": "Sem dados suficientes.",
            "recomendacao": "Registrar informações de radar para gerar análises."
        }

    motivacao = radar.get("motivacao", 0)
    performance = radar.get("performance", 0)
    engajamento = radar.get("engajamento", 0)
    risco = radar.get("risco_desgaste", 0)
    alinhamento = radar.get("alinhamento_equipe", 0)

    observacoes = []

    if performance >= 4:
        observacoes.append(
            "alta performance"
        )

    if motivacao <= 3:
        observacoes.append(
            "motivação moderada ou baixa"
        )

    if engajamento <= 3:
        observacoes.append(
            "engajamento abaixo do ideal"
        )

    if risco >= 4:
        observacoes.append(
            "risco elevado de desgaste"
        )

    if alinhamento >= 4:
        observacoes.append(
            "bom alinhamento com a equipe"
        )

    texto = ", ".join(observacoes)

    recomendacoes = []

    if risco >= 4:
        recomendacoes.append(
            "realizar conversa individual preventiva"
        )

    if motivacao <= 3:
        recomendacoes.append(
            "reforçar reconhecimento e acompanhamento"
        )

    if planos_abertos > 0:
        recomendacoes.append(
            "acompanhar execução dos planos de ação"
        )

    if not recomendacoes:
        recomendacoes.append(
            "manter rotina atual de acompanhamento"
        )

    return {
        "diagnostico": texto.capitalize(),
        "recomendacao": ". ".join(recomendacoes).capitalize()
    }