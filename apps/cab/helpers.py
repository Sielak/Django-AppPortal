import requests
import json
import time
from .models import CabData


class FreshServiceAPI:
    def __init__(self):
        self.api_key = "Zpll1RafGc3UY8CoSRV"
        self.root_url = "https://hldisplayab.freshservice.com/api/v2/"
        self.root_url_v1 = "https://hldisplayab.freshservice.com/itil/"
        self.password = "x"
        self.change_statuses = [
            {
                "name": "Open",
                "id": 1
            },
            {
                "name": "Planning",
                "id": 2
            },
            {
                "name": "Awaiting Approval",
                "id": 3
            },
            {
                "name": "Pending Release",
                "id": 4
            },
            {
                "name": "Pending Review",
                "id": 5
            },
            {
                "name": "closed",
                "id": 6
            }
        ]

    def _look4name(self, status_id):
        """Look for change status name by its id  
            ## Parameters:   
            `status_id` : int    
            ## Returns:  
            `string` [change status name]  
            """
        for item in self.change_statuses:
            if item['id'] == status_id:
                return item['name']

    def fetch_changes(self):
        """Fetch all changes from FreshService and save it in DB    
            """
        results = {
            'items': [],
            'errors': []
        }
        counter = 1
        while True:
            r = requests.get(self.root_url + "changes?include=custom_fields&updated_since=2019-04-01&per_page=100&page={0}".format(counter), auth=(self.api_key, self.password))
            if r.status_code == 200:
                response_raw = json.loads(r.content)
                response = response_raw['changes']
                info = 'Page: {0}, Items: {1}'.format(counter, len(response))
                results['items'].append(info)
                print(info)
                if len(response) == 0:
                    break
                for item in response:
                    change_id = item['id']     
                    item2save = self._fetch_one_change(change_id)
                    data_checker = CabData.objects.filter(id=item2save['id'])
                    if data_checker:
                        data_checker.update(
                            status = item2save['status'],
                            step = item2save['step'],
                            stream = item2save['stream'],
                            feature = item2save['feature_number'],
                            est_dev_hrs = item2save['est_dev_hrs'],
                            est_cost_sek = item2save['est_cost_sek'],
                            est_deliv_date = item2save['est_deliv_date'],
                            subject = item2save['subject'],
                            hl_payer = item2save['hl_payer'],
                            comment = item2save['comment'],
                            description_text = item2save['description_text']
                        )
                    else:
                        CabData.objects.create(
                            id = item2save['id'],
                            status = item2save['status'],
                            step = item2save['step'],
                            stream = item2save['stream'],
                            feature = item2save['feature_number'],
                            est_dev_hrs = item2save['est_dev_hrs'],
                            est_cost_sek = item2save['est_cost_sek'],
                            est_deliv_date = item2save['est_deliv_date'],
                            subject = item2save['subject'],
                            hl_payer = item2save['hl_payer'],
                            comment = item2save['comment'],
                            description_text = item2save['description_text']
                        )
            elif r.status_code == 429:
                print("Rate limit exceeded, Sleeping for 60 sek")
                time.sleep(60)
            else:
                error = """
                    Failed to read changes, errors are displayed below,")
                    {error}
                    x-request-id : {headers}
                    Status Code : {status_code}
                """.format(error=r.text, headers=r.headers, status_code=r.status_code)
                results["errors"].append(error)
                return results
            counter += 1

        return results

    def _fetch_one_change(self, change_id):
        """Fetch info about specific change in FreshService  
            ## Parameters:   
            `change_id` : int   
            ## Returns:  
            `dict` [change id, change status, feature number]  
            """
        r = requests.get(self.root_url + "changes/{0}".format(change_id), auth=(self.api_key, self.password))
        if r.status_code == 200:
            response_raw = json.loads(r.content)
            response = response_raw['change']
            change_id = response['id']
            change_status = self._look4name(response['status'])
            change_feature_number = response['custom_fields']['feature_id']
            change_stream = response['custom_fields']['stream']
            change_step = response['custom_fields']['step']
            hl_payer = response['custom_fields']['msf_hl_unit_payer_2']
            if len(hl_payer) > 0:
                hl_payer = "#".join(hl_payer)
            else:
                hl_payer = ''
            est_dev_hrs = response['custom_fields']['est_dev_hrs']
            est_cost_sek = response['custom_fields']['est_cost_sek']
            est_deliv_date = response['custom_fields']['est_deliv_date']
            comment = response['custom_fields']['comment']
            subject = response['subject']
            description_text = response['description_text']
            change = {
                "id": change_id,
                "status_id": response['status'],
                "status": change_status,
                "feature_number": change_feature_number,
                "stream": change_stream,
                "step": change_step,
                "subject": subject,
                "hl_payer": hl_payer,
                "est_dev_hrs": est_dev_hrs,
                "est_cost_sek": est_cost_sek,
                "est_deliv_date": est_deliv_date,
                "comment": comment,
                "description_text": description_text
            }
            return change
        else:
            comment = """
            Failed to read tickets, errors are displayed below,")
            {error}
            x-request-id : {headers}
            Status Code : {status_code}
            """.format(error=r, headers=r.headers, status_code=r.status_code)
            
            change = {
                "id": change_id,
                "status_id": "error",
                "status": "error",
                "feature_number": "error",
                "stream": "error",
                "step": "error",
                "subject": "Details in comment",
                "hl_payer": "error",
                "est_dev_hrs": "error",
                "est_cost_sek": "error",
                "comment": comment,
                "description_text": "error"
            }
            return change
