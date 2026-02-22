from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, ListFlowable, ListItem
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import tempfile
import os


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return colors.Color(
        int(hex_color[0:2], 16)/255,
        int(hex_color[2:4], 16)/255,
        int(hex_color[4:6], 16)/255
    )


def register_font(font_name):
    # Basic fallback system
    try:
        if font_name.lower() == "helvetica":
            return "Helvetica"
        if font_name.lower() == "times new roman":
            return "Times-Roman"
        if font_name.lower() == "arial":
            return "Helvetica"
        return "Helvetica"
    except:
        return "Helvetica"


def generate_pdf(resume_data, template, font_name, accent_hex, photo_file):

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(
        tmp_file.name,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elements = []

    accent_color = hex_to_rgb(accent_hex)
    base_font = register_font(font_name)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontName=base_font,
        fontSize=22,
        textColor=accent_color,
        spaceAfter=10
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        fontName=base_font,
        fontSize=14,
        textColor=accent_color,
        spaceAfter=6
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontName=base_font,
        fontSize=11,
        spaceAfter=4
    )

    # -------------------------
    # HEADER
    # -------------------------
    elements.append(Paragraph(resume_data.get("name", ""), title_style))
    elements.append(Spacer(1, 10))

    if photo_file:
        img = Image(photo_file, width=1.2*inch, height=1.2*inch)
        elements.append(img)
        elements.append(Spacer(1, 12))

    # -------------------------
    # SUMMARY
    # -------------------------
    elements.append(Paragraph("Professional Summary", section_style))
    elements.append(Paragraph(resume_data.get("summary", ""), normal_style))
    elements.append(Spacer(1, 12))

    # -------------------------
    # EDUCATION
    # -------------------------
    elements.append(Paragraph("Education", section_style))
    elements.append(Paragraph(resume_data.get("education", ""), normal_style))
    elements.append(Spacer(1, 12))

    # -------------------------
    # SKILLS
    # -------------------------
    elements.append(Paragraph("Skills", section_style))

    skills = resume_data.get("skills", [])
    skill_paragraph = Paragraph(", ".join(skills), normal_style)
    elements.append(skill_paragraph)
    elements.append(Spacer(1, 12))

    # -------------------------
    # EXPERIENCE
    # -------------------------
    elements.append(Paragraph("Professional Experience", section_style))

    for exp in resume_data.get("experience", []):
        elements.append(Paragraph(
            f"<b>{exp.get('title','')}</b> | {exp.get('company','')} ({exp.get('duration','')})",
            normal_style
        ))

        bullets = [
            ListItem(Paragraph(b, normal_style))
            for b in exp.get("bullets", [])
        ]

        elements.append(ListFlowable(bullets, bulletType='bullet'))
        elements.append(Spacer(1, 10))

    # -------------------------
    # PROJECTS
    # -------------------------
    if resume_data.get("projects"):
        elements.append(Paragraph("Projects", section_style))

        for proj in resume_data.get("projects", []):
            elements.append(Paragraph(f"<b>{proj.get('title','')}</b>", normal_style))

            bullets = [
                ListItem(Paragraph(b, normal_style))
                for b in proj.get("bullets", [])
            ]

            elements.append(ListFlowable(bullets, bulletType='bullet'))
            elements.append(Spacer(1, 10))

    doc.build(elements)

    return tmp_file.name
