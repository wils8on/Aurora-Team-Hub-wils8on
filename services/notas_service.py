from database.db import SessionLocal
from database.models import Nota


def criar_nota(dados):

    db = SessionLocal()

    nota = Nota(**dados)

    db.add(nota)
    db.commit()
    db.refresh(nota)

    db.close()

    return nota


def listar_notas():

    db = SessionLocal()

    notas = (
        db.query(Nota)
        .order_by(Nota.data.desc())
        .all()
    )

    lista = []

    for nota in notas:

        colaborador_nome = "-"

        if nota.colaborador:
            colaborador_nome = nota.colaborador.nome

        lista.append(
            {
                "id": nota.id,
                "titulo": nota.titulo,
                "conteudo": nota.conteudo,
                "data": nota.data,
                "categoria": nota.categoria,
                "prioridade": nota.prioridade,
                "tag": nota.tag,
                "colaborador_id": nota.colaborador_id,
                "colaborador_nome": colaborador_nome
            }
        )

    db.close()

    return lista


def editar_nota(nota_id, dados):

    db = SessionLocal()

    nota = (
        db.query(Nota)
        .filter(Nota.id == nota_id)
        .first()
    )

    if nota:

        nota.titulo = dados.get("titulo")
        nota.conteudo = dados.get("conteudo")
        nota.data = dados.get("data")
        nota.categoria = dados.get("categoria")
        nota.prioridade = dados.get("prioridade")
        nota.tag = dados.get("tag")
        nota.colaborador_id = dados.get("colaborador_id")

        db.commit()

    db.close()


def excluir_nota(nota_id):

    db = SessionLocal()

    nota = (
        db.query(Nota)
        .filter(Nota.id == nota_id)
        .first()
    )

    if nota:

        db.delete(nota)
        db.commit()

    db.close()