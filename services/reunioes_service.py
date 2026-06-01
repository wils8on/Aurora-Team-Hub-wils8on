from database.db import SessionLocal
from database.models import Reuniao


def criar_reuniao(dados):

    db = SessionLocal()

    reuniao = Reuniao(**dados)

    db.add(reuniao)
    db.commit()
    db.refresh(reuniao)

    db.close()

    return reuniao


def listar_reunioes():

    db = SessionLocal()

    reunioes = (
        db.query(Reuniao)
        .order_by(Reuniao.data.desc())
        .all()
    )

    lista = []

    for reuniao in reunioes:

        nome_colaborador = "-"

        if reuniao.colaborador:
            nome_colaborador = reuniao.colaborador.nome

        lista.append(
            {
                "id": reuniao.id,
                "colaborador_id": reuniao.colaborador_id,
                "colaborador_nome": nome_colaborador,
                "data": reuniao.data,
                "tipo": reuniao.tipo,
                "status": reuniao.status,
                "formato": reuniao.formato,
                "assunto_principal": reuniao.assunto_principal,
                "pauta": reuniao.pauta,
                "humor_percebido": reuniao.humor_percebido,
                "situacao_atual": reuniao.situacao_atual,
                "dificuldades_relatadas": reuniao.dificuldades_relatadas,
                "pontos_positivos": reuniao.pontos_positivos,
                "feedback_recebido": reuniao.feedback_recebido,
                "feedback_dado": reuniao.feedback_dado,
                "decisoes_tomadas": reuniao.decisoes_tomadas,
                "combinados": reuniao.combinados,
                "proximos_passos": reuniao.proximos_passos,
                "resumo_final": reuniao.resumo_final,
                "follow_up": reuniao.follow_up,
                "prioridade": reuniao.prioridade
            }
        )

    db.close()

    return lista


def editar_reuniao(reuniao_id, dados):

    db = SessionLocal()

    reuniao = db.query(Reuniao).filter(
        Reuniao.id == reuniao_id
    ).first()

    if reuniao:

        for campo, valor in dados.items():
            setattr(reuniao, campo, valor)

        db.commit()

    db.close()


def excluir_reuniao(reuniao_id):

    db = SessionLocal()

    reuniao = db.query(Reuniao).filter(
        Reuniao.id == reuniao_id
    ).first()

    if reuniao:
        db.delete(reuniao)
        db.commit()

    db.close()