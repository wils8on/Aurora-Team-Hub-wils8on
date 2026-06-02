from services.radar_service import listar_radares


def gerar_insight_radar(radar):

    insights = []

    motivacao = radar.get("motivacao") or 0
    performance = radar.get("performance") or 0
    engajamento = radar.get("engajamento") or 0
    risco = radar.get("risco_desgaste") or 0
    alinhamento = radar.get("alinhamento_equipe") or 0
    carga = radar.get("carga_trabalho") or 0

    if performance >= 4 and motivacao <= 3:
        insights.append(
            {
                "nivel": "Atenção",
                "mensagem": "Alta performance com motivação moderada ou baixa. Pode indicar esforço elevado sem energia proporcional.",
                "recomendacao": "Realizar 1:1 focada em reconhecimento, carga de trabalho e expectativas."
            }
        )

    if engajamento <= 2:
        insights.append(
            {
                "nivel": "Atenção",
                "mensagem": "Engajamento baixo identificado.",
                "recomendacao": "Investigar alinhamento, clareza de papel, motivadores e possíveis bloqueios."
            }
        )

    if risco >= 4:
        insights.append(
            {
                "nivel": "Crítico",
                "mensagem": "Risco de desgaste elevado.",
                "recomendacao": "Priorizar conversa individual e avaliar redistribuição de demandas."
            }
        )

    if carga >= 4 and risco >= 4:
        insights.append(
            {
                "nivel": "Crítico",
                "mensagem": "Carga de trabalho alta combinada com risco elevado.",
                "recomendacao": "Mapear demandas urgentes, reduzir sobrecarga e acompanhar semanalmente."
            }
        )

    if motivacao >= 4 and performance >= 4 and engajamento >= 4:
        insights.append(
            {
                "nivel": "Positivo",
                "mensagem": "Colaborador em momento positivo, com bons sinais de motivação, performance e engajamento.",
                "recomendacao": "Manter acompanhamento e considerar novas oportunidades de desenvolvimento."
            }
        )

    if alinhamento <= 2:
        insights.append(
            {
                "nivel": "Atenção",
                "mensagem": "Alinhamento com a equipe abaixo do esperado.",
                "recomendacao": "Promover alinhamento de expectativas, comunicação e integração com o time."
            }
        )

    if not insights:
        insights.append(
            {
                "nivel": "Estável",
                "mensagem": "Sem sinais críticos identificados no radar atual.",
                "recomendacao": "Manter acompanhamento regular."
            }
        )

    return insights


def gerar_insights_dashboard():

    radares = listar_radares()

    ultimos_por_colaborador = {}

    for radar in radares:
        colaborador_id = radar["colaborador_id"]

        if colaborador_id not in ultimos_por_colaborador:
            ultimos_por_colaborador[colaborador_id] = radar

    insights_dashboard = []

    for radar in ultimos_por_colaborador.values():

        insights = gerar_insight_radar(radar)

        for insight in insights:
            insights_dashboard.append(
                {
                    "colaborador_nome": radar["colaborador_nome"],
                    "data_registro": radar["data_registro"],
                    "nivel": insight["nivel"],
                    "mensagem": insight["mensagem"],
                    "recomendacao": insight["recomendacao"],
                    "risco_desgaste": radar["risco_desgaste"],
                    "motivacao": radar["motivacao"],
                    "performance": radar["performance"],
                    "engajamento": radar["engajamento"]
                }
            )

    ordem = {
        "Crítico": 1,
        "Atenção": 2,
        "Estável": 3,
        "Positivo": 4
    }

    insights_dashboard = sorted(
        insights_dashboard,
        key=lambda item: ordem.get(item["nivel"], 99)
    )

    return insights_dashboard[:10]


def gerar_insight_colaborador(colaborador_id):

    radares = listar_radares()

    radares_colaborador = [
        radar for radar in radares
        if radar["colaborador_id"] == colaborador_id
    ]

    if not radares_colaborador:
        return []

    ultimo_radar = radares_colaborador[0]

    return gerar_insight_radar(ultimo_radar)