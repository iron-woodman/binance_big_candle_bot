## -*- coding: utf-8 -*-
import json
from binance_api import futures_list
from config_handler import TIMEFRAMES, CANDLE_BODY_SIZE
import logger as custom_logging
from telegram_api import send_signal
WEBSOCKET_URL_FUTURES = "wss://fstream.binance.com/stream"


def lets_close_ws():
    with open('closing_socket.txt') as f:
        return int(f.readline()) > 0


def check_bar_for_signal(symbol, open_, high, low, close, volume, timeframe):
    bar_body_size = abs(open_ - close)
    price_move_size_procent = round(bar_body_size * 100 / open_, 2)
    if price_move_size_procent >= CANDLE_BODY_SIZE:
        custom_logging.info(
            f"{symbol}:{timeframe}:OHLC=({open_}, {high}, {low}, {close}):Vol={volume}:Price_Move={price_move_size_procent}")
        return f"{symbol}:{timeframe}:{price_move_size_procent}%"
    else:
        return ""

def on_message(ws, message):
    if lets_close_ws():
        ws.close()
    message = json.loads(message)

    if 'e' in message: # and 'm' in message:
        if message['m'] == 'Queue overflow. Message not filled':
            custom_logging.warning("Socket queue full. Resetting connection.")
            return
        else:
            custom_logging.error(f"Stream error: {message['m']}")
            exit(1)

    try:
        if 'stream' in message and 'data' in message:
            json_message = message['data']
            symbol = json_message['s']
            candle = json_message['k']
            is_candle_closed = candle['x']  # True -свеча сформировалась (закрыта), False - еще формируется (открыта)
            open_ = float(candle['o'])
            high = float(candle['h'])
            low = float(candle['l'])
            close = float(candle['c'])
            volume = float(candle['v'])
            timeframe = candle['i']
            candle_time = candle['t']

            if is_candle_closed:
                signal = ''
                custom_logging.info(f'{symbol}:(open={open_}, high={high}, low={low}, close={close}, timeframe="{timeframe}")')
                signal = check_bar_for_signal(symbol, open_, high, low, close, volume, timeframe)
                if signal != '':
                    send_signal(signal)

    except Exception as e:
        print("on_message exception:", e)
        custom_logging.error(f"on_message exception: {e} ")

    if False:
        # in case your internal logic invalidates the items in the queue
        # (e.g. your business logic ran too long and items in queue became "too old")
        reset_socket()

    # print(message)


def on_error(ws, error):
    print(error)
    custom_logging.error(f"Socket error: {error}")


def on_close(ws, close_status_code, close_msg):
    print("####### Socket closed. #######")
    custom_logging.warning(f"####### Socket closed. #######")


def on_open(ws):
    data = dict(
        method="SUBSCRIBE",
        id=1,
        params=[]
    )

    for symbol in futures_list:
        for timeframe in TIMEFRAMES:
            data['params'].append(f"{symbol.replace('/', '').lower()}@kline_{timeframe}")
    ws.send(json.dumps(data))
    print("Opened socket connection.")
    custom_logging.info(f"Opened socket connection.")
