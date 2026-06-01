from datetime import timedelta

from database.db import SessionLocal
from database.models import Colaborador


def criar_colaborador(dados):

    db = SessionLocal()

    novo_colaborador = Colaborador(**dados)

    db.add(novo_colaborador)
    db.commit()
    db.refresh(novo_colaborador)

    db.close()

    return novo_colaborador


def listar_colaboradores():

    db = SessionLocal()

    colaboradores = (
        db.query(Colaborador)
        .order_by(Colaborador.nome)
        .all()
    )

    db.close()

    return colaboradores


def editar_colaborador(colaborador_id, dados):

    db = SessionLocal()

    colaborador = db.query(Colaborador).filter(
        Colaborador.id == colaborador_id
    ).first()

    if colaborador:

        for campo, valor in dados.items():
            setattr(colaborador, campo, valor)

        db.commit()

    db.close()


def excluir_colaborador(colaborador_id):

    db = SessionLocal()

    colaborador = db.query(Colaborador).filter(
        Colaborador.id == colaborador_id
    ).first()

    if colaborador:
        db.delete(colaborador)
        db.commit()

    db.close()


def atualizar_datas_reuniao_colaborador(
    colaborador_id,
    data_reuniao
):

    db = SessionLocal()

    colaborador = db.query(Colaborador).filter(
        Colaborador.id == colaborador_id
    ).first()

    if colaborador:

        colaborador.data_ultima_reuniao = data_reuniao

        frequencia = colaborador.frequencia_1_1

        if frequencia == "Semanal":
            colaborador.proxima_reuniao_recomendada = data_reuniao + timedelta(days=7)

        elif frequencia == "Quinzenal":
            colaborador.proxima_reuniao_recomendada = data_reuniao + timedelta(days=15)

        elif frequencia == "Mensal":
            colaborador.proxima_reuniao_recomendada = data_reuniao + timedelta(days=30)

        else:
            colaborador.proxima_reuniao_recomendada = None

        db.commit()

    db.close()