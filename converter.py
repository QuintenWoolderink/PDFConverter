import markdown
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from docx import Document

def md_to_pdf(input_file, output_file, font="Helvetica", page_size=letter):
    if input_file.endswith(".md"):
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
        text = markdown.markdown(text)
    elif input_file.endswith(".docx"):
        doc = Document(input_file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file format")

    doc = SimpleDocTemplate(output_file, pagesize=page_size)
    styles = getSampleStyleSheet()
    styles["Normal"].fontName = font

    story = [Paragraph(text, styles["Normal"])]
    doc.build(story)
    print(f"✅ {input_file} converted to {output_file}")