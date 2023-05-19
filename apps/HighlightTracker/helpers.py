from django.conf import settings
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_cmr_file(delivery_number, po_list):
    packet = io.BytesIO()
    # Create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Helvetica', 8)
    if len(po_list) > 8:
        y = 280
        y2 = 280
        for item in po_list[:8]:
            can.drawString(55, y, "PO{0}".format(item))
            y -= 10
        for item in po_list[8:]:
            can.drawString(110, y2, "PO{0}".format(item))
            y2 -= 10
    else:
        y = 280
        for item in po_list:
            can.drawString(55, y, "PO{0}".format(item))
            y -= 10
    can.showPage()
    can.save()
    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # Read your existing PDF
    existing_pdf = PdfFileReader(open("{0}\\cmr_template.pdf".format(settings.MEDIA_ROOT), "rb"))
    output = PdfFileWriter()
    # Add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(3)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # Finally, write "output" to a real file
    root = "\\\\ew1-fil-101\\Public\\_IT\\_TEMP\\files_2950\\"
    filename = "{0}cmr_{1}.pdf".format(root, delivery_number)
    outputStream = open(filename, "wb")
    output.write(outputStream)
    outputStream.close()