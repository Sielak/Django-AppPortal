from django.conf import settings
from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.toreportlab import makerl
from pdfrw.buildxobj import pagexobj
import tempfile
from datetime import date
from .models import CrossDockingParams, CrossDockingLogs
from django.db.models import Sum
from smtplib import SMTP  # sending email
from email.mime.text import MIMEText  # constructing messages
from jinja2 import Environment  # Jinja2 templating


def create_cmr_file(po_list, carrier_name, carrier_address, carrier_country, vehicle_number, trailer_number, load_date, cmr_number):
    input_file = "{0}/cmr_template.pdf".format(settings.MEDIA_ROOT)
    # output_file = "cmr_template_out.pdf"
    output_file = tempfile.TemporaryFile()

    # Get pages
    reader = PdfReader(input_file)
    pages = [pagexobj(p) for p in reader.pages]


    # Compose new pdf
    canvas = Canvas(output_file)

    # Add page
    page = pages[3]
    canvas.setPageSize((page.BBox[2], page.BBox[3]))
    canvas.doForm(makerl(canvas, page))

    # Draw template info
    canvas.setFont('Helvetica', 8)
    # Data from user
    address = carrier_name
    name = carrier_address
    country = carrier_country
    # CMR no
    canvas.drawString(430, 760, cmr_number)
    # 1. Sender
    canvas.drawString(55, 755, "HL DISTRIBUTION CENTER EUROPE sp. z o.o.")
    canvas.drawString(55, 745, "al. Jana Nowaka-Jezioranskiego 1")
    canvas.drawString(55, 735, "44-164 Kleszczów")
    canvas.drawString(55, 725, "Poland")
    # 2. Consignee
    canvas.drawString(55, 690, "HL Display Nordic AB")
    canvas.drawString(55, 680, "Bultgatan 12")
    canvas.drawString(55, 670, "85350 Sundsvall")
    canvas.drawString(55, 660, "Sweden")
    # 3. Place of delivery of the goods
    canvas.drawString(55, 625, "Sundsvall, Sweden")
    # 4. Place and date taking over the goods
    canvas.drawString(55, 585, f"Kleszczów, Poland {load_date}")
    # 6. PO numbers
    y_6 = 500
    for item in po_list:
        pallets = item['pallet_count']
        packages = item['packages_count']
        if pallets is None:
            pallets = "0"
        if packages is None:
            packages = "0"
        canvas.drawString(55, y_6, "PO{0}".format(item['po_number']))
        canvas.drawString(110, y_6, "{0} pll / {1} pkg".format(pallets, packages))
        canvas.drawString(165, y_6, "Plastik")
        canvas.drawString(210, y_6, item['po_supplier'][:25])
        canvas.drawString(400, y_6, str(item['weight']))
        y_6 -= 10
    # 13. Sender’s instructions
    canvas.drawString(55, 280, "Towary bedace przedmiotem wewnatrzwspólnotowej")
    canvas.drawString(55, 270, "dostawy towarów zgodnie z warunkami okreslonymi w")
    canvas.drawString(55, 260, "art.. 42 ustawy z dnia 11-03-2004r o podatku od")
    canvas.drawString(55, 250, "towarów i uslug.")
    # 16. Carrier
    canvas.drawString(305, 695, address)
    canvas.drawString(305, 685, name)
    canvas.drawString(305, 675, country)
    canvas.drawString(345, 667, vehicle_number)
    canvas.drawString(420, 667, trailer_number)
    # 21. Established in
    canvas.drawString(55, 160, f"Kleszczów, Poland {date.today()}")

    canvas.showPage()
    canvas.setFont('Helvetica', 8)
    y_6 = 755
    for item in po_list:
        pallets = item['pallet_count']
        packages = item['packages_count']
        if pallets is None:
            pallets = "0"
        if packages is None:
            packages = "0"
        canvas.drawString(55, y_6, "PO{0}".format(item['po_number']))
        canvas.drawString(110, y_6, "{0} pll / {1} pkg".format(pallets, packages))
        canvas.drawString(165, y_6, "Plastik")
        canvas.drawString(210, y_6, item['po_supplier'][:25])
        canvas.drawString(320, y_6, item['pallet_location'].replace("\r\n", ', '))
        y_6 -= 10

    canvas.showPage()

    canvas.save()

    output_file.seek(0)

    return output_file


def send_summary_email():
    config_email_address = CrossDockingParams.objects.filter(Param_Name='Summary_email')

    if len(config_email_address) == 0:
        config_recipant = 'cape.polar@hl-display.com'
    elif config_email_address[0].Param_Value_string is None:
        config_recipant = 'cape.polar@hl-display.com'
    else:
        config_recipant = config_email_address[0].Param_Value_string

    # Data
    sum_pallet_count = CrossDockingLogs.objects.filter(row_status='Delivered to GLI RDC').aggregate(Sum('pallet_count'))
    sum_weight = CrossDockingLogs.objects.filter(row_status='Delivered to GLI RDC').aggregate(Sum('weight'))
    sum_packages = CrossDockingLogs.objects.filter(row_status='Delivered to GLI RDC').aggregate(Sum('packages'))

    # HTML
    TEMPLATE = """
    <style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;border-color:#ccc;}
    .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#fff;}
    .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#ccc;color:#333;background-color:#f0f0f0;}
    .tg .tg-s6z2{text-align:center}
    .tg .tg-yw4l{vertical-align:top}
    </style>
    <h1>Cross Docking Summary:</h1>
    <table class="tg">
    <tr>
        <th class="tg-yw4l">Pallet count</th>
        <th class="tg-yw4l">Pallet weight</th>
        <th class="tg-yw4l">Packages count</th>
    </tr>
    <tr>
        <td class="tg-yw4l">{{ sum_pallet_count }} pcs</td>
        <td class="tg-yw4l">{{ sum_weight }} kg</td>
        <td class="tg-yw4l">{{ sum_packages }} pcs</td>
    </tr>
    </table>
    """
    # Create a text/html message from a rendered template
    msg = MIMEText(
        Environment().from_string(TEMPLATE).render(
            title='Cross Docking summary', sum_pallet_count=sum_pallet_count['pallet_count__sum'],
            sum_weight=sum_weight['weight__sum'], sum_packages=sum_packages['packages__sum']
        ), "html"
    )
    # e-mail
    COMMASPACE = ', '
    subject = "Cross Docking Summary"
    sender = "noreply@hl-display.com"
    recipient = [config_recipant]

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(recipient)

    # Send the message via our own local SMTP server.
    s = SMTP('smtp.hl-display.com')
    s.send_message(msg)
    s.quit()
    return "Email was sent to {0}".format(recipient)
