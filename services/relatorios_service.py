from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors


def limpar_texto(valor):
    if valor is None:
        return "-"
    valor = str(valor).strip()
    if not valor:
        return "-"
    return valor


def adicionar_secao(elementos, titulo, conteudo, estilos):
    elementos.append(Paragraph(titulo, estilos["Secao"]))
    elementos.append(
        Paragraph(
            limpar_texto(conteudo).replace("\n", "<br/>"),
            estilos["NormalCustom"]
        )
    )
    elementos.append(Spacer(1, 0.35 * cm))


def gerar_pdf_reuniao(reuniao):
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
            name="Secao",
            parent=estilos["Heading2"],
            fontSize=12,
            leading=15,
            spaceBefore=10,
            spaceAfter=6,
            textColor=colors.HexColor("#1F4E79")
        )
    )

    estilos.add(
        ParagraphStyle(
            name="NormalCustom",
            parent=estilos["Normal"],
            fontSize=10,
            leading=14
        )
    )

    elementos = []

    elementos.append(Paragraph("Relatório de Reunião", estilos["TituloCustom"]))

    dados_cabecalho = [
        ["Colaborador", limpar_texto(reuniao.get("colaborador_nome"))],
        ["Data", limpar_texto(reuniao.get("data"))],
        ["Tipo", limpar_texto(reuniao.get("tipo"))],
        ["Status", limpar_texto(reuniao.get("status"))],
        ["Formato", limpar_texto(reuniao.get("formato"))],
        ["Prioridade", limpar_texto(reuniao.get("prioridade"))],
        ["Follow-up", limpar_texto(reuniao.get("follow_up"))],
    ]

    tabela = Table(dados_cabecalho, colWidths=[4 * cm, 12 * cm])

    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8EEF7")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1F4E79")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CCCCCC")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elementos.append(tabela)
    elementos.append(Spacer(1, 0.4 * cm))

    secoes = [
        ("Assunto principal", "assunto_principal"),
        ("Pauta", "pauta"),
        ("Resumo final", "resumo_final"),
        ("Situação atual", "situacao_atual"),
        ("Dificuldades relatadas", "dificuldades_relatadas"),
        ("Pontos positivos", "pontos_positivos"),
        ("Feedback recebido pelo gestor", "feedback_recebido"),
        ("Feedback dado ao colaborador", "feedback_dado"),
        ("Decisões tomadas", "decisoes_tomadas"),
        ("Combinados", "combinados"),
        ("Próximos passos", "proximos_passos"),
    ]

    for titulo, campo in secoes:
        adicionar_secao(elementos, titulo, reuniao.get(campo), estilos)

    documento.build(elementos)

    buffer.seek(0)
    return buffer.getvalue()
