import json

import requests
from test import CONFIG_DATA


class OmniRunner:
    def __init__(self):
        self.base_url = CONFIG_DATA['omnirunner']['base_url']

    def update_status(self, id_test, step_name, status):
        try:
            payload = json.dumps({
                "id_test": id_test,
                "step_name": step_name,
                "status": status
                })
            headers = {
                'Content-Type': 'application/json'
            }
            print(payload)
            response = requests.post(self.base_url+"/automation/update-status", data=payload, headers=headers)
            responseJson = response.json()
            print("response_text", responseJson)
            return responseJson
        except Exception as e:
            print(f"error occur while update status to omnirunner: {str(e)}")
            raise e
