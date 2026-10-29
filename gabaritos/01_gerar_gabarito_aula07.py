"""
Objetivo
    Gerar o gabarito docente das perguntas e atividades da Aula 7.

Entradas
    Dados numéricos e enunciados consolidados em index.Rmd.

Saída
    gabarito_atividades_aula07.docx, salvo na mesma pasta do script.

Transformações e critérios
    Calcula carga, utilização, fluxo, atraso e sequências FIFO, MTP, MDE e MFE.
    A MFE utiliza folga estática no tempo zero e os empates seguem a ordem de chegada.

Limitações
    O estudo de caso usa carga agregada por máquina e não substitui um cronograma
    detalhado de job shop com conflitos simultâneos e precedências temporais.
"""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE

OUTPUT = str(Path(__file__).resolve().parent / "gabarito_atividades_aula07.docx")

INK = "17324D"
BLUE = "176B87"
PALE = "EAF3F6"
PALE2 = "F5F7F8"
GRAY = "D9D9D9"
WHITE = "FFFFFF"
BLACK = "000000"


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_border(cell, color=GRAY, size="6"):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tc_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = "w:" + edge
        element = borders.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            borders.append(element)
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), size)
        element.set(qn("w:color"), color)


def set_cell_margins(cell, top=90, start=100, bottom=90, end=100):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for m, v in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn("w:" + m))
        if node is None:
            node = OxmlElement("w:" + m)
            tc_mar.append(node)
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")


def repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_repeat_table_header(row):
    repeat_table_header(row)


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Página ")
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr_text = OxmlElement("w:instrText")
    instr_text.set(qn("xml:space"), "preserve")
    instr_text.text = " PAGE "
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char1)
    run._r.append(instr_text)
    run._r.append(fld_char2)


def set_repeat_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_col_widths(table, widths):
    for row in table.rows:
        for idx, width in enumerate(widths):
            row.cells[idx].width = Inches(width)


def remove_paragraph_borders(style):
    p_pr = style._element.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is not None:
        p_pr.remove(p_bdr)


