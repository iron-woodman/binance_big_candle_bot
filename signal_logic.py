## -*- coding: utf-8 -*-
import json
from telegram_message import TLGMessage
import logger as custom_logging
from config_handler import AVG_VOLUMES_FILE, CANDLE_BODY_SIZE


AVG_VOLUMES = dict()


def load_avg_volumes(file):
    global AVG_VOLUMES
    AVG_VOLUMES = dict()
    try:
        with open(file, 'r', encoding='cp1251') as f:
            AVG_VOLUMES = json.load(f)
        print('avg volumes loaded')
    except Exception as e:
        print("Load_avg_volume_params exception:", e)
        custom_logging.error(f"Load_avg_volumes exception: {e}")


def get_volume_ratio(volume, timeframe, symbol):
    global AVG_VOLUMES
    avg_volume = 0.0
    ratio = 0.0
    if symbol in AVG_VOLUMES:
        if timeframe in AVG_VOLUMES[symbol]:
            avg_volume = AVG_VOLUMES[symbol][timeframe]
            if avg_volume == 0:
                return None
            ratio = round(volume / avg_volume, 1)
            return ratio
    else:
        custom_logging.warning(f"Avg volume not exists for {symbol}:{timeframe}.")



def get_candle_proportion(open_, high, low, close):
    if open_ == close:
        open_ = open_ + open_ * 0.0001
    proportion = round((high - low) / abs(open_ - close), 2)
    if 2 < proportion <= 2.5:
        return "1 to 2"
    elif 2.5 < proportion <= 3:
        return "1 to 3"
    elif 3 < proportion <= 3.5:
        return "1 to 3"
    elif 3.5 < proportion <= 4:
        return "1 to 4"
    elif 4 < proportion <= 4.5:
        return "1 to 4"
    elif 4.5 < proportion <= 5:
        return "1 to 5"
    elif 5 < proportion <= 5.5:
        return "1 to 5"
    elif 5.5 < proportion <= 6:
        return "1 to 6"
    elif 6 < proportion <= 6.5:
        return "1 to 6"
    elif 6.5 < proportion <= 7:
        return "1 to 7"
    elif 7 < proportion <= 7.5:
        return "1 to 7"
    elif 7.5 < proportion <= 8:
        return "1 to 8"
    elif 8 < proportion <= 8.5:
        return "1 to 8"
    elif 8.5 < proportion <= 9:
        return "1 to 9"
    elif 9 < proportion <= 9.5:
        return "1 to 9"
    elif 9.5 < proportion <= 10:
        return "1 to 10"
    elif 10 < proportion <= 10.5:
        return "1 to 10"
    else:
        return f"1 to {proportion}"


def check_bar_for_signal(symbol, open_, high, low, close, volume, timeframe):
    bar_body_size = abs(open_ - close)
    bar_color = 'GREEN'
    if open_ >= close:
        bar_color = 'RED'
    price_move_size_procent = round(bar_body_size * 100 / open_, 2)
    if price_move_size_procent < CANDLE_BODY_SIZE:
        return
    volume_ratio = get_volume_ratio(volume, timeframe, symbol)
    custom_logging.info(
        f"{symbol}:{timeframe}:{bar_color}:PRICE_MOVE{price_move_size_procent}%:Vol. {volume_ratio}")
    tlg_message = TLGMessage(symbol, timeframe, bar_color, price_move_size_procent, volume_ratio)
    signal = tlg_message.generate_message()

    return signal
    # return f"{symbol}:{timeframe}:{price_move_size_percent}%"


load_avg_volumes(AVG_VOLUMES_FILE)