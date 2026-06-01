from database.db import SessionLocal
from database.models import EvolucaoColaborador
from database.models import Colaborador


def criar_evolucao(dados):

    db = SessionLocal()

    evolucao = EvolucaoColaborador(**dados)

    db.add(evolucao)

    colaborador = db.query(Colaborador).filter(
        Colaborador.id == dados["colaborador_id"]
    ).first()

    if colaborador:

        novo_cargo = dados.get("cargo_novo")
        novo_contrato = dados.get("contrato_novo")

        if novo_cargo:
            colaborador.cargo = novo_cargo

        if novo_contrato:
            colaborador.tipo_contrato = novo_contrato

    db.commit()
    db.refresh(evolucao)

    db.close()

    return evolucao


def listar_evolucoes_colaborador(colaborador_id):

    db = SessionLocal()

    evolucoes = (
        db.query(EvolucaoColaborador)
        .filter(EvolucaoColaborador.colaborador_id == colaborador_id)
        .order_by(EvolucaoColaborador.data.desc())
        .all()
    )

    lista = []

    for evolucao in evolucoes:
        lista.append(
            {
                "id": evolucao.id,
                "data": evolucao.data,
                "tipo_evolucao": evolucao.tipo_evolucao,
                "cargo_anterior": evolucao.cargo_anterior,
                "cargo_novo": evolucao.cargo_novo,
                "contrato_anterior": evolucao.contrato_anterior,
                "contrato_novo": evolucao.contrato_novo,
                "motivo": evolucao.motivo,
                "observacoes": evolucao.observacoes
            }
        )

    db.close()

    return lista