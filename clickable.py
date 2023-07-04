import PyPDF2

def create_clickable_pdf(excel_data, output_pdf_path, link_url):
    pdf = PyPDF2.PdfFileWriter()
    with open('input.pdf', 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        page = pdf_reader.getPage(0)  # Assuming you want to modify the first page
        width = page.mediaBox.getWidth()
        height = page.mediaBox.getHeight()

        # Iterate through the Excel data
        for data in excel_data:
            xc1, xc2, xc3, xc4, yc1, yc2, yc3, yc4 = data  # Assuming data is in the format you mentioned

            # Calculate the coordinates of the rectangle on the page
            x1 = xc1 * width
            x2 = xc2 * width
            y1 = yc1 * height
            y2 = yc2 * height

            # Create an annotation with a link
            annotation = PyPDF2.pdf.PageAnnotation.create_link(
                uri=link_url,
                rect=[x1, y1, x2, y2]
            )
            page.add_annotation(annotation)

        pdf.addPage(page)

        # Save the modified PDF
        with open(output_pdf_path, 'wb') as output_file:
            pdf.write(output_file)

# Example usage
excel_data = [
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],  # Example data for one rectangle
    # Add more rectangles if needed
]
output_pdf_path = 'output.pdf'
link_url = 'https://www.example.com'

create_clickable_pdf(excel_data, output_pdf_path, link_url)
