import requests
import datetime
from config import *


def api_add_status(status, processing, last_processed_patient):
    try:
        api_url = 'https://fhr-json-status.vercel.app/' + api_name
        post_json = {
            "time": datetime.datetime.now().strftime("%d-%b %H:%M:%S"),
            "status": status,
            "processing": processing,
            "last_processed_patient": last_processed_patient
        }

        response = requests.post(api_url, json=post_json)
        print(f"[Step 8]: API Post response code: {response.status_code}")
    except Exception as e:
        print('Exception: -> Excpetion occured while adding status to api')
        print(str(e))

