from database.db import SessionLocal
from database.models import RadarColaborador


def criar_radar(dados):

    db = SessionLocal()

    radar = RadarColaborador(**dados)

    db.add(radar)
    db.commit()
    db.refresh(radar)

    db.close()

    return radar


def listar_radares():

    db = SessionLocal()

    radares = (
        db.query(RadarColaborador)
        .order_by(RadarColaborador.data_registro.desc())
        .all()
    )

    lista = []

    for radar in radares:

        nome_colaborador = "-"

        if radar.colaborador:
            nome_colaborador = radar.colaborador.nome

        lista.append(
            {
                "id": radar.id,
                "colaborador_id": radar.colaborador_id,
                "colaborador_nome": nome_colaborador,
                "data_registro": radar.data_registro,
                "motivacao": radar.motivacao,
                "performance": radar.performance,
                "carga_trabalho": radar.carga_trabalho,
                "engajamento": radar.engajamento,
                "risco_desgaste": radar.risco_desgaste,
                "alinhamento_equipe": radar.alinhamento_equipe,
                "observacoes": radar.observacoes
            }
        )

    db.close()

    return lista


def editar_radar(radar_id, dados):

    db = SessionLocal()

    radar = db.query(RadarColaborador).filter(
        RadarColaborador.id == radar_id
    ).first()

    if radar:

        for campo, valor in dados.items():
            setattr(radar, campo, valor)

        db.commit()

    db.close()


def excluir_radar(radar_id):

    db = SessionLocal()

    radar = db.query(RadarColaborador).filter(
        RadarColaborador.id == radar_id
    ).first()

    if radar:
        db.delete(radar)
        db.commit()

    db.close()

def listar_radares_colaborador(colaborador_id):

    radares = listar_radares()

    return [
        radar
        for radar in radares
        if radar["colaborador_id"] == colaborador_id
    ]