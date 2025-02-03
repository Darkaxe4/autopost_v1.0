import requests

from general.logger import push_to_log

def telegram_api_request(data, method: str, bot_token: str)->dict:
    URL = f"https://api.telegram.org/bot{bot_token}/{method}"
    resp = requests.post(url=URL, json=data)
    return resp.json()

@push_to_log
def send_delayed_post()->dict:
    raise NotImplementedError
