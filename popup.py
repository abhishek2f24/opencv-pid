from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import NameObject, createStringObject, DictionaryObject

def add_popup_annotation(input_pdf_path, output_pdf_path, x1, y1, x3, y3, popup_text):
    pdf_reader = PdfFileReader(open(input_pdf_path, 'rb'))
    pdf_writer = PdfFileWriter()

    page = pdf_reader.getPage(0)  # Assuming you want to add the popup to the first page

    # Create the rectangle annotation
    rectangle = [x1, y1, x3, y3]
    rectangle_object = DictionaryObject()
    rectangle_object.update({
        NameObject('/Type'): NameObject('/Annot'),
        NameObject('/Subtype'): NameObject('/Square'),
        NameObject('/Rect'): createStringObject('[{}]'.format(' '.join(map(str, rectangle)))),
        NameObject('/Popup'): DictionaryObject(),
    })

    # Create the popup annotation
    popup_annotation = DictionaryObject()
    popup_annotation.update({
        NameObject('/Type'): NameObject('/Annot'),
        NameObject('/Subtype'): NameObject('/Popup'),
        NameObject('/Parent'): rectangle_object,
        NameObject('/Contents'): createStringObject(popup_text),
    })

    # Add the annotations to the page
    page['/Annots'] = [rectangle_object, popup_annotation]

    # Add the modified page to the PDF writer
    pdf_writer.addPage(page)

    # Write the output PDF file
    with open(output_pdf_path, 'wb') as output_file:
        pdf_writer.write(output_file)

# Usage example
input_pdf_path = 'input.pdf'
output_pdf_path = 'output.pdf'
x1, y1, x3, y3 = 100, 100, 200, 200
popup_text = 'This is a popup annotation.'

add_popup_annotation(input_pdf_path, output_pdf_path, x1, y1, x3, y3, popup_text)


import fitz

def add_popup_annotation(input_pdf_path, output_pdf_path, x1, y1, x3, y3, popup_text):
    doc = fitz.open(input_pdf_path)
    page = doc[0]  # Assuming you want to add the popup to the first page

    # Create the rectangle annotation
    rectangle = fitz.Rect(x1, y1, x3, y3)
    rectangle_annot = page.add_rect_annot(rectangle)

    # Create the popup annotation
    popup_annot = page.add_freetext_annot(rectangle.tl, popup_text)
    popup_annot.set_flag(fitz.ANNOT_FLAG_POPUP)

    # Associate the popup annotation with the rectangle annotation
    rectangle_annot.set_popup(popup_annot)

    doc.save(output_pdf_path, incremental=True)
    doc.close()

# Usage example
input_pdf_path = 'input.pdf'
output_pdf_path = 'output.pdf'
x1, y1, x3, y3 = 100, 100, 200, 200
popup_text = 'This is a popup annotation.'

add_popup_annotation(input_pdf_path, output_pdf_path, x1, y1, x3, y3, popup_text)




from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_rectangle_with_popup(pdf_path, x1, y1, x3, y3, text):
    output = PdfFileWriter()

    # Load the existing PDF
    with open(pdf_path, 'rb') as file:
        input_pdf = PdfFileReader(file)
        page = input_pdf.getPage(0)  # Assuming you want to add the rectangle to the first page

        # Create a canvas to draw the rectangle and the text window
        c = canvas.Canvas('temp.pdf', pagesize=letter)
        c.setLineWidth(1)
        c.setStrokeColorRGB(0, 0, 0)
        c.rect(x1, y1, x3 - x1, y3 - y1)

        # Create a text window
        text_width = x3 - x1 - 10  # Adjust the width as per your requirement
        text_height = y3 - y1 - 10  # Adjust the height as per your requirement
        c.setFont("Helvetica", 12)
        c.drawString(x1 + 5, y1 + 5, text, textWidth=text_width, leading=text_height)

        c.save()

        # Merge the canvas with the existing PDF page
        overlay_pdf = PdfFileReader('temp.pdf')
        page.mergePage(overlay_pdf.getPage(0))
        output.addPage(page)

        # Save the modified PDF with the rectangle and the text window
        with open('output.pdf', 'wb') as output_pdf:
            output.write(output_pdf)

    print("PDF with rectangle and popup created successfully!")

# Example usage
create_rectangle_with_popup('input.pdf', 100, 100, 300, 200, 'This is a popup text')





from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_button_with_popup(pdf_path, x, y, width, height, text):
    output = PdfFileWriter()

    # Load the existing PDF
    with open(pdf_path, 'rb') as file:
        input_pdf = PdfFileReader(file)
        page = input_pdf.getPage(0)  # Assuming you want to add the button to the first page

        # Create a canvas to draw the button and the rectangle
        c = canvas.Canvas('temp.pdf', pagesize=letter)

        # Create the button
        button_name = 'button1'
        c.acroForm.button(
            name=button_name,
            x=x,
            y=y,
            width=width,
            height=height,
            buttonStyle='rectangle',
            fillColor=(0, 0, 0),
            textColor=(1, 1, 1),
            borderWidth=0,
            borderColor=None,
            borderColorSelected=None,
            fillColorSelected=(0, 0, 0),
            textColorSelected=(1, 1, 1),
            annotationFlags='print',
            relative=False,
            borderWidthOn=0,
            borderStyle='solid',
            text=text,
            fontSize=12,
            forceBorder=True,
        )

        # Create the rectangle
        rect_name = 'rectangle1'
        c.acroForm.rect(
            name=rect_name,
            x=x + 2,
            y=y - 2,
            width=width - 4,
            height=height - 4,
            borderWidth=1,
            borderColor=(0, 0, 0),
            fillColor=None,
            strokeColor=(0, 0, 0),
            fillColorSelected=None,
            textColorSelected=(0, 0, 0),
            lineWidth=1,
            lineStyle='solid',
        )

        c.save()

        # Add JavaScript action to the button for the hover effect
        button_action = '''
        var rect = this.getField('rectangle1');
        rect.display = display.hidden;
        '''
        page['/AA'] = {
            '/E': 'this.setAction("MouseEnter", "' + button_action + '");'
        }

        # Merge the canvas with the existing PDF page
        overlay_pdf = PdfFileReader('temp.pdf')
        page.mergePage(overlay_pdf.getPage(0))
        output.addPage(page)

        # Save the modified PDF with the button and the rectangle
        with open('output.pdf', 'wb') as output_pdf:
            output.write(output_pdf)

    print("PDF with button and popup created successfully!")

# Example usage
create_button_with_popup('input.pdf', 100, 100, 100, 50, 'Click Me')