def add_table(doc, headers, rows, widths=None, font_size=9.5, alignments=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False if widths else True
    hdr = table.rows[0]
    set_repeat_header(hdr)
    for i, header in enumerate(headers):
        cell = hdr.cells[i]
        cell.text = str(header)
        set_cell_shading(cell, INK)
        set_cell_border(cell)
        set_cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in paragraph.runs:
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.bold = True
                run.font.size = Pt(font_size)
    for r_idx, values in enumerate(rows):
        row = table.add_row()
        for c_idx, value in enumerate(values):
            cell = row.cells[c_idx]
            cell.text = str(value)
            set_cell_shading(cell, WHITE if r_idx % 2 == 0 else PALE2)
            set_cell_border(cell)
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            alignment = WD_ALIGN_PARAGRAPH.LEFT
            if alignments and c_idx < len(alignments):
                alignment = alignments[c_idx]
            for paragraph in cell.paragraphs:
                paragraph.alignment = alignment
                paragraph.paragraph_format.space_after = Pt(0)
                for run in paragraph.runs:
                    run.font.size = Pt(font_size)
                    run.font.color.rgb = RGBColor(23, 50, 77)
    if widths:
        set_col_widths(table, widths)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table


def add_label_paragraph(doc, label, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(7)
    r = p.add_run(label + " ")
    r.bold = True
    r.font.color.rgb = RGBColor(23, 50, 77)
    p.add_run(text)
    return p


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        p.add_run(item)


doc = Document()
section = doc.sections[0]
section.top_margin = Inches(0.75)
section.bottom_margin = Inches(0.7)
section.left_margin = Inches(0.85)
section.right_margin = Inches(0.85)

styles = doc.styles
normal = styles["Normal"]
normal.font.name = "Arial"
normal._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
normal._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
normal.font.size = Pt(10.5)
normal.font.color.rgb = RGBColor(0, 0, 0)
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.08

title_style = styles["Title"]
title_style.font.name = "Arial"
title_style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
title_style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
title_style.font.size = Pt(28)
title_style.font.bold = True
title_style.font.color.rgb = RGBColor(0, 0, 0)
title_style.paragraph_format.space_after = Pt(14)
remove_paragraph_borders(title_style)

for name, size in (("Heading 1", 18), ("Heading 2", 14), ("Heading 3", 11.5)):
    style = styles[name]
    style.font.name = "Arial"
    style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor(0, 0, 0)
    style.paragraph_format.keep_with_next = True
    style.paragraph_format.space_before = Pt(12)
    style.paragraph_format.space_after = Pt(6)

for list_name in ("List Bullet", "List Number"):
    style = styles[list_name]
    style.font.name = "Arial"
    style._element.rPr.rFonts.set(qn("w:ascii"), "Arial")
    style._element.rPr.rFonts.set(qn("w:hAnsi"), "Arial")
    style.font.size = Pt(10.5)

# Footer
footer = section.footer
fp = footer.paragraphs[0]
fp.text = "Administração da Produção   Aula 7   Gabarito docente"
fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
for run in fp.runs:
    run.font.name = "Arial"
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(104, 119, 134)
add_page_number(footer.add_paragraph())

# Title page
p = doc.add_paragraph(style="Title")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("Gabarito das atividades da Aula 7")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Administração da Produção")
r.bold = True
r.font.size = Pt(15)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Unidade 7  Programação da produção")
r.font.size = Pt(13)
r.font.color.rgb = RGBColor(23, 107, 135)

doc.add_paragraph()
intro = doc.add_paragraph()
intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
intro.add_run(
    "Este gabarito reúne as respostas esperadas para as perguntas e atividades propostas nos slides. "
    "Os cálculos consideram os dados e as simplificações usados em aula. Respostas alternativas são "
    "válidas quando explicitam as restrições, demonstram os cálculos e relacionam a decisão ao objetivo da programação."
)

add_label_paragraph(doc, "Uso sugerido", "Aplicar após a discussão dos grupos ou como material docente de apoio à correção.")
doc.add_page_break()

doc.add_heading("1 Decisões operacionais e roteiro", level=1)

doc.add_heading("1.1 Máquina disponível e ordem impedida", level=2)
add_label_paragraph(doc, "Pergunta", "Em qual decisão uma máquina pode estar disponível e, ainda assim, a ordem não poder começar?")
add_label_paragraph(
    doc,
    "Resposta esperada",
    "A disponibilidade da máquina não garante a liberação da ordem. O impedimento pode estar no roteiro, nos materiais, "
    "nas precedências ou em outro recurso necessário."
)
add_bullets(doc, [
    "uma operação predecessora ainda não terminou",
    "o material ou componente não foi liberado pelo MRP",
    "o ferramental, o operador qualificado ou o programa da máquina não está disponível",
    "a ordem aguarda inspeção, documentação ou autorização de qualidade",
])
add_label_paragraph(doc, "Critério de correção", "A resposta deve distinguir capacidade disponível de ordem efetivamente liberada para execução.")

doc.add_heading("1.2 Carga do lote de 100 eixos", level=2)
add_label_paragraph(doc, "Pergunta", "Com 16 horas disponíveis, o problema deve ser tratado por carregamento, sequenciamento ou aumento de capacidade?")
add_table(
    doc,
    ["Operação no Torno CNC 01", "Cálculo", "Carga"],
    [
        ["Tornear desbaste", "20 + 8,5 x 100", "870 min"],
        ["Tornear acabamento", "10 + 4,2 x 100", "430 min"],
        ["Total", "870 + 430", "1.300 min"],
    ],
    widths=[2.45, 2.45, 1.25],
    alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER],
)
add_bullets(doc, [
    "capacidade disponível: 16 h = 960 min",
    "déficit: 1.300 - 960 = 340 min = 5 h 40 min",
    "utilização necessária: 1.300 / 960 = 135,4 por cento",
])
add_label_paragraph(
    doc,
    "Conclusão",
    "O diagnóstico pertence ao carregamento, pois a carga excede a capacidade. O sequenciamento define a prioridade, "
    "mas não elimina o déficit. A solução exige capacidade adicional, recurso alternativo, divisão do lote ou renegociação do prazo."
)

doc.add_page_break()
doc.add_heading("2 Regras de sequenciamento", level=1)

doc.add_heading("2.1 Sequências da carteira comum", level=2)
add_table(
    doc,
    ["Trabalho", "Processamento h", "Prazo h", "Chegada", "Folga estática h"],
    [
        ["A", "8", "15", "1", "7"],
        ["B", "3", "10", "2", "7"],
        ["C", "7", "20", "3", "13"],
        ["D", "12", "25", "4", "13"],
        ["E", "5", "12", "5", "7"],
    ],
    widths=[1.0, 1.45, 1.15, 1.0, 1.55],
    alignments=[WD_ALIGN_PARAGRAPH.CENTER] * 5,
)
add_label_paragraph(doc, "Fórmula da folga estática", "Prazo - tempo atual - tempo de processamento. Como o tempo atual é zero, a folga corresponde a prazo - processamento.")

add_table(
    doc,
    ["Regra", "Sequência", "Fluxo médio h", "Atraso médio h", "Atraso máximo h", "Atrasados"],
    [
        ["FIFO", "A - B - C - D - E", "20,4", "5,8", "23", "3"],
        ["MTP", "B - E - C - A - D", "16,8", "3,6", "10", "2"],
        ["MDE", "B - E - A - C - D", "17,0", "2,8", "10", "3"],
        ["MFE", "A - B - E - C - D", "18,6", "3,6", "10", "4"],
    ],
    widths=[0.65, 1.65, 1.1, 1.15, 1.15, 0.8],
    font_size=8.7,
    alignments=[WD_ALIGN_PARAGRAPH.CENTER] * 6,
)

add_label_paragraph(doc, "Interpretação", "MTP produz o menor fluxo médio e o menor número de trabalhos atrasados. MDE produz o menor atraso médio. O makespan é 35 horas em todas as regras porque não há ociosidade e a carga total não muda.")

doc.add_heading("2.2 Detalhamento da regra MTP", level=2)
add_table(
    doc,
    ["Ordem", "Processamento h", "Início h", "Término h", "Prazo h", "Atraso h"],
    [
        ["B", "3", "0", "3", "10", "0"],
        ["E", "5", "3", "8", "12", "0"],
        ["C", "7", "8", "15", "20", "0"],
        ["A", "8", "15", "23", "15", "8"],
        ["D", "12", "23", "35", "25", "10"],
    ],
    widths=[0.8, 1.25, 1.0, 1.0, 0.9, 0.9],
    alignments=[WD_ALIGN_PARAGRAPH.CENTER] * 6,
)
add_label_paragraph(doc, "Resposta à previsão dos grupos", "MTP tende a reduzir o fluxo médio. MDE tende a proteger melhor as datas de entrega. Nesta carteira, MDE confirma essa expectativa pelo menor atraso médio, embora MTP deixe menos trabalhos atrasados.")

doc.add_heading("2.3 Prioridade para cliente estratégico", level=2)
add_label_paragraph(doc, "Pergunta", "Que indicador mostra o custo de antecipar o pedido de um cliente estratégico para os demais pedidos?")
add_label_paragraph(doc, "Resposta esperada", "A equipe deve recalcular a sequência com e sem a prioridade e comparar os indicadores. Não basta afirmar que o cliente estratégico melhora.")
add_bullets(doc, [
    "número de pedidos atrasados e OTIF",
    "atraso médio e atraso máximo",
    "fluxo médio e tempo de espera dos pedidos deslocados",
    "eventual aumento de setup ou perda de utilização",
])
add_label_paragraph(doc, "Critério de correção", "A resposta deve medir o efeito sistêmico da prioridade, e não apenas o desempenho do pedido antecipado.")

doc.add_heading("3 Carga finita e decisões de capacidade", level=1)

doc.add_heading("3.1 Decisão antes de publicar o programa", level=2)
add_label_paragraph(doc, "Situação", "Uma máquina possui 20 horas disponíveis e recebe 24,25 horas de trabalho.")
add_label_paragraph(doc, "Resposta esperada", "A carga infinita registra o déficit de 4,25 horas. Antes de publicar o programa finito, o PCP precisa escolher uma ação que torne a carga executável.")
add_table(
    doc,
    ["Alternativa", "Quando faz sentido", "Informação que precisa ser confirmada"],
    [
        ["Hora extra", "prazo rígido e equipe disponível", "custo, limite legal, fadiga e manutenção"],
        ["Recurso alternativo", "há capacidade em máquina compatível", "roteiro, ferramental, qualidade e operador"],
        ["Dividir a ordem", "entrega parcial tem valor", "lote mínimo, setup adicional e rastreabilidade"],
        ["Novo prazo", "cliente aceita reprogramação", "impacto no serviço, contrato e carteira"],
    ],
    widths=[1.25, 2.25, 2.75],
    font_size=9,
)
add_label_paragraph(doc, "Conclusão", "Não existe uma alternativa universalmente correta. A resposta é adequada quando explicita o critério de decisão e demonstra que a carga final respeita as 20 horas.")

doc.add_heading("3.2 Transferência entre os tornos", level=2)
add_table(
    doc,
    ["Recurso", "Carga h", "Capacidade h", "Saldo h"],
    [
        ["Torno 01", "14,75", "20,00", "+5,25"],
        ["Torno 02", "24,25", "20,00", "-4,25"],
    ],
    widths=[1.6, 1.4, 1.4, 1.4],
    alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER],
)
add_label_paragraph(doc, "Resposta", "Em termos quantitativos, o Torno 01 possui 5,25 horas livres e pode absorver o déficit de 4,25 horas. A transferência só é válida se o recurso puder executar a operação com o mesmo padrão técnico.")
add_label_paragraph(doc, "Exemplo de solução", "Se a OP 005 puder ser dividida, transferir 22 das 40 unidades para o Torno 01 reduz a carga do Torno 02 para 19,85 horas. O Torno 01 recebe 0,75 hora de setup adicional e 4,40 horas de processamento, encerrando com 19,90 horas.")
add_label_paragraph(doc, "Verificações obrigatórias", "Compatibilidade do roteiro, ferramental, programa, operador, inspeção, lote mínimo, setup duplicado e prazo.")

