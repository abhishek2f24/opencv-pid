import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Path to the base PDF
base_pdf_path = "path_to_base_pdf.pdf"

# Path to the text file containing extracted text and coordinates
text_file_path = "path_to_extracted_text.txt"

# Path to the output PDF
output_pdf_path = "output_pdf.pdf"

# Load the base PDF
pdf_reader = PyPDF2.PdfFileReader(open(base_pdf_path, "rb"))
pdf_writer = PyPDF2.PdfFileWriter()

# Create a new PDF canvas to overlay the text
overlay_canvas = canvas.Canvas("overlay.pdf", pagesize=letter)

# Read the extracted text and coordinates
with open(text_file_path, "r", encoding="utf-8") as file:
    for line in file:
        # Extract the text and coordinates from each line
        text, xc1, yc1, xc2, yc2, xc3, yc3, xc4, yc4 = line.strip().split(",")
        
        # Convert coordinates to float
        xc1, yc1, xc2, yc2, xc3, yc3, xc4, yc4 = map(float, [xc1, yc1, xc2, yc2, xc3, yc3, xc4, yc4])

        # Overlay the text on the canvas using coordinates
        overlay_canvas.drawString(xc1, yc1, text)

# Save the overlay as a PDF
overlay_canvas.save()

# Merge the overlay PDF with the base PDF
overlay_pdf = PyPDF2.PdfFileReader(open("overlay.pdf", "rb"))

for page_num in range(pdf_reader.getNumPages()):
    page = pdf_reader.getPage(page_num)
    overlay_page = overlay_pdf.getPage(page_num)
    page.mergePage(overlay_page)
    pdf_writer.addPage(page)

# Save the resulting PDF
with open(output_pdf_path, "wb") as output_pdf:
    pdf_writer.write(output_pdf)

print("Searchable PDF creation completed.")
