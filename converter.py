import markdown
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from docx import Document
import tempfile
import os
from docx.shared import Inches

def md_to_pdf(input_file, output_file, font="Helvetica", page_size=letter):
    story = []
    temp_dir = tempfile.mkdtemp()

    try:
        if input_file.endswith(".md"):
            with open(input_file, "r", encoding="utf-8") as f:
                text = f.read()
            text = markdown.markdown(text)
            story.append(Paragraph(text, getSampleStyleSheet()["Normal"]))
        elif input_file.endswith(".docx"):
            doc = Document(input_file)
            for para in doc.paragraphs:
                story.append(Paragraph(para.text, getSampleStyleSheet()["Normal"]))
            for rel in doc.part.rels.values():
                if "image" in rel.target_ref:
                    img_path = os.path.join(temp_dir, os.path.basename(rel.target_ref))
                    with open(img_path, "wb") as img_file:
                        img_file.write(rel.target_part.blob)
                    img = Image(img_path)
                    img.drawWidth = 7 * 72  # 4 inches
                    img.drawHeight = 6 * 72  # 3 inches
                    story.append(img)
        elif input_file.endswith(".txt"):
            with open(input_file, "r", encoding="utf-8") as f:
                text = f.read()
            story.append(Paragraph(text, getSampleStyleSheet()["Normal"]))
        else:
            raise ValueError("Unsupported file format")

        doc = SimpleDocTemplate(output_file, pagesize=page_size)
        styles = getSampleStyleSheet()
        styles["Normal"].fontName = font

        doc.build(story)
        print(f"✅ {input_file} converted to {output_file}")
    finally:
        # Clean up the temporary directory
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)