doc.add_heading("3.3 Resposta modelo para a atividade em grupos", level=2)
add_label_paragraph(doc, "Ação escolhida", "Dividir a OP 005 e processar 22 unidades no Torno 01, desde que a transferência seja tecnicamente autorizada.")
add_label_paragraph(doc, "Justificativa", "A divisão elimina a sobrecarga e mantém ambos os tornos abaixo de 20 horas. Transferir a OP 005 inteira apenas deslocaria a sobrecarga para o Torno 01.")
add_label_paragraph(doc, "Dado adicional prioritário", "Confirmar se o Torno 01 possui ferramental, programa, capacidade de qualidade e operador qualificado para a operação da OP 005.")

doc.add_heading("4 Estudo de caso da fábrica de componentes", level=1)

doc.add_heading("4.1 Duração total dos pedidos", level=2)
add_table(
    doc,
    ["Pedido", "Prioridade", "Prazo dias", "Duração total h"],
    [
        ["P1", "2", "5", "5,7"],
        ["P2", "1", "3", "4,2"],
        ["P3", "3", "6", "6,7"],
        ["P4", "1", "4", "5,0"],
        ["P5", "2", "5", "7,2"],
    ],
    widths=[1.2, 1.2, 1.4, 1.5],
    alignments=[WD_ALIGN_PARAGRAPH.CENTER] * 4,
)
add_label_paragraph(doc, "Sequência", "P2 - P4 - P1 - P5 - P3. A prioridade menor representa maior urgência. O prazo desempata P2 e P4. P1 e P5 mantêm a ordem original porque possuem a mesma prioridade e o mesmo prazo.")

