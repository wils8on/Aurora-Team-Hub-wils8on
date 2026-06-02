from datetime import timedelta

from database.db import SessionLocal
from database.models import Colaborador
from database.models import Reuniao
from database.models import Feedback
from database.models import PlanoAcao
from database.models import RadarColaborador
from database.models import Nota
from database.models import EvolucaoColaborador


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


def obter_colaborador_360(colaborador_id):

    from database.models import Reuniao
    from database.models import Feedback
    from database.models import PlanoAcao
    from database.models import RadarColaborador
    from database.models import Nota
    from database.models import EvolucaoColaborador

    db = SessionLocal()

    colaborador = db.query(Colaborador).filter(
        Colaborador.id == colaborador_id
    ).first()

    if not colaborador:
        db.close()
        return None

    dados_colaborador = {
        "id": colaborador.id,
        "nome": colaborador.nome,
        "cargo": colaborador.cargo,
        "status": colaborador.status,
        "momento_atual": colaborador.momento_atual,
        "risco_percebido": colaborador.risco_percebido,
        "data_ultima_reuniao": colaborador.data_ultima_reuniao,
        "proxima_reuniao_recomendada": colaborador.proxima_reuniao_recomendada
    }

    reunioes = (
        db.query(Reuniao)
        .filter(Reuniao.colaborador_id == colaborador_id)
        .order_by(Reuniao.data.desc())
        .all()
    )

    feedbacks = (
        db.query(Feedback)
        .filter(Feedback.colaborador_id == colaborador_id)
        .order_by(Feedback.data.desc())
        .all()
    )

    planos = (
        db.query(PlanoAcao)
        .filter(PlanoAcao.colaborador_id == colaborador_id)
        .order_by(PlanoAcao.prazo.asc())
        .all()
    )

    radares = (
        db.query(RadarColaborador)
        .filter(RadarColaborador.colaborador_id == colaborador_id)
        .order_by(RadarColaborador.data_registro.desc())
        .all()
    )

    notas = (
        db.query(Nota)
        .filter(Nota.colaborador_id == colaborador_id)
        .order_by(Nota.data.desc())
        .all()
    )

    evolucoes = (
        db.query(EvolucaoColaborador)
        .filter(EvolucaoColaborador.colaborador_id == colaborador_id)
        .order_by(EvolucaoColaborador.data.desc())
        .all()
    )

    resultado = {
        "colaborador": dados_colaborador,
        "reunioes": [
            {
                "id": item.id,
                "data": item.data,
                "tipo": item.tipo,
                "status": item.status,
                "assunto_principal": item.assunto_principal,
                "resumo_final": item.resumo_final
            }
            for item in reunioes
        ],
        "feedbacks": [
            {
                "id": item.id,
                "data": item.data,
                "tipo": item.tipo,
                "origem": item.origem,
                "status_acompanhamento": item.status_acompanhamento,
                "contexto": item.contexto
            }
            for item in feedbacks
        ],
        "planos": [
            {
                "id": item.id,
                "titulo": item.titulo,
                "prazo": item.prazo,
                "prioridade": item.prioridade,
                "status": item.status
            }
            for item in planos
        ],
        "radares": [
            {
                "id": item.id,
                "data_registro": item.data_registro,
                "motivacao": item.motivacao,
                "performance": item.performance,
                "engajamento": item.engajamento,
                "risco_desgaste": item.risco_desgaste,
                "alinhamento_equipe": item.alinhamento_equipe
            }
            for item in radares
        ],
        "notas": [
            {
                "id": item.id,
                "data": item.data,
                "titulo": item.titulo,
                "categoria": item.categoria,
                "prioridade": item.prioridade,
                "conteudo": item.conteudo
            }
            for item in notas
        ],
        "evolucoes": [
            {
                "id": item.id,
                "data": item.data,
                "tipo_evolucao": item.tipo_evolucao,
                "cargo_anterior": item.cargo_anterior,
                "cargo_novo": item.cargo_novo,
                "contrato_anterior": item.contrato_anterior,
                "contrato_novo": item.contrato_novo,
                "motivo": item.motivo
            }
            for item in evolucoes
        ]
    }

    db.close()

    return resultado

