"""Render the submit-ready Markdown file to a visually checked Chinese PDF."""

from __future__ import annotations

import html
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_ROOT / "Day35&Day36作业_提交版.md"
OUTPUT = PROJECT_ROOT / "output" / "pdf" / "Day35&Day36作业_提交版.pdf"
FONT_REGULAR = Path(r"C:\Windows\Fonts\msyh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msyhbd.ttc")

INK = colors.HexColor("#17223B")
BLUE = colors.HexColor("#1F5AA6")
LIGHT_BLUE = colors.HexColor("#EAF2FC")
TEAL = colors.HexColor("#157A7A")
LIGHT_GRAY = colors.HexColor("#F4F6F8")
MID_GRAY = colors.HexColor("#667085")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("CN", str(FONT_REGULAR)))
    pdfmetrics.registerFont(TTFont("CN-Bold", str(FONT_BOLD)))


def safe(text: str) -> str:
    return html.escape(text).replace("  ", "&nbsp;&nbsp;")


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleCN",
            parent=base["Title"],
            fontName="CN-Bold",
            fontSize=25,
            leading=34,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=16,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCN",
            parent=base["Normal"],
            fontName="CN",
            fontSize=11,
            leading=18,
            textColor=MID_GRAY,
            alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "H1CN",
            parent=base["Heading1"],
            fontName="CN-Bold",
            fontSize=18,
            leading=25,
            textColor=BLUE,
            spaceBefore=4,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "H2CN",
            parent=base["Heading2"],
            fontName="CN-Bold",
            fontSize=14,
            leading=20,
            textColor=INK,
            spaceBefore=10,
            spaceAfter=7,
        ),
        "h3": ParagraphStyle(
            "H3CN",
            parent=base["Heading3"],
            fontName="CN-Bold",
            fontSize=11.5,
            leading=17,
            textColor=TEAL,
            spaceBefore=7,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "BodyCN",
            parent=base["BodyText"],
            fontName="CN",
            fontSize=9.5,
            leading=16,
            textColor=INK,
            alignment=TA_JUSTIFY,
            spaceAfter=5,
            wordWrap="CJK",
        ),
        "bullet": ParagraphStyle(
            "BulletCN",
            parent=base["BodyText"],
            fontName="CN",
            fontSize=9.3,
            leading=15,
            textColor=INK,
            leftIndent=16,
            firstLineIndent=-9,
            bulletIndent=5,
            spaceAfter=3,
            wordWrap="CJK",
        ),
        "quote": ParagraphStyle(
            "QuoteCN",
            parent=base["BodyText"],
            fontName="CN",
            fontSize=9,
            leading=15,
            textColor=colors.HexColor("#344054"),
            backColor=LIGHT_BLUE,
            borderColor=BLUE,
            borderWidth=0.8,
            borderPadding=8,
            leftIndent=6,
            rightIndent=6,
            spaceBefore=4,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "code": ParagraphStyle(
            "CodeCN",
            parent=base["Code"],
            fontName="CN",
            fontSize=8.1,
            leading=12.5,
            textColor=colors.HexColor("#182230"),
            backColor=LIGHT_GRAY,
            borderColor=colors.HexColor("#D0D5DD"),
            borderWidth=0.5,
            borderPadding=7,
            leftIndent=4,
            rightIndent=4,
            spaceBefore=3,
            spaceAfter=7,
        ),
        "table": ParagraphStyle(
            "TableCN",
            parent=base["BodyText"],
            fontName="CN",
            fontSize=8,
            leading=11.5,
            textColor=INK,
            alignment=TA_LEFT,
            wordWrap="CJK",
        ),
        "table_header": ParagraphStyle(
            "TableHeaderCN",
            parent=base["BodyText"],
            fontName="CN-Bold",
            fontSize=8.2,
            leading=11.5,
            textColor=colors.white,
            alignment=TA_CENTER,
            wordWrap="CJK",
        ),
    }


def parse_table(lines: list[str], styles: dict[str, ParagraphStyle]) -> Table:
    rows: list[list[str]] = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        rows.append(cells)
    paragraph_rows = []
    for row_index, row in enumerate(rows):
        style = styles["table_header"] if row_index == 0 else styles["table"]
        paragraph_rows.append([Paragraph(safe(cell), style) for cell in row])
    column_count = len(paragraph_rows[0])
    available_width = A4[0] - 34 * mm
    table = Table(
        paragraph_rows,
        colWidths=[available_width / column_count] * column_count,
        repeatRows=1,
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C7D2E2")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
            ]
        )
    )
    return table


