import requests

from asyncio import get_event_loop, Future
from datetime import datetime

from general.delayer import delayer
from general.logger import push_to_log
from general.settings import TARGET_CHANNEL, BOT_TOKEN

def telegram_api_request(data, method: str, bot_token: str)->dict:
    URL = f"https://api.telegram.org/bot{bot_token}/{method}"
    resp = requests.post(url=URL, json=data)
    return resp.json()

async def send_post(message: str, time: datetime)->Future:
    data = {
        'chat_id': TARGET_CHANNEL,
        'text': message,
        'parse_mode': 'MarkdownV2',
    }
    return telegram_api_request(data, 'sendMessage', BOT_TOKEN)
