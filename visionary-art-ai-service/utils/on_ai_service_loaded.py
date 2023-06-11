import requests
import json
from modules import shared

host_url = "http://127.0.0.1:" + shared.opts.visionary_art_server_port

def on_ai_service_loaded(service_port, auth_key):
    url = "{0}/on_ai_service_loaded?service_port={1}&auth_key={2}".format(
        host_url, service_port, auth_key
    )

    payload = {}
    headers = {
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        pass
