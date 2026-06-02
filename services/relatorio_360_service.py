from datetime import date
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def limpar_texto(valor):

    if valor is None:
        return "-"

    valor = str(valor).strip()

    if not valor:
        return "-"

    return valor


def formatar_data_pdf(valor):

    if not valor:
        return "-"

    try:
        return valor.strftime("%d/%m/%Y")
    except AttributeError:
        return limpar_texto(valor)


def calcular_tempo_casa(data_admissao):

    if not data_admissao:
        return "-"

    dias = (date.today() - data_admissao).days

    if dias < 0:
        return "-"

    anos = dias // 365
    meses = (dias % 365) // 30

    return f"{anos}a {meses}m"


def adicionar_titulo(elementos, texto, estilos):

    elementos.append(Paragraph(texto, estilos["Secao"]))
    elementos.append(Spacer(1, 0.15 * cm))


def criar_tabela(dados, largura_colunas=None):

    tabela = Table(dados, colWidths=largura_colunas)

    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CCCCCC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    return tabela


def criar_tabela_chave_valor(dados):

    tabela = Table(dados, colWidths=[4.2 * cm, 11.8 * cm])

    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8EEF7")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1F4E79")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CCCCCC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    return tabela


def gerar_pdf_colaborador_360(dados_360):

    buffer = BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    estilos = getSampleStyleSheet()

    estilos.add(
        ParagraphStyle(
            name="TituloCustom",
            parent=estilos["Title"],
            fontSize=18,
            leading=22,
            spaceAfter=14
        )
    )

    estilos.add(
        ParagraphStyle(
            name="Subtitulo",
            parent=estilos["Normal"],
            fontSize=9,
            leading=12,
            alignment=1,
            textColor=colors.HexColor("#666666"),
            spaceAfter=12
        )
    )

    estilos.add(
        ParagraphStyle(
            name="Secao",
            parent=estilos["Heading2"],
            fontSize=12,
            leading=15,
            spaceBefore=10,
            spaceAfter=6,
            textColor=colors.HexColor("#1F4E79")
        )
    )

    elementos = []

    colab = dados_360["colaborador"]
    reunioes = dados_360["reunioes"]
    feedbacks = dados_360["feedbacks"]
    planos = dados_360["planos"]
    radares = dados_360["radares"]
    notas = dados_360["notas"]
    evolucoes = dados_360["evolucoes"]

    ultima_reuniao = reunioes[0]["data"] if reunioes else None
    ultimo_feedback = feedbacks[0]["data"] if feedbacks else None
    ultimo_radar = radares[0] if radares else None

    planos_abertos = [
        plano for plano in planos
        if plano["status"] in ["Pendente", "Em andamento"]
    ]

    elementos.append(Paragraph("Relatório 360° do Colaborador", estilos["TituloCustom"]))
    elementos.append(
        Paragraph(
            f"Gerado em {date.today().strftime('%d/%m/%Y')} pelo Aurora Team Hub",
            estilos["Subtitulo"]
        )
    )

    adicionar_titulo(elementos, "1. Dados Cadastrais", estilos)

    dados_cadastrais = [
        ["Nome", limpar_texto(colab.get("nome"))],
        ["Cargo", limpar_texto(colab.get("cargo"))],
        ["Status", limpar_texto(colab.get("status"))],
        ["Unidade", limpar_texto(colab.get("unidade"))],
        ["Tipo de contrato", limpar_texto(colab.get("tipo_contrato"))],
        ["Gestor direto", limpar_texto(colab.get("gestor_direto"))],
        ["Data de admissão", formatar_data_pdf(colab.get("data_admissao"))],
        ["Tempo de casa", calcular_tempo_casa(colab.get("data_admissao"))],
        ["Momento atual", limpar_texto(colab.get("momento_atual"))],
        ["Risco percebido", limpar_texto(colab.get("risco_percebido"))],
    ]

    elementos.append(criar_tabela_chave_valor(dados_cadastrais))
    elementos.append(Spacer(1, 0.35 * cm))

    adicionar_titulo(elementos, "2. Resumo Executivo", estilos)

    resumo = [
        ["Indicador", "Valor"],
        ["Última reunião", formatar_data_pdf(ultima_reuniao)],
        ["Último feedback", formatar_data_pdf(ultimo_feedback)],
        ["Planos abertos", limpar_texto(len(planos_abertos))],
        ["Próxima 1:1", formatar_data_pdf(colab.get("proxima_reuniao_recomendada"))],
        ["Risco radar", limpar_texto(ultimo_radar.get("risco_desgaste") if ultimo_radar else "-")],
    ]

    elementos.append(criar_tabela(resumo, [6 * cm, 10 * cm]))
    elementos.append(Spacer(1, 0.35 * cm))

    adicionar_titulo(elementos, "3. Saúde Atual", estilos)

    if ultimo_radar:
        saude = [
            ["Motivação", "Performance", "Engajamento", "Risco", "Alinhamento"],
            [
                limpar_texto(ultimo_radar.get("motivacao")),
                limpar_texto(ultimo_radar.get("performance")),
                limpar_texto(ultimo_radar.get("engajamento")),
                limpar_texto(ultimo_radar.get("risco_desgaste")),
                limpar_texto(ultimo_radar.get("alinhamento_equipe")),
            ]
        ]
        elementos.append(criar_tabela(saude, [3.2 * cm] * 5))
    else:
        elementos.append(Paragraph("Sem registro de radar.", estilos["Normal"]))

    elementos.append(Spacer(1, 0.35 * cm))

    adicionar_titulo(elementos, "4. Últimas Reuniões", estilos)

    tabela_reunioes = [["Data", "Tipo", "Status", "Assunto"]]

    for item in reunioes[:10]:
        tabela_reunioes.append(
            [
                formatar_data_pdf(item.get("data")),
                limpar_texto(item.get("tipo")),
                limpar_texto(item.get("status")),
                limpar_texto(item.get("assunto_principal")),
            ]
        )

    elementos.append(criar_tabela(tabela_reunioes, [2.5 * cm, 3 * cm, 3 * cm, 7.5 * cm]))
    elementos.append(Spacer(1, 0.35 * cm))

    adicionar_titulo(elementos, "5. Últimos Feedbacks", estilos)

    tabela_feedbacks = [["Data", "Tipo", "Origem", "Status"]]

    for item in feedbacks[:10]:
        tabela_feedbacks.append(
            [
                formatar_data_pdf(item.get("data")),
                limpar_texto(item.get("tipo")),
                limpar_texto(item.get("origem")),
                limpar_texto(item.get("status_acompanhamento")),
            ]
        )

    elementos.append(criar_tabela(tabela_feedbacks, [2.5 * cm, 4 * cm, 4 * cm, 5.5 * cm]))
    elementos.append(Spacer(1, 0.35 * cm))

    adicionar_titulo(elementos, "6. Planos de Ação", estilos)

    tabela_planos = [["Prazo", "Título", "Prioridade", "Status"]]

    for item in planos[:10]:
        tabela_planos.append(
            [
                formatar_data_pdf(item.get("prazo")),
                limpar_texto(item.get("titulo")),
                limpar_texto(item.get("prioridade")),
                limpar_texto(item.get("status")),
            ]
        )

    elementos.append(criar_tabela(tabela_planos, [2.5 * cm, 7 * cm, 3 * cm, 3.5 * cm]))
    elementos.append(Spacer(1, 0.35 * cm))

    adicionar_titulo(elementos, "7. Evoluções", estilos)

    tabela_evolucoes = [["Data", "Tipo", "Cargo anterior", "Novo cargo"]]

    for item in evolucoes[:10]:
        tabela_evolucoes.append(
            [
                formatar_data_pdf(item.get("data")),
                limpar_texto(item.get("tipo_evolucao")),
                limpar_texto(item.get("cargo_anterior")),
                limpar_texto(item.get("cargo_novo")),
            ]
        )

    elementos.append(criar_tabela(tabela_evolucoes, [2.5 * cm, 4.5 * cm, 4.5 * cm, 4.5 * cm]))
    elementos.append(Spacer(1, 0.35 * cm))

    adicionar_titulo(elementos, "8. Notas Gerenciais", estilos)

    tabela_notas = [["Data", "Título", "Categoria", "Prioridade"]]

    for item in notas[:10]:
        tabela_notas.append(
            [
                formatar_data_pdf(item.get("data")),
                limpar_texto(item.get("titulo")),
                limpar_texto(item.get("categoria")),
                limpar_texto(item.get("prioridade")),
            ]
        )

    elementos.append(criar_tabela(tabela_notas, [2.5 * cm, 6.5 * cm, 3.5 * cm, 3.5 * cm]))

    documento.build(elementos)

    buffer.seek(0)
    return buffer.getvalue()