def markdown_story(text: str, styles: dict[str, ParagraphStyle]) -> list[object]:
    story: list[object] = []
    lines = text.splitlines()
    index = 0
    skipped_document_title = False
    while index < len(lines):
        line = lines[index].rstrip()
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("```"):
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index].rstrip())
                index += 1
            index += 1
            story.append(Preformatted("\n".join(code_lines), styles["code"]))
            continue
        if stripped.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            story.append(parse_table(table_lines, styles))
            story.append(Spacer(1, 7))
            continue
        if stripped.startswith("# "):
            if not skipped_document_title:
                skipped_document_title = True
            else:
                story.append(PageBreak())
                story.append(Paragraph(safe(stripped[2:]), styles["h1"]))
            index += 1
            continue
        if stripped.startswith("## "):
            story.append(CondPageBreak(45 * mm))
            story.append(Paragraph(safe(stripped[3:]), styles["h1"]))
            index += 1
            continue
        if stripped.startswith("### "):
            story.append(Paragraph(safe(stripped[4:]), styles["h2"]))
            index += 1
            continue
        if stripped.startswith("#### "):
            story.append(Paragraph(safe(stripped[5:]), styles["h3"]))
            index += 1
            continue
        if stripped.startswith("> "):
            story.append(Paragraph(safe(stripped[2:]), styles["quote"]))
            index += 1
            continue
        if stripped.startswith("- "):
            story.append(Paragraph(safe(stripped[2:]), styles["bullet"], bulletText="•"))
            index += 1
            continue
        if len(stripped) > 3 and stripped[0].isdigit() and ". " in stripped[:4]:
            number, content = stripped.split(". ", 1)
            story.append(Paragraph(safe(content), styles["bullet"], bulletText=f"{number}."))
            index += 1
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            candidate = lines[index].strip()
            if (
                not candidate
                or candidate.startswith(("#", "```", "|", "> ", "- "))
                or (len(candidate) > 3 and candidate[0].isdigit() and ". " in candidate[:4])
            ):
                break
            paragraph_lines.append(candidate)
            index += 1
        story.append(Paragraph(safe(" ".join(paragraph_lines)), styles["body"]))
    return story


def page_decor(canvas, document) -> None:  # type: ignore[no-untyped-def]
    canvas.saveState()
    width, height = A4
    if document.page > 1:
        canvas.setStrokeColor(colors.HexColor("#D0D5DD"))
        canvas.setLineWidth(0.4)
        canvas.line(17 * mm, height - 15 * mm, width - 17 * mm, height - 15 * mm)
        canvas.setFont("CN", 7.5)
        canvas.setFillColor(MID_GRAY)
        canvas.drawString(17 * mm, height - 11.5 * mm, "银行 GraphRAG 与混合检索项目")
        canvas.drawRightString(width - 17 * mm, 10 * mm, f"第 {document.page} 页")
    canvas.restoreState()


def build() -> None:
    register_fonts()
    styles = build_styles()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=17 * mm,
        rightMargin=17 * mm,
        topMargin=20 * mm,
        bottomMargin=17 * mm,
        title="Day35 & Day36 银行 GraphRAG 与混合检索项目",
        author="待填写",
        subject="Neo4j GDS, LangGraph, Milvus, NL2SQL and NL2Cypher",
    )

    story: list[object] = [
        Spacer(1, 34 * mm),
        Paragraph("Day35 &amp; 项目", styles["subtitle"]),
        Spacer(1, 7 * mm),
        Paragraph("银行 GraphRAG 与混合检索", styles["title"]),
        Spacer(1, 5 * mm),
        Table(
            [
                [
                    Paragraph("Neo4j GDS", styles["subtitle"]),
                    Paragraph("LangGraph", styles["subtitle"]),
                    Paragraph("Milvus 2.6", styles["subtitle"]),
                ],
                [
                    Paragraph("Dijkstra · PageRank · Louvain", styles["table"]),
                    Paragraph("多路召回 · RRF · 硬规则", styles["table"]),
                    Paragraph("Dense · BM25 · Hybrid", styles["table"]),
                ],
            ],
            colWidths=[52 * mm, 52 * mm, 52 * mm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#B8C8DD")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D0D5DD")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            ),
        ),
        Spacer(1, 18 * mm),
        Paragraph("姓名：待填写　　团队：AI03　　日期：2026-08-30", styles["subtitle"]),
        Spacer(1, 4 * mm),
        Paragraph("完整代码、测试、复现手册和真实集成证据随文档提交", styles["subtitle"]),
        PageBreak(),
    ]
    story.extend(markdown_story(SOURCE.read_text(encoding="utf-8"), styles))
    document.build(story, onFirstPage=page_decor, onLaterPages=page_decor)
    print(OUTPUT)


if __name__ == "__main__":
    build()



