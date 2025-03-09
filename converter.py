import os
import tempfile
import markdown
from docx import Document
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

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

                    pil_img = PILImage.open(img_path)
                    img_width, img_height = pil_img.size
                    max_width, max_height = 7 * inch, 6 * inch  # 7 inches by 6 inches

                    if img_width > max_width or img_height > max_height:
                        aspect_ratio = img_width / img_height
                        if img_width > img_height:
                            img_width = max_width
                            img_height = max_width / aspect_ratio
                        else:
                            img_height = max_height
                            img_width = max_height * aspect_ratio
                        img = Image(img_path, width=img_width, height=img_height)
                    else:
                        img = Image(img_path, width=img_width, height=img_height)

                    story.append(img)
                    pil_img.close()  # Ensure the image file is closed
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