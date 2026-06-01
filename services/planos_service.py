from database.db import SessionLocal
from database.models import PlanoAcao


def criar_plano(dados):

    db = SessionLocal()

    plano = PlanoAcao(**dados)

    db.add(plano)
    db.commit()
    db.refresh(plano)

    db.close()

    return plano


def listar_planos():

    db = SessionLocal()

    planos = (
        db.query(PlanoAcao)
        .order_by(PlanoAcao.prazo.asc())
        .all()
    )

    lista = []

    for plano in planos:

        nome_colaborador = "-"

        if plano.colaborador:
            nome_colaborador = plano.colaborador.nome

        lista.append(
            {
                "id": plano.id,
                "colaborador_id": plano.colaborador_id,
                "colaborador_nome": nome_colaborador,
                "titulo": plano.titulo,
                "descricao": plano.descricao,
                "origem": plano.origem,
                "data_criacao": plano.data_criacao,
                "prazo": plano.prazo,
                "prioridade": plano.prioridade,
                "status": plano.status,
                "observacoes_progresso": plano.observacoes_progresso,
                "data_conclusao": plano.data_conclusao
            }
        )

    db.close()

    return lista


def editar_plano(plano_id, dados):

    db = SessionLocal()

    plano = db.query(PlanoAcao).filter(
        PlanoAcao.id == plano_id
    ).first()

    if plano:

        for campo, valor in dados.items():
            setattr(plano, campo, valor)

        db.commit()

    db.close()


def excluir_plano(plano_id):

    db = SessionLocal()

    plano = db.query(PlanoAcao).filter(
        PlanoAcao.id == plano_id
    ).first()

    if plano:
        db.delete(plano)
        db.commit()

    db.close()