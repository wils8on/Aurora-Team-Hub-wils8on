from datetime import date, timedelta

from services.colaboradores_service import listar_colaboradores
from services.reunioes_service import listar_reunioes
from services.feedbacks_service import listar_feedbacks
from services.planos_service import listar_planos
from services.radar_service import listar_radares


def obter_dados_base():
    return {
        "colaboradores": listar_colaboradores(),
        "reunioes": listar_reunioes(),
        "feedbacks": listar_feedbacks(),
        "planos": listar_planos(),
        "radares": listar_radares()
    }


def obter_indicadores_dashboard():

    dados = obter_dados_base()
    hoje = date.today()
    limite_30_dias = hoje - timedelta(days=30)

    colaboradores = dados["colaboradores"]
    reunioes = dados["reunioes"]
    feedbacks = dados["feedbacks"]
    planos = dados["planos"]
    radares = dados["radares"]

    return {
        "colaboradores_ativos": len([c for c in colaboradores if c.status == "Ativo"]),
        "reunioes_30_dias": len([r for r in reunioes if r["data"] and r["data"] >= limite_30_dias]),
        "feedbacks_abertos": len([f for f in feedbacks if f["status_acompanhamento"] in ["Aberto", "Em acompanhamento"]]),
        "planos_andamento": len([p for p in planos if p["status"] in ["Pendente", "Em andamento"]]),
        "planos_atrasados": len([p for p in planos if p["prazo"] and p["prazo"] < hoje and p["status"] not in ["Concluído", "Cancelado"]]),
        "radares_30_dias": len([r for r in radares if r["data_registro"] and r["data_registro"] >= limite_30_dias]),
    }


def obter_alertas_dashboard():

    dados = obter_dados_base()
    hoje = date.today()

    alertas = []

    for colaborador in dados["colaboradores"]:

        if colaborador.status != "Ativo":
            continue

        if colaborador.data_ultima_reuniao:
            dias_sem_1_1 = (hoje - colaborador.data_ultima_reuniao).days

            if dias_sem_1_1 >= 30:
                alertas.append(
                    f"{colaborador.nome} está há {dias_sem_1_1} dias sem 1:1."
                )
        else:
            alertas.append(
                f"{colaborador.nome} ainda não possui 1:1 registrada."
            )

        if colaborador.risco_percebido == "Alto":
            alertas.append(
                f"{colaborador.nome} está com risco percebido alto."
            )

    for plano in dados["planos"]:

        if plano["prazo"] and plano["prazo"] < hoje and plano["status"] not in ["Concluído", "Cancelado"]:
            alertas.append(
                f"Plano atrasado: {plano['titulo']} — {plano['colaborador_nome']}."
            )

    for radar in dados["radares"]:

        if radar["risco_desgaste"] == 5:
            alertas.append(
                f"{radar['colaborador_nome']} registrou risco de desgaste 5 no radar."
            )

    return alertas[:10]


def obter_saude_equipe():

    radares = listar_radares()

    if not radares:
        return None

    return {
        "motivacao": round(sum(r["motivacao"] for r in radares) / len(radares), 2),
        "performance": round(sum(r["performance"] for r in radares) / len(radares), 2),
        "engajamento": round(sum(r["engajamento"] for r in radares) / len(radares), 2),
        "risco": round(sum(r["risco_desgaste"] for r in radares) / len(radares), 2),
        "alinhamento": round(sum(r["alinhamento_equipe"] for r in radares) / len(radares), 2),
    }


def obter_ultimas_reunioes():
    return listar_reunioes()[:5]


def obter_ultimos_feedbacks():
    return listar_feedbacks()[:5]


def obter_planos_pendentes():
    return [
        p for p in listar_planos()
        if p["status"] in ["Pendente", "Em andamento"]
    ][:10]


def obter_radares_recentes():
    return listar_radares()[:10]