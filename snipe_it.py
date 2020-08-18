import json
import requests


class SnipeITConnection:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def add_hardware_asset(self, machine, status_id):
        url = self.base_url + "/api/v1/hardware"

        asset_name = machine[0]
        asset_tag = input(f"Enter asset tag for {asset_name}: ")
        if asset_tag is None:
            return
        model_id = self.get_model_id(machine)
        payload = "{\"asset_tag\":\"" + asset_tag + "\",\"status_id\":" + str(status_id) + ",\"model_id\":" + str(model_id) + ",\"name\":\"" + asset_name + "\"}"
        headers = {
            'Authorization': self.api_key,
            'Accept': "application/json",
            'Content-Type': "application/json"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        if response.json()['status'] == "success":
            # We need to add the serial number with another put request
            url = self.base_url + "/api/v1/hardware/" + str(response.json()['payload']['id'])
            # We assume only a single company with id of 1
            payload = f'{{"requestable":false,"archived":false,"serial":"{machine[4]}","company_id":1}}'

            response = requests.request("PUT", url, data=payload, headers=headers)

        return response

    def get_hardware_assets(self, **kwargs):
        url = self.base_url + "/api/v1/hardware"

        if kwargs:
            querystring = {key: str(value) for key, value in kwargs.items()}
        else:
            querystring = None

        headers = {
            'Authorization': self.api_key,
            'Accept': "application/json",
            'Content-Type': "application/json"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        return response

    def get_model_id(self, machine):
        url = self.base_url + "/api/v1/models"
        querystring = {"limit": "50", "offset": "0", "search": machine[3], "sort": "created_at", "order": "asc"}

        headers = {
            'Authorization': self.api_key,
            'Accept': "application/json",
            'Content-Type': "application/json"
        }

        response = requests.request("GET", url, params=querystring, headers=headers)
        if response.json()['total'] > 1:
            print("Models:\n")
            for model in response.json()['rows']:
                print(f"Model ID [{model['id']}]: {model['name']}, {model['model_number']}")
            model_id = int(input("Select correct model ID: "))
        else:
            model_id = response.json()['rows'][0]['id']
        return model_id

    def get_status_labels(self):
        url = self.base_url + "/api/v1/statuslabels"

        headers = {
            'Authorization': self.api_key,
            'Accept': "application/json",
            'Content-Type': "application/json"
        }

        response = requests.request("GET", url, headers=headers)

        return response

    def update_hardware_asset(self, hardware_id, **kwargs):
        url = self.base_url + "/api/v1/hardware/" + str(hardware_id)

        if kwargs:
            payload = {key: str(value) for key, value in kwargs.items()}
        else:
            payload = None

        headers = {
            'Authorization': self.api_key,
            'Accept': "application/json",
            'Content-Type': "application/json"
        }

        response = requests.request("PATCH", url, headers=headers, data=json.dumps(payload))

        return response


def id_from_value(json_results, search_term):
    if not isinstance(json_results, dict):
        json_results = json.loads(json_results)

    for result in json_results['rows']:
        if search_term in result['name']:
            return result['id']
