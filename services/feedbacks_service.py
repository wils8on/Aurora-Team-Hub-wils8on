from database.db import SessionLocal
from database.models import Feedback


def criar_feedback(dados):

    db = SessionLocal()

    feedback = Feedback(**dados)

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    db.close()

    return feedback


def listar_feedbacks():

    db = SessionLocal()

    feedbacks = (
        db.query(Feedback)
        .order_by(Feedback.data.desc())
        .all()
    )

    lista = []

    for feedback in feedbacks:

        nome_colaborador = "-"

        if feedback.colaborador:
            nome_colaborador = feedback.colaborador.nome

        lista.append(
            {
                "id": feedback.id,
                "colaborador_id": feedback.colaborador_id,
                "colaborador_nome": nome_colaborador,
                "reuniao_id": feedback.reuniao_id,
                "data": feedback.data,
                "origem": feedback.origem,
                "tipo": feedback.tipo,
                "contexto": feedback.contexto,
                "comportamento_observado": feedback.comportamento_observado,
                "impacto_percebido": feedback.impacto_percebido,
                "leitura_gestor": feedback.leitura_gestor,
                "orientacao_dada": feedback.orientacao_dada,
                "reacao_colaborador": feedback.reacao_colaborador,
                "plano_melhoria": feedback.plano_melhoria,
                "data_revisao": feedback.data_revisao,
                "status_acompanhamento": feedback.status_acompanhamento
            }
        )

    db.close()

    return lista


def editar_feedback(feedback_id, dados):

    db = SessionLocal()

    feedback = db.query(Feedback).filter(
        Feedback.id == feedback_id
    ).first()

    if feedback:

        for campo, valor in dados.items():
            setattr(feedback, campo, valor)

        db.commit()

    db.close()


def excluir_feedback(feedback_id):

    db = SessionLocal()

    feedback = db.query(Feedback).filter(
        Feedback.id == feedback_id
    ).first()

    if feedback:
        db.delete(feedback)
        db.commit()

    db.close()