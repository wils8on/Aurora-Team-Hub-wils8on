from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from database.db import Base


class Colaborador(Base):

    __tablename__ = "colaboradores"

    id = Column(Integer, primary_key=True)

    nome = Column(String)
    nome_social = Column(String)
    data_aniversario = Column(Date)

    cargo = Column(String)
    email = Column(String)
    telefone = Column(String)
    email_pessoal = Column(String)
    telefone_pessoal = Column(String)

    unidade = Column(String)

    data_admissao = Column(Date)

    tipo_contrato = Column(String)
    gestor_direto = Column(String)
    area_equipe = Column(String)

    status = Column(String)

    principais_responsabilidades = Column(String)
    projetos_atuais = Column(String)
    prioridades_atuais = Column(String)
    entregas_responsabilidade = Column(String)
    observacoes_operacionais = Column(String)

    pontos_fortes = Column(String)
    pontos_desenvolvimento = Column(String)
    perfil_comportamental = Column(String)
    interesses_desenvolvimento = Column(String)
    objetivos_profissionais = Column(String)
    competencias_desenvolver = Column(String)

    frequencia_1_1 = Column(String)

    data_ultima_reuniao = Column(Date)
    proxima_reuniao_recomendada = Column(Date)

    satisfacao_percebida = Column(String)
    risco_percebido = Column(String)
    momento_atual = Column(String)

    observacoes_gerais = Column(String)

    reunioes = relationship(
        "Reuniao",
        back_populates="colaborador"
    )

    feedbacks = relationship(
        "Feedback",
        back_populates="colaborador"
    )

    evolucoes = relationship(
        "EvolucaoColaborador",
        back_populates="colaborador"
    )

    planos_acao = relationship(
        "PlanoAcao",
        back_populates="colaborador"
    )

    feedbacks = relationship(
        "Feedback",
        back_populates="colaborador"
    )

    radares = relationship(
        "RadarColaborador",
        back_populates="colaborador"
    )


class Reuniao(Base):

    __tablename__ = "reunioes"

    id = Column(Integer, primary_key=True)

    colaborador_id = Column(
        Integer,
        ForeignKey("colaboradores.id")
    )

    data = Column(Date)

    tipo = Column(String)

    status = Column(String)

    formato = Column(String)

    assunto_principal = Column(String)

    pauta = Column(String)

    humor_percebido = Column(String)

    situacao_atual = Column(String)

    dificuldades_relatadas = Column(String)

    pontos_positivos = Column(String)

    feedback_recebido = Column(String)

    feedback_dado = Column(String)

    decisoes_tomadas = Column(String)

    combinados = Column(String)

    proximos_passos = Column(String)

    resumo_final = Column(String)

    follow_up = Column(String)

    prioridade = Column(String)

    colaborador = relationship(
        "Colaborador",
        back_populates="reunioes"
    )


class Feedback(Base):

    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True)

    colaborador_id = Column(
        Integer,
        ForeignKey("colaboradores.id")
    )

    reuniao_id = Column(
        Integer,
        ForeignKey("reunioes.id"),
        nullable=True
    )

    data = Column(Date)

    origem = Column(String)

    tipo = Column(String)

    contexto = Column(String)

    comportamento_observado = Column(String)

    impacto_percebido = Column(String)

    leitura_gestor = Column(String)

    orientacao_dada = Column(String)

    reacao_colaborador = Column(String)

    plano_melhoria = Column(String)

    data_revisao = Column(Date)

    status_acompanhamento = Column(String)

    colaborador = relationship(
        "Colaborador",
        back_populates="feedbacks"
    )

class EvolucaoColaborador(Base):

    __tablename__ = "evolucoes_colaborador"

    id = Column(Integer, primary_key=True)

    colaborador_id = Column(
        Integer,
        ForeignKey("colaboradores.id")
    )

    data = Column(Date)

    tipo_evolucao = Column(String)

    cargo_anterior = Column(String)
    cargo_novo = Column(String)

    contrato_anterior = Column(String)
    contrato_novo = Column(String)

    motivo = Column(String)
    observacoes = Column(String)

    colaborador = relationship(
        "Colaborador",
        back_populates="evolucoes"
    )

class PlanoAcao(Base):

    __tablename__ = "planos_acao"

    id = Column(Integer, primary_key=True)

    colaborador_id = Column(
        Integer,
        ForeignKey("colaboradores.id")
    )

    titulo = Column(String)
    descricao = Column(String)

    origem = Column(String)

    data_criacao = Column(Date)
    prazo = Column(Date)

    prioridade = Column(String)
    status = Column(String)

    observacoes_progresso = Column(String)

    data_conclusao = Column(Date)

    colaborador = relationship(
        "Colaborador",
        back_populates="planos_acao"
    )

class RadarColaborador(Base):

    __tablename__ = "radar_colaborador"

    id = Column(Integer, primary_key=True)

    colaborador_id = Column(
        Integer,
        ForeignKey("colaboradores.id")
    )

    data_registro = Column(Date)

    motivacao = Column(Integer)
    performance = Column(Integer)
    carga_trabalho = Column(Integer)
    engajamento = Column(Integer)
    risco_desgaste = Column(Integer)
    alinhamento_equipe = Column(Integer)

    observacoes = Column(String)

    colaborador = relationship(
        "Colaborador",
        back_populates="radares"
    )

class Nota(Base):

    __tablename__ = "notas"

    id = Column(Integer, primary_key=True)

    titulo = Column(String)

    conteudo = Column(String)

    data = Column(Date)

    categoria = Column(String)

    colaborador_id = Column(
        Integer,
        ForeignKey("colaboradores.id"),
        nullable=True
    )

    prioridade = Column(String)

    tag = Column(String)

    colaborador = relationship("Colaborador")