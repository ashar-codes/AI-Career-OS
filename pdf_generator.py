from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import tempfile

PAGE_WIDTH, PAGE_HEIGHT = A4


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return colors.Color(
        int(hex_color[0:2], 16)/255,
        int(hex_color[2:4], 16)/255,
        int(hex_color[4:6], 16)/255
    )


def draw_circular_image(c, image_file, x, y, size):
    img = ImageReader(image_file)

    path = c.beginPath()
    path.circle(x + size/2, y + size/2, size/2)

    c.saveState()
    c.clipPath(path, stroke=0, fill=0)
    c.drawImage(img, x, y, size, size, preserveAspectRatio=True, mask='auto')
    c.restoreState()


def wrap_text(text, font, size, max_width, c):
    words = text.split()
    lines = []
    current = ""

    c.setFont(font, size)

    for word in words:
        test = current + " " + word if current else word
        if c.stringWidth(test, font, size) < max_width:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def generate_pdf(resume, template, font_choice, accent_hex, photo):

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(tmp.name, pagesize=A4)

    accent = hex_to_rgb(accent_hex)

    sidebar_width = PAGE_WIDTH * 0.35
    content_x = sidebar_width + 40
    content_width = PAGE_WIDTH - sidebar_width - 80

    # =============================
    # SIDEBAR BACKGROUND
    # =============================
    c.setFillColor(accent)
    c.rect(0, 0, sidebar_width, PAGE_HEIGHT, fill=1)

    # =============================
    # PHOTO
    # =============================
    if photo:
        draw_circular_image(
            c,
            photo,
            sidebar_width/2 - 60,
            PAGE_HEIGHT - 200,
            120
        )

    y_sidebar = PAGE_HEIGHT - 250

    c.setFillColor(colors.white)

    # =============================
    # CONTACT
    # =============================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y_sidebar, "CONTACT")
    y_sidebar -= 20

    c.setFont("Helvetica", 10)
    contact_lines = [
        resume.get("email", ""),
    ]

    for line in contact_lines:
        wrapped = wrap_text(line, "Helvetica", 10, sidebar_width - 80, c)
        for w in wrapped:
            c.drawString(40, y_sidebar, w)
            y_sidebar -= 14

    y_sidebar -= 20

    # =============================
    # SKILLS
    # =============================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y_sidebar, "SKILLS")
    y_sidebar -= 20

    c.setFont("Helvetica", 10)

    for skill in resume.get("skills", []):
        wrapped = wrap_text(skill, "Helvetica", 10, sidebar_width - 80, c)
        for w in wrapped:
            c.drawString(40, y_sidebar, "• " + w)
            y_sidebar -= 14

    y_sidebar -= 20

    # =============================
    # EDUCATION
    # =============================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y_sidebar, "EDUCATION")
    y_sidebar -= 20

    edu_lines = wrap_text(
        resume.get("education", ""),
        "Helvetica",
        10,
        sidebar_width - 80,
        c
    )

    for line in edu_lines:
        c.drawString(40, y_sidebar, line)
        y_sidebar -= 14

    # =============================
    # MAIN CONTENT
    # =============================
    y_main = PAGE_HEIGHT - 120

    # NAME
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 32)
    c.drawString(content_x, y_main, resume.get("name", ""))
    y_main -= 30

    # Divider
    c.setStrokeColor(accent)
    c.setLineWidth(3)
    c.line(content_x, y_main, content_x + content_width, y_main)
    y_main -= 30

    # SUMMARY
    c.setFont("Helvetica-Bold", 14)
    c.drawString(content_x, y_main, "PROFESSIONAL SUMMARY")
    y_main -= 20

    c.setFont("Helvetica", 10.5)
    summary_lines = wrap_text(
        resume.get("summary", ""),
        "Helvetica",
        10.5,
        content_width,
        c
    )

    for line in summary_lines:
        c.drawString(content_x, y_main, line)
        y_main -= 14

    y_main -= 25

    # EXPERIENCE
    c.setFont("Helvetica-Bold", 14)
    c.drawString(content_x, y_main, "EXPERIENCE")
    y_main -= 20

    for exp in resume.get("experience", []):
        c.setFont("Helvetica-Bold", 11)
        title_line = f"{exp.get('title','')} | {exp.get('company','')} ({exp.get('duration','')})"
        c.drawString(content_x, y_main, title_line)
        y_main -= 16

        c.setFont("Helvetica", 10)

        for bullet in exp.get("bullets", []):
            bullet_lines = wrap_text(bullet, "Helvetica", 10, content_width - 15, c)
            for i, bl in enumerate(bullet_lines):
                prefix = "• " if i == 0 else "   "
                c.drawString(content_x, y_main, prefix + bl)
                y_main -= 14

        y_main -= 10

    # PROJECTS
    if resume.get("projects"):
        y_main -= 10
        c.setFont("Helvetica-Bold", 14)
        c.drawString(content_x, y_main, "PROJECTS")
        y_main -= 20

        for proj in resume.get("projects", []):
            c.setFont("Helvetica-Bold", 11)
            c.drawString(content_x, y_main, proj.get("title", ""))
            y_main -= 16

            c.setFont("Helvetica", 10)

            for bullet in proj.get("bullets", []):
                bullet_lines = wrap_text(bullet, "Helvetica", 10, content_width - 15, c)
                for i, bl in enumerate(bullet_lines):
                    prefix = "• " if i == 0 else "   "
                    c.drawString(content_x, y_main, prefix + bl)
                    y_main -= 14

            y_main -= 10

    c.save()
    return tmp.name
