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


def wrap_text(text, font, size, max_width, c):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = current + " " + word if current else word
        if c.stringWidth(test, font, size) <= max_width:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def draw_circular_image(c, image_file, x, y, size):
    img = ImageReader(image_file)
    path = c.beginPath()
    path.circle(x + size/2, y + size/2, size/2)

    c.saveState()
    c.clipPath(path, stroke=0, fill=0)
    c.drawImage(img, x, y, size, size, preserveAspectRatio=True, mask='auto')
    c.restoreState()


def generate_pdf(resume, template, font_choice, accent_hex, photo):

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(tmp.name, pagesize=A4)

    accent = hex_to_rgb(accent_hex)

    header_height = 130
    sidebar_width = PAGE_WIDTH * 0.33

    dark_header = colors.HexColor("#1F1F1F")
    dark_sidebar = colors.HexColor("#2A2A2A")
    right_bg = colors.HexColor("#F4F4F4")

    # ---------------- HEADER ----------------
    c.setFillColor(dark_header)
    c.rect(0, PAGE_HEIGHT - header_height, PAGE_WIDTH, header_height, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 34)
    name_width = c.stringWidth(resume.get("name", ""), "Helvetica-Bold", 34)
    c.drawString((PAGE_WIDTH - name_width)/2, PAGE_HEIGHT - 80, resume.get("name", ""))

    c.setStrokeColor(accent)
    c.setLineWidth(3)
    c.line(PAGE_WIDTH*0.25, PAGE_HEIGHT - 100, PAGE_WIDTH*0.75, PAGE_HEIGHT - 100)

    # ---------------- RIGHT BACKGROUND ----------------
    c.setFillColor(right_bg)
    c.rect(sidebar_width, 0, PAGE_WIDTH-sidebar_width, PAGE_HEIGHT-header_height, fill=1)

    # ---------------- SIDEBAR ----------------
    c.setFillColor(dark_sidebar)
    c.rect(0, 0, sidebar_width, PAGE_HEIGHT-header_height, fill=1)

    y_sidebar = PAGE_HEIGHT - header_height - 40

    # Photo
    if photo:
        draw_circular_image(
            c,
            photo,
            sidebar_width/2 - 50,
            y_sidebar - 100,
            100
        )
        c.setStrokeColor(colors.white)
        c.setLineWidth(2)
        c.circle(sidebar_width/2, y_sidebar - 50, 50)
        y_sidebar -= 130

    c.setFillColor(colors.white)

    # CONTACT
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y_sidebar, "CONTACT")
    y_sidebar -= 20

    c.setFont("Helvetica", 10)
    c.drawString(40, y_sidebar, resume.get("email", ""))
    y_sidebar -= 40

    # SKILLS (limit 6)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y_sidebar, "SKILLS")
    y_sidebar -= 25

    skills = resume.get("skills", [])[:6]

    bar_width = sidebar_width - 80

    for i, skill in enumerate(skills):
        c.setFont("Helvetica", 10)
        c.drawString(40, y_sidebar, skill)
        y_sidebar -= 10

        c.setFillColor(colors.grey)
        c.rect(40, y_sidebar, bar_width, 3, fill=1)

        fill_ratio = 0.85 - (i * 0.08)
        fill_ratio = max(fill_ratio, 0.5)

        c.setFillColor(accent)
        c.rect(40, y_sidebar, bar_width * fill_ratio, 3, fill=1)

        y_sidebar -= 20

    # EDUCATION
    y_sidebar -= 10
    c.setFillColor(colors.white)
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

    # ---------------- MAIN CONTENT ----------------
    content_x = sidebar_width + 50
    content_width = PAGE_WIDTH - sidebar_width - 100
    y_main = PAGE_HEIGHT - header_height - 50

    # SUMMARY
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(content_x, y_main, "SUMMARY")
    y_main -= 25

    c.setFont("Helvetica", 10)
    summary_lines = wrap_text(
        resume.get("summary", ""),
        "Helvetica",
        10,
        content_width,
        c
    )

    for line in summary_lines:
        c.drawString(content_x, y_main, line)
        y_main -= 14

    y_main -= 30

    # EXPERIENCE
    c.setFont("Helvetica-Bold", 13)
    c.drawString(content_x, y_main, "EXPERIENCE")
    y_main -= 25

    c.setStrokeColor(accent)
    c.setLineWidth(2)
    c.line(content_x - 20, y_main + 10, content_x - 20, 100)

    for exp in resume.get("experience", []):
        c.setFillColor(accent)
        c.circle(content_x - 20, y_main + 5, 5, fill=1)

        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 11)
        title_line = f"{exp.get('title','')} | {exp.get('company','')}"
        c.drawString(content_x, y_main, title_line)
        y_main -= 18

        c.setFont("Helvetica", 10)
        for bullet in exp.get("bullets", []):
            bullet_lines = wrap_text(
                bullet,
                "Helvetica",
                10,
                content_width,
                c
            )

            for i, line in enumerate(bullet_lines):
                prefix = "• " if i == 0 else "   "
                c.drawString(content_x, y_main, prefix + line)
                y_main -= 14

        y_main -= 20

    c.save()
    return tmp.name
