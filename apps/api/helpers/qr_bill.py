from django.conf import settings
import shutil
import xmltodict       
from json.decoder import JSONDecodeError
import os
# imports for qr
import uuid
from qrbill.bill import QRBill
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from django.http import JsonResponse
import PyPDF2 
import json
from xml.parsers.expat import ExpatError
from .db_logs import log2db


class CreateQrBill:
    """
    Class used for creating QR code  
    with Swiss invoice
    Input JSON structure
    {
        "root": {
            "source": "qr_bill",
            "account": "",
            "creditor": {
                "name": "",
                "street": "",
                "city": "",
                "pcode": "",
                "country": ""
            },
            "amount": "",
            "currency": "",
            "debtor": {
                "name": "",
                "street": "",
                "city": "",
                "pcode": "",
                "country": ""
            },
            "ref_number": "",
            "extra_infos": ""
        }
    }
    """
    def __init__(self, args, input_type):
        try:
            self.error = 'None'
            self.filename = str(uuid.uuid4())
            if len(args) != 0:
                if input_type == "json":
                    json_data = json.loads(args)
                else:
                    try:
                        json_data = self.convert_xml(args)
                    except ExpatError:
                        self.error = 'xml data corrupted'    
                self.parse_json(json_data)
            else:
                self.error = 'No data in request body'
        except JSONDecodeError:
            self.error = 'Corrupted input json'

    def convert_xml(self, xml_string):
        json_file = xmltodict.parse(xml_string)
        return json_file

    def parse_json(self, json_data):
        try:
            self.root = json_data['root']
            self.account = self.root['account']
            self.creditor = self.root['creditor']
            self.creditor_name = self.creditor['name']
            self.creditor_street = self.creditor['street']
            self.creditor_city = self.creditor['city']
            self.creditor_pcode = self.creditor['pcode']
            self.creditor_country = self.creditor['country']
            self.amount = self.root['amount']
            self.currency = self.root['currency']
            self.debtor = self.root['debtor']
            self.debtor_name = self.debtor['name']
            self.debtor_street = self.debtor['street']
            self.debtor_city = self.debtor['city']
            self.debtor_pcode = self.debtor['pcode']
            self.debtor_country = self.debtor['country']
            self.file_path = self.root['filepath']
            self.foretagkod = self.root['foretagkod']
            self.invoice_number = self.root['faktnr']
            self.ref_number = self.root['ref_number']
            # self.extra_infos = self.root['extra_infos']
        except KeyError:
            self.error = 'Not all mandatory fields are filled.'


    def create_qr_file(self):
        if self.error != 'None':
            return self.return_json(message=self.error)
        # check if original invoice exists on path
        invoice_checker = os.path.isfile(f"{self.file_path}/Invoice_{self.foretagkod}_{self.invoice_number}.pdf")
        if invoice_checker is False:
            return self.return_json(message=f'File for invoice {self.file_path}/Invoice_{self.foretagkod}_{self.invoice_number} not exists')
        try:
            my_bill = QRBill(
                account=self.account,
                creditor={
                    'name': self.creditor_name, 
                    'pcode': self.creditor_pcode, 
                    'city': self.creditor_city, 
                    'country': self.creditor_country,
                    'street': self.creditor_street,
                },
                amount = '{:.2f}'.format(float(self.amount)),
                currency = self.currency,
                debtor = {
                    'name': self.debtor_name,
                    'street': self.debtor_street,
                    'pcode': self.debtor_pcode,
                    'city': self.debtor_city,
                    'country': self.debtor_country,
                },
                ref_number = self.ref_number,
                # extra_infos = self.extra_infos,
            )
        except Exception as e:
            return self.return_json(message=str(e))    
        # full_path2file = f"{self.file_path}/{self.filename}.pdf"
        temp_file = f"{settings.MEDIA_ROOT}/qr_bill/{self.filename}.svg"
        temp_file_pdf = f"{settings.MEDIA_ROOT}/qr_bill/{self.filename}.pdf"
        with open(temp_file, mode='w', encoding='utf-8') as temp:
            my_bill.as_svg(temp)
            temp.seek(0)
            drawing = svg2rlg(temp.name)
            renderPDF.drawToFile(drawing, temp_file_pdf)
        self.delete_old_files(temp_file)
        self.combine_pdfs(temp_file_pdf)
        self.delete_old_files(temp_file_pdf)
        return self.return_json(message_id='0', message=f"File{self.file_path}/Invoice_{self.foretagkod}_{self.invoice_number}.pdf updated")

    def return_json(self, **kwargs):
        message_id = kwargs.get('message_id', '1')
        message = kwargs.get('message', 'Error')
        email = kwargs.get('email', 'dawid.wybierek@hl-display.com')
        email_cc = kwargs.get('email_cc', '')
        status = kwargs.get('status', 200)
        res = JsonResponse(
            {'MessageId': message_id,
             'Message': message,
             'email': email,
             'email_cc': email_cc},
            status=status)
        log2db(customer=getattr(self, 'debtor_name', 'error'), 
                type='qrBill', 
                name=getattr(self, 'account', 'error'), 
                result=message)
        return res

    def delete_old_files(self, file_path):
        """
        Helper method for deleting already processed files.
        :return:
        Nothing
        """
        try:
            os.remove(file_path)
        except (IndexError, FileNotFoundError) as e:
            pass

    def combine_pdfs(self, qr_bill_pdf):
        # config
        invoice_pdf = f"{self.file_path}/Invoice_{self.foretagkod}_{self.invoice_number}.pdf"
        output_path = f"{settings.MEDIA_ROOT}/qr_bill/Invoice_{self.foretagkod}_{self.invoice_number}.pdf"
        # Open the files that have to be merged one by one
        pdf1File = open(invoice_pdf, 'rb')
        pdf2File = open(qr_bill_pdf, 'rb')
        
        # Read the files that you have opened
        pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
        pdf2Reader = PyPDF2.PdfFileReader(pdf2File)
        
        # Create a new PdfFileWriter object which represents a blank PDF document
        pdfWriter = PyPDF2.PdfFileWriter()
        
        # Loop through all the pagenumbers for the first document
        for pageNum in range(pdf1Reader.numPages):
            pageObj = pdf1Reader.getPage(pageNum)
            pdfWriter.addPage(pageObj)
        
        # Loop through all the pagenumbers for the second document
        for pageNum in range(pdf2Reader.numPages):
            pageObj = pdf2Reader.getPage(pageNum)
            pdfWriter.addPage(pageObj)
        
        # Now that you have copied all the pages in both the documents, write them into the a new document        
        pdfOutputFile = open(output_path, 'wb')
        pdfWriter.write(pdfOutputFile)
        
        # Close all the files - Created as well as opened
        pdfOutputFile.close()
        pdf1File.close()
        pdf2File.close()

        # Copy combined pdf to final destination
        os.remove(invoice_pdf)
        shutil.move(output_path, invoice_pdf)
        
