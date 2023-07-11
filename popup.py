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

