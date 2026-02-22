from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Frame,
    ListFlowable,
    ListItem,
    Image
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Circle
from reportlab.graphics import renderPDF
import tempfile
import os

PAGE_WIDTH, PAGE_HEIGHT = A4


# -----------------------------
# UTILITIES
# -----------------------------

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return colors.Color(
        int(hex_color[0:2], 16) / 255,
        int(hex_color[2:4], 16) / 255,
        int(hex_color[4:6], 16) / 255
    )


def register_fonts():
    # Embed fonts (add your own .ttf later if needed)
    try:
        pdfmetrics.registerFont(TTFont("Montserrat", "Montserrat-Regular.ttf"))
        pdfmetrics.registerFont(TTFont("Montserrat-Bold", "Montserrat-Bold.ttf"))
        return "Montserrat", "Montserrat-Bold"
    except:
        return "Helvetica", "Helvetica-Bold"


# -----------------------------
# CIRCULAR IMAGE MASK
# -----------------------------

def draw_circular_image(c, image_path, x, y, size):
    d = Drawing(size, size)
    circle = Circle(size / 2, size / 2, size / 2)
    d.add(circle)
    renderPDF.draw(d, c, x, y)
    c.saveState()
    c.clipPath(circle.getPath(), stroke=0)
    c.drawImage(image_path, x, y, size, size, preserveAspectRatio=True, mask='auto')
    c.restoreState()


# -----------------------------
# HEADER DRAWERS
# -----------------------------

def header_full_band(c, accent, name):
    c.setFillColor(accent)
    c.rect(0, PAGE_HEIGHT - 120, PAGE_WIDTH, 120, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 70, name)


def header_block(c, accent, name):
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(PAGE_WIDTH / 2, PAGE_HEIGHT - 80, name)
    c.setFillColor(accent)
    c.rect(PAGE_WIDTH/2 - 120, PAGE_HEIGHT - 100, 240, 8, fill=1)


def header_sidebar(c, accent):
    c.setFillColor(accent)
    c.rect(0, 0, 60, PAGE_HEIGHT, fill=1)


# -----------------------------
# MAIN GENERATOR
# -----------------------------

def generate_pdf(resume, template, font_choice, accent_hex, photo):

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(
        tmp.name,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    accent = hex_to_rgb(accent_hex)
    base_font, bold_font = register_fonts()

    styles = getSampleStyleSheet()

    h1 = ParagraphStyle(
        "h1",
        parent=styles["Heading1"],
        fontName=bold_font,
        fontSize=24,
        spaceAfter=12,
        textColor=colors.black
    )

    h2 = ParagraphStyle(
        "h2",
        parent=styles["Heading2"],
        fontName=bold_font,
        fontSize=14,
        textColor=accent,
        spaceAfter=6
    )

    body = ParagraphStyle(
        "body",
        parent=styles["Normal"],
        fontName=base_font,
        fontSize=11,
        leading=16,
        spaceAfter=6
    )

    story = []

    # -----------------------------
    # HEADER RENDER VIA CANVAS
    # -----------------------------
    def first_page(canvas_obj, doc_obj):
        if template == "Full Width Color Band":
            header_full_band(canvas_obj, accent, resume.get("name", ""))
        elif template == "Block Under Name":
            header_block(canvas_obj, accent, resume.get("name", ""))
        elif template == "Vertical Sidebar Accent":
            header_sidebar(canvas_obj, accent)
            canvas_obj.setFont(bold_font, 26)
            canvas_obj.drawString(80, PAGE_HEIGHT - 80, resume.get("name", ""))

        if photo:
            draw_circular_image(
                canvas_obj,
                photo,
                PAGE_WIDTH - 130,
                PAGE_HEIGHT - 140,
                90
            )

    # -----------------------------
    # TYPOGRAPHIC SCALE
    # -----------------------------
    story.append(Spacer(1, 120))

    # SUMMARY
    story.append(Paragraph("🧑 Professional Summary", h2))
    story.append(Paragraph(resume.get("summary", ""), body))
    story.append(Spacer(1, 12))

    # TWO COLUMN LAYOUT
    left_frame = Frame(40, 40, 180, PAGE_HEIGHT - 200, showBoundary=0)
    right_frame = Frame(240, 40, PAGE_WIDTH - 280, PAGE_HEIGHT - 200, showBoundary=0)

    left_story = []
    right_story = []

    # SIDEBAR CONTENT
    left_story.append(Paragraph("🛠 Skills", h2))
    skills = resume.get("skills", [])
    skill_list = [
        ListItem(Paragraph(skill, body))
        for skill in skills
    ]
    left_story.append(ListFlowable(skill_list, bulletType='bullet'))
    left_story.append(Spacer(1, 20))

    left_story.append(Paragraph("🎓 Education", h2))
    left_story.append(Paragraph(resume.get("education", ""), body))

    # MAIN CONTENT
    right_story.append(Paragraph("💼 Experience", h2))

    for exp in resume.get("experience", []):
        right_story.append(
            Paragraph(
                f"<b>{exp.get('title','')}</b> | {exp.get('company','')} ({exp.get('duration','')})",
                body
            )
        )

        bullets = [
            ListItem(Paragraph(b, body))
            for b in exp.get("bullets", [])
        ]
        right_story.append(ListFlowable(bullets, bulletType='bullet'))
        right_story.append(Spacer(1, 10))

    if resume.get("projects"):
        right_story.append(Paragraph("🚀 Projects", h2))
        for proj in resume.get("projects", []):
            right_story.append(Paragraph(f"<b>{proj.get('title','')}</b>", body))
            bullets = [
                ListItem(Paragraph(b, body))
                for b in proj.get("bullets", [])
            ]
            right_story.append(ListFlowable(bullets, bulletType='bullet'))
            right_story.append(Spacer(1, 10))

    doc.build(
        story,
        onFirstPage=first_page
    )

    # Draw column frames
    c = canvas.Canvas(tmp.name)
    left_frame.addFromList(left_story, c)
    right_frame.addFromList(right_story, c)
    c.save()

    return tmp.name
