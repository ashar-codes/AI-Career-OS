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


def draw_gradient_sidebar(c, width, accent):
    for i in range(int(PAGE_HEIGHT)):
        ratio = i / PAGE_HEIGHT
        dark = colors.Color(
            accent.red * 0.6,
            accent.green * 0.6,
            accent.blue * 0.6
        )
        r = dark.red + (accent.red - dark.red) * ratio
        g = dark.green + (accent.green - dark.green) * ratio
        b = dark.blue + (accent.blue - dark.blue) * ratio
        c.setStrokeColor(colors.Color(r, g, b))
        c.line(0, i, width, i)


def draw_icon_circle(c, x, y, radius, fill_color):
    c.setFillColor(fill_color)
    c.circle(x, y, radius, fill=1)


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

    # -------------------------
    # SIDEBAR
    # -------------------------
    draw_gradient_sidebar(c, sidebar_width, accent)

    # Photo
    if photo:
        draw_circular_image(
            c,
            photo,
            sidebar_width/2 - 55,
            PAGE_HEIGHT - 190,
            110
        )
        c.setStrokeColor(colors.white)
        c.setLineWidth(3)
        c.circle(sidebar_width/2, PAGE_HEIGHT - 135, 55)

    y_sidebar = PAGE_HEIGHT - 260
    c.setFillColor(colors.white)

    # CONTACT
    c.setFont("Helvetica-Bold", 12)
    draw_icon_circle(c, 40, y_sidebar+5, 8, colors.white)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(40, y_sidebar+2, "C")

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y_sidebar, "CONTACT")
    y_sidebar -= 25

    c.setFont("Helvetica", 10)
    c.drawString(60, y_sidebar, resume.get("email", ""))
    y_sidebar -= 30

    # SKILLS
    draw_icon_circle(c, 40, y_sidebar+5, 8, colors.white)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(40, y_sidebar+2, "S")

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y_sidebar, "SKILLS")
    y_sidebar -= 25

    for skill in resume.get("skills", []):
        c.setFillColor(colors.white)
        c.setFont("Helvetica", 10)
        c.drawString(60, y_sidebar, skill)

        # Skill bar
        c.setFillColor(colors.grey)
        c.rect(60, y_sidebar-5, sidebar_width-100, 4, fill=1)
        c.setFillColor(accent)
        c.rect(60, y_sidebar-5, (sidebar_width-100)*0.7, 4, fill=1)

        y_sidebar -= 20

    # EDUCATION
    y_sidebar -= 15
    draw_icon_circle(c, 40, y_sidebar+5, 8, colors.white)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(40, y_sidebar+2, "E")

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y_sidebar, "EDUCATION")
    y_sidebar -= 25

    edu_lines = wrap_text(
        resume.get("education", ""),
        "Helvetica",
        10,
        sidebar_width - 80,
        c
    )

    for line in edu_lines:
        c.drawString(60, y_sidebar, line)
        y_sidebar -= 14

    # -------------------------
    # MAIN CONTENT
    # -------------------------
    y_main = PAGE_HEIGHT - 120

    # Name Header Band
    c.setFillColor(colors.darkgrey)
    c.rect(sidebar_width, PAGE_HEIGHT - 150, PAGE_WIDTH-sidebar_width, 150, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 32)
    c.drawString(content_x, PAGE_HEIGHT - 80, resume.get("name", ""))

    # Divider
    c.setStrokeColor(accent)
    c.setLineWidth(3)
    c.line(content_x, PAGE_HEIGHT - 100, content_x+200, PAGE_HEIGHT - 100)

    y_main = PAGE_HEIGHT - 180

    # Timeline vertical line
    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)
    c.line(content_x-20, y_main, content_x-20, 100)

    # SUMMARY
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(content_x, y_main, "SUMMARY")
    y_main -= 25

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
        # Timeline dot
        c.setFillColor(accent)
        c.circle(content_x-20, y_main+5, 4, fill=1)

        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 11)
        title_line = f"{exp.get('title','')} | {exp.get('company','')}"
        c.drawString(content_x, y_main, title_line)
        y_main -= 16

        c.setFont("Helvetica", 10)
        for bullet in exp.get("bullets", []):
            lines = wrap_text(bullet, "Helvetica", 10, content_width-10, c)
            for i, l in enumerate(lines):
                prefix = "• " if i == 0 else "   "
                c.drawString(content_x, y_main, prefix+l)
                y_main -= 14

        y_main -= 15

    c.save()
    return tmp.name
