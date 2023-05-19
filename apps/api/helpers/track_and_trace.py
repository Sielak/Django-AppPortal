from django.http import JsonResponse
from .db_logs import log2db
from json.decoder import JSONDecodeError
import uuid
import json
import requests
from bs4 import BeautifulSoup


class TrackAndTrace:
    """Class used to download and store documnets from carrier like schenker
    """    
    def __init__(self, args):
        try:
            self.error = 'None'
            self.filename = str(uuid.uuid4())
            if len(args) != 0:
                json_data = json.loads(args)
                self._parse_json(json_data)
            else:
                self.error = 'No data in request body'
        except JSONDecodeError:
            self.error = 'Corrupted input json'

    def _parse_json(self, json_data):
        try:
            self.root = json_data['root']
            self.url = self.root['url']
            self.path2file = '/media/TrackAndTrace/{0}/'.format(self.root['env'])
            self.carrier_name = self.url.split("/")[2]
            self.document_id = self.url.split("=")[-1]
        except KeyError:
            self.error = 'Not all mandatory fields are filled.'
        except IndexError:
            self.error = 'Problem with url - {0}'.format(self.url)

    def download_files(self):
        if self.error != 'None':
            return self.return_json(message=self.error)
        response = requests.get(self.url)
        file_extension = '.' + response.headers['Content-Type'].split("/")[1]
        if ';' in file_extension:
            file_extension = file_extension.split(';')[0]
        file_id = str(uuid.uuid1())
        filename = file_id + file_extension
        full_path = self.path2file + filename 
        soup = BeautifulSoup(response.content, features="lxml")
        try:
            new_link = soup.find('a')['href']
            if 'maps.google' in new_link or 'go.microsoft.com' in new_link:
                raise TypeError
        except TypeError:
            # if not found save first page
            try:
                with open(full_path, mode='wb') as f:     
                    f.write(response.content)
                return self.return_json(message_id='0', message="File saved at {0}".format(full_path), filename=filename)
            except FileNotFoundError:
                return self.return_json(message_id='1', message="Error saving file at {0}".format(full_path))  
        response_with_file = requests.get('https://services.schenkerfrance.fr' + new_link)
        filename = file_id + '.pdf'
        full_path = self.path2file + filename 
        try:
            with open(full_path, 'wb') as f:
                f.write(response_with_file.content)
        except FileNotFoundError:
            return self.return_json(message_id='1', message="Error saving file at {0}".format(full_path))    
        return self.return_json(message_id='0', message="File saved at {0}".format(full_path), filename=filename)

    def return_json(self, **kwargs):
        message_id = kwargs.get('message_id', '1')
        message = kwargs.get('message', 'Error')
        filename = kwargs.get('filename', '')
        status = kwargs.get('status', 200)
        res = JsonResponse(
            {'MessageId': message_id,
             'Message': message,
             'filename': filename},
            status=status)
        log2db(customer=getattr(self, 'carrier_name', 'error'), 
                type='TrackAndTrace', 
                name=getattr(self, 'document_id', 'error'), 
                result=message)
        return res