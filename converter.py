import markdown
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph

def md_to_pdf(input_file, output_file, font="Helvetica", page_size=letter):
    with open(input_file, "r") as f:
        text = f.read()

    if input_file.endswith(".md"):
        text = markdown.markdown(text)

    doc = SimpleDocTemplate(output_file, pagesize=page_size)
    styles = getSampleStyleSheet()
    styles["Normal"].fontName = font

    story = [Paragraph(text, styles["Normal"])]
    doc.build(story)
    print(f"✅ {input_file} converted to {output_file}")