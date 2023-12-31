## -*- coding: utf-8 -*-
import threading
import os
import json
from datetime import datetime
from config_handler import TIMEFRAMES, CANDLE_BODY_SIZE, AVG_VOLUMES_FILE
import logger as custom_logging
from binance_api import futures_list
from websocket_handler import QueueManager
from telegram_api import send_signal, send_signals_pack
from avg_volumes_updater import update_avg_volumes_by_time, update_avg_volumes, load_avg_volumes
from repeated_timer import RepeatedTimer


# timer function
def on_timer_function():
    update_avg_volumes(TIMEFRAMES)

def timer(start, **kwargs):
    # get cuurent time
    now = datetime.today().strftime("%H:%M:%S")
    tm = kwargs.get('tm')  # object of our class

    # print(now, tm.nruns)  # debug
    # check the time...
    if str(now) == start:
        on_timer_function()  # start our function


def main():
    custom_logging.info(f"Bot started.")
    custom_logging.info(f"Coin list loaded ({len(futures_list)})")
    print(f"Coin list count {len(futures_list)}.")
    send_signal(f'Bot started. Coins count: {len(futures_list)}. TF:{TIMEFRAMES}. Bar size limit: {CANDLE_BODY_SIZE}%.')

    if len(futures_list) == 0:
        exit(1)

    if os.path.isfile(AVG_VOLUMES_FILE) is False:  # avg volumes file don't exists
        # get avg volumes for every timeframe
        update_avg_volumes(TIMEFRAMES)
    elif os.path.getsize(AVG_VOLUMES_FILE) == 0:
        update_avg_volumes(TIMEFRAMES)

    load_avg_volumes(AVG_VOLUMES_FILE)

    # send tlg signals thread
    tlg_message_sender = threading.Thread(target=send_signals_pack)
    tlg_message_sender.start()
    # update avg volumes thread
    # avg_volumes_updater = threading.Thread(target=update_avg_volumes_by_time)
    # avg_volumes_updater.start()

    manager = QueueManager(symbols=futures_list, timeframes=TIMEFRAMES)
    manager.join()


if __name__ == "__main__":
    try:
        rt_avg_updater = RepeatedTimer((1., -1), timer, '03:10:00')
        main()
    finally:
        rt_avg_updater.stop()
