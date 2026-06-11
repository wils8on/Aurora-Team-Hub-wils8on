from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
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

def gerar_pdf_pauta_reuniao(reuniao):

    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from io import BytesIO

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    largura, altura = A4
    y = altura - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Pauta da Reunião")
    y -= 40

    pdf.setFont("Helvetica", 11)

    campos = [
        ("Colaborador", reuniao.get("colaborador_nome", "-")),
        ("Data", str(reuniao.get("data", "-"))),
        ("Tipo", reuniao.get("tipo", "-")),
        ("Formato", reuniao.get("formato", "-")),
        ("Assunto", reuniao.get("assunto_principal", "-")),
        ("Pauta", reuniao.get("pauta", "-")),
        ("Prioridade", reuniao.get("prioridade", "-")),
        ("Follow-up", reuniao.get("follow_up", "-")),
    ]

    for titulo, valor in campos:
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(50, y, f"{titulo}:")
        y -= 16

        pdf.setFont("Helvetica", 10)

        texto = str(valor or "-")

        for linha in texto.split("\n"):
            pdf.drawString(70, y, linha[:95])
            y -= 14

            if y < 60:
                pdf.showPage()
                y = altura - 50

        y -= 10

    pdf.save()
    buffer.seek(0)

    return buffer.getvalue()

def gerar_pdf_feedback(feedback):

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    largura, altura = A4
    y = altura - 50

    def escrever_titulo(texto):
        nonlocal y
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, y, texto)
        y -= 35

    def escrever_campo(titulo, valor):
        nonlocal y

        if y < 80:
            pdf.showPage()
            y = altura - 50

        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(50, y, f"{titulo}:")
        y -= 16

        pdf.setFont("Helvetica", 10)

        texto = str(valor or "-")

        for linha in texto.split("\n"):
            while len(linha) > 95:
                pdf.drawString(70, y, linha[:95])
                linha = linha[95:]
                y -= 14

                if y < 60:
                    pdf.showPage()
                    y = altura - 50

            pdf.drawString(70, y, linha)
            y -= 14

            if y < 60:
                pdf.showPage()
                y = altura - 50

        y -= 8

    escrever_titulo("Relatório de Feedback")

    campos = [
        ("Colaborador", feedback.get("colaborador_nome", "-")),
        ("Data", feedback.get("data", "-")),
        ("Data de Revisão", feedback.get("data_revisao", "-")),
        ("Tipo", feedback.get("tipo", "-")),
        ("Origem", feedback.get("origem", "-")),
        ("Status", feedback.get("status_acompanhamento", "-")),
        ("Contexto", feedback.get("contexto", "-")),
        ("Comportamento Observado", feedback.get("comportamento_observado", "-")),
        ("Impacto Percebido", feedback.get("impacto_percebido", "-")),
        ("Leitura do Gestor", feedback.get("leitura_gestor", "-")),
        ("Orientação Dada", feedback.get("orientacao_dada", "-")),
        ("Reação do Colaborador", feedback.get("reacao_colaborador", "-")),
        ("Plano de Melhoria / Acompanhamento", feedback.get("plano_melhoria", "-")),
    ]

    for titulo, valor in campos:
        escrever_campo(titulo, valor)

    pdf.save()
    buffer.seek(0)

    return buffer.getvalue()