doc.add_heading("4.2 Início término e atraso", level=2)
add_table(
    doc,
    ["Ordem", "Pedido", "Duração h", "Início h", "Término h", "Prazo h", "Atraso h"],
    [
        ["1", "P2", "4,2", "0,0", "4,2", "24", "0"],
        ["2", "P4", "5,0", "4,2", "9,2", "32", "0"],
        ["3", "P1", "5,7", "9,2", "14,9", "40", "0"],
        ["4", "P5", "7,2", "14,9", "22,1", "40", "0"],
        ["5", "P3", "6,7", "22,1", "28,8", "48", "0"],
    ],
    widths=[0.65, 0.75, 0.9, 0.9, 1.0, 0.85, 0.85],
    font_size=9,
    alignments=[WD_ALIGN_PARAGRAPH.CENTER] * 7,
)
add_label_paragraph(doc, "Resultado", "O makespan simplificado é 28,8 horas e todos os pedidos ficam dentro dos prazos convertidos para jornadas de oito horas.")

doc.add_heading("4.3 Carga por máquina", level=2)
add_table(
    doc,
    ["Máquina", "Carga h", "Capacidade h", "Utilização", "Diagnóstico"],
    [
        ["M1", "10,4", "40", "26,0 por cento", "maior carga, sem restrição"],
        ["M2", "8,9", "40", "22,3 por cento", "capacidade disponível"],
        ["M3", "9,5", "40", "23,8 por cento", "capacidade disponível"],
    ],
    widths=[1.0, 1.0, 1.2, 1.45, 2.0],
    font_size=9,
    alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT],
)
add_label_paragraph(doc, "Decisão imediata", "Nenhuma máquina apresenta sobrecarga agregada. A M1 merece acompanhamento por ser a mais carregada, mas não exige hora extra neste cenário.")

