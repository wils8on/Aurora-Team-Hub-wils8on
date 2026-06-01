from datetime import date

from services.colaboradores_service import listar_colaboradores
from services.reunioes_service import listar_reunioes
from services.feedbacks_service import listar_feedbacks
from services.planos_service import listar_planos
from services.radar_service import listar_radares


def obter_indicadores_dashboard():

    colaboradores = listar_colaboradores()
    reunioes = listar_reunioes()
    feedbacks = listar_feedbacks()
    planos = listar_planos()
    radares = listar_radares()

    hoje = date.today()

    colaboradores_ativos = len(
        [
            c for c in colaboradores
            if c.status == "Ativo"
        ]
    )

    reunioes_mes = len(
        [
            r for r in reunioes
            if r["data"]
            and r["data"].month == hoje.month
            and r["data"].year == hoje.year
        ]
    )

    feedbacks_mes = len(
        [
            f for f in feedbacks
            if f["data"]
            and f["data"].month == hoje.month
            and f["data"].year == hoje.year
        ]
    )

    planos_pendentes = len(
        [
            p for p in planos
            if p["status"] in ["Pendente", "Em andamento"]
        ]
    )

    colaboradores_atencao = len(
        [
            c for c in colaboradores
            if c.risco_percebido in ["Médio", "Alto"]
        ]
    )

    colaboradores_destaque = len(
        [
            c for c in colaboradores
            if c.momento_atual == "Destaque"
        ]
    )

    return {
        "colaboradores_ativos": colaboradores_ativos,
        "reunioes_mes": reunioes_mes,
        "feedbacks_mes": feedbacks_mes,
        "planos_pendentes": planos_pendentes,
        "colaboradores_atencao": colaboradores_atencao,
        "colaboradores_destaque": colaboradores_destaque
    }


def obter_ultimas_reunioes():

    reunioes = listar_reunioes()

    return reunioes[:5]


def obter_ultimos_feedbacks():

    feedbacks = listar_feedbacks()

    return feedbacks[:5]


def obter_planos_pendentes():

    planos = listar_planos()

    return [
        p
        for p in planos
        if p["status"] in ["Pendente", "Em andamento"]
    ][:10]


def obter_radares_recentes():

    radares = listar_radares()

    return radares[:10]