def obter_colaborador_360(colaborador_id):

    db = SessionLocal()

    colaborador = db.query(Colaborador).filter(
        Colaborador.id == colaborador_id
    ).first()

    if not colaborador:
        db.close()
        return None

    dados_colaborador = {
        "id": colaborador.id,
        "nome": colaborador.nome,
        "nome_social": colaborador.nome_social,
        "cargo": colaborador.cargo,
        "email": colaborador.email,
        "email_pessoal": colaborador.email_pessoal,
        "telefone": colaborador.telefone,
        "telefone_pessoal": colaborador.telefone_pessoal,
        "unidade": colaborador.unidade,
        "data_admissao": colaborador.data_admissao,
        "data_aniversario": colaborador.data_aniversario,
        "tipo_contrato": colaborador.tipo_contrato,
        "gestor_direto": colaborador.gestor_direto,
        "area_equipe": colaborador.area_equipe,
        "status": colaborador.status,
        "frequencia_1_1": colaborador.frequencia_1_1,
        "data_ultima_reuniao": colaborador.data_ultima_reuniao,
        "proxima_reuniao_recomendada": colaborador.proxima_reuniao_recomendada,
        "satisfacao_percebida": colaborador.satisfacao_percebida,
        "risco_percebido": colaborador.risco_percebido,
        "momento_atual": colaborador.momento_atual,
        "observacoes_gerais": colaborador.observacoes_gerais
    }

    reunioes = (
        db.query(Reuniao)
        .filter(Reuniao.colaborador_id == colaborador_id)
        .order_by(Reuniao.data.desc())
        .all()
    )

    feedbacks = (
        db.query(Feedback)
        .filter(Feedback.colaborador_id == colaborador_id)
        .order_by(Feedback.data.desc())
        .all()
    )

    planos = (
        db.query(PlanoAcao)
        .filter(PlanoAcao.colaborador_id == colaborador_id)
        .order_by(PlanoAcao.prazo.asc())
        .all()
    )

    radares = (
        db.query(RadarColaborador)
        .filter(RadarColaborador.colaborador_id == colaborador_id)
        .order_by(RadarColaborador.data_registro.desc())
        .all()
    )

    notas = (
        db.query(Nota)
        .filter(Nota.colaborador_id == colaborador_id)
        .order_by(Nota.data.desc())
        .all()
    )

    evolucoes = (
        db.query(EvolucaoColaborador)
        .filter(EvolucaoColaborador.colaborador_id == colaborador_id)
        .order_by(EvolucaoColaborador.data.desc())
        .all()
    )

    resultado = {
        "colaborador": dados_colaborador,
        "reunioes": [
            {
                "id": r.id,
                "data": r.data,
                "tipo": r.tipo,
                "status": r.status,
                "assunto_principal": r.assunto_principal,
                "resumo_final": r.resumo_final
            }
            for r in reunioes
        ],
        "feedbacks": [
            {
                "id": f.id,
                "data": f.data,
                "tipo": f.tipo,
                "origem": f.origem,
                "status_acompanhamento": f.status_acompanhamento,
                "contexto": f.contexto
            }
            for f in feedbacks
        ],
        "planos": [
            {
                "id": p.id,
                "titulo": p.titulo,
                "prazo": p.prazo,
                "prioridade": p.prioridade,
                "status": p.status
            }
            for p in planos
        ],
        "radares": [
            {
                "id": r.id,
                "data_registro": r.data_registro,
                "motivacao": r.motivacao,
                "performance": r.performance,
                "engajamento": r.engajamento,
                "risco_desgaste": r.risco_desgaste,
                "alinhamento_equipe": r.alinhamento_equipe
            }
            for r in radares
        ],
        "notas": [
            {
                "id": n.id,
                "data": n.data,
                "titulo": n.titulo,
                "categoria": n.categoria,
                "prioridade": n.prioridade,
                "conteudo": n.conteudo
            }
            for n in notas
        ],
        "evolucoes": [
            {
                "id": e.id,
                "data": e.data,
                "tipo_evolucao": e.tipo_evolucao,
                "cargo_anterior": e.cargo_anterior,
                "cargo_novo": e.cargo_novo,
                "contrato_anterior": e.contrato_anterior,
                "contrato_novo": e.contrato_novo,
                "motivo": e.motivo
            }
            for e in evolucoes
        ]
    }

    db.close()

    return resultado