doc.add_heading("4.4 A máquina mais carregada é sempre gargalo", level=2)
add_label_paragraph(doc, "Resposta", "Não. Um gargalo depende da relação entre carga e capacidade e também da posição do recurso nas precedências. A M1 tem a maior carga do caso, mas utiliza apenas 26 por cento da capacidade semanal.")
add_label_paragraph(doc, "Limitação do exercício", "A soma agregada não representa todos os conflitos simultâneos entre operações. Antes de publicar o programa, o PCP deve montar um cronograma finito por máquina e respeitar as precedências de cada pedido.")

doc.add_heading("5 Questão de fechamento", level=1)
add_label_paragraph(doc, "Pergunta", "Qual decisão mudaria primeiro se uma máquina quebrasse durante o turno?")
add_label_paragraph(doc, "Resposta esperada", "A primeira mudança ocorre na capacidade disponível e no carregamento finito. O PCP precisa retirar o período de indisponibilidade, recalcular a carga e identificar as ordens afetadas. Em seguida, deve resequenciar, transferir operações elegíveis ou renegociar prazos.")
add_bullets(doc, [
    "atualizar o calendário do recurso e o tempo estimado de reparo",
    "recalcular início, término, filas, atrasos e utilização",
    "proteger pedidos críticos e comunicar o novo programa à produção e às áreas comerciais",
])

doc.add_page_break()
doc.add_heading("6 Critérios sugeridos para correção", level=1)
add_table(
    doc,
    ["Dimensão", "Evidência esperada", "Peso sugerido"],
    [
        ["Restrições operacionais", "distingue máquina disponível de ordem liberada", "1,0"],
        ["Carga do roteiro", "calcula 1.300 min, déficit de 340 min e interpreta a capacidade", "1,0"],
        ["Sequências", "monta corretamente FIFO, MTP, MDE e MFE", "2,0"],
        ["Indicadores", "calcula ou interpreta fluxo e atraso sem confundir os conceitos", "1,5"],
        ["Decisão de capacidade", "compara alternativas e explicita a condição técnica", "1,5"],
        ["Estudo de caso", "obtém durações, sequência, términos e ausência de atraso", "2,0"],
        ["Gargalo e reação", "relaciona carga, capacidade, precedência e reprogramação", "1,0"],
    ],
    widths=[1.5, 4.0, 1.0],
    font_size=9,
    alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER],
)
add_label_paragraph(doc, "Total sugerido", "10,0 pontos. A pontuação pode ser adaptada conforme a atividade aplicada em sala.")

# Core properties
doc.core_properties.title = "Gabarito das atividades da Aula 7"
doc.core_properties.subject = "Programação da produção"
doc.core_properties.author = "Renata Oliveira"
doc.core_properties.keywords = "PCP, sequenciamento, carga de máquinas, gabarito"

doc.save(OUTPUT)
print(OUTPUT)
