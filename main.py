## -*- coding: utf-8 -*-

import websocket
import rel
from config_handler import TIMEFRAMES,CANDLE_BODY_SIZE
import logger as custom_logging
from binance_api import futures_list
from websocket_handler import WEBSOCKET_URL_FUTURES, on_open, on_message, on_error, on_close
from telegram_api import send_signal
from binance import  ThreadedWebsocketManager


def main():
    custom_logging.info(f"Bot started.")
    custom_logging.info(f"Coin list loaded ({len(futures_list)})")
    print(f"Coin list count {len(futures_list)}.")
    send_signal(f'Bot started. Coins count: {len(futures_list)}. TF:{TIMEFRAMES}:Bar Size:{CANDLE_BODY_SIZE}')

    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(WEBSOCKET_URL_FUTURES,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever(dispatcher=rel,
                   reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()


if __name__ == "__main__":
    main()

