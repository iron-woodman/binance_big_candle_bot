## -*- coding: utf-8 -*-
import requests
from config_handler import TLG_TOKEN, TLG_CHANNEL_ID
import datetime
import logger as custom_logging


def send_signal(signal):
    print("*" * 30 + "\n" + signal)
    custom_logging.info("\n" + signal)
    url = "https://api.telegram.org/bot"
    url += TLG_TOKEN
    method = url + "/sendMessage"
    attemts_count = 5
    while (attemts_count > 0):
        r = requests.post(method, data={
            "chat_id": TLG_CHANNEL_ID,
            "text": signal,
            "parse_mode": "Markdown"
        })
        if r.status_code == 200:
            return
        elif r.status_code != 200:
            print(f'Telegram send signal error ({signal}). Status code={r.status_code}. Text="{r.text}".')
            custom_logging.error(f'Telegram send signal error:\n ({signal}). \nAttempts count={attemts_count}')
            datetime.time.sleep(1)
            attemts_count -= 1
