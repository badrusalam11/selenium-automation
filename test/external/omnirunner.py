import json
import os

import requests
from test import CONFIG_DATA
from test.utils.session_manager import session_manager


class OmniRunner:
    def __init__(self):
        self.base_url = CONFIG_DATA['omnirunner']['base_url']

    def update_status(self, id_test, step_name, status, report_path=None):
        try:
            refnum = session_manager.load_reference_number()
            payload = {
                "id_test": id_test,
                "step_name": step_name,
                "status": status,
                "reference_number": refnum['reference_number']
            }
            
            files = None
            if report_path and os.path.exists(report_path):
                print("report exist")
                files = {
                    'report_file': (
                        os.path.basename(report_path),
                        open(report_path, 'rb'),
                        # 'application/pdf'
                    )
                }
                print(files)
            
            print(payload)
            response = requests.post(
                self.base_url + "/automation/update-status",
                data=payload,
                files=files
            )
            responseJson = response.json()
            print("response_text", responseJson)
            
            # Clean up the file handle if we opened one
            if files:
                files['report_file'][1].close()
                
            return responseJson
        except Exception as e:
            print(f"error occur while update status to omnirunner: {str(e)}")
            raise e
