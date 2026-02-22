from xhtml2pdf import pisa
import tempfile

def generate_pdf_from_html(html_content):
    result_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    with open(result_file.name, "w+b") as result:
        pisa.CreatePDF(html_content, dest=result)

    return result_file.name
