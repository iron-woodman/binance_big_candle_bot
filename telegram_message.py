## -*- coding: utf-8 -*-
import logger as custom_logging


class TLGMessage:
    def __init__(self, symbol, timeframe, bar_color, price_move_size_percent, volume_rate=None):
        self.pair = symbol
        self.timeframe = timeframe
        if timeframe == '4h' or timeframe == '1d':
            self.timeframe = f'*{timeframe}*'# выделяем старшие ТФ жирным
        self.bar_color = bar_color
        self.price_move_size_percent = price_move_size_percent
        self.volume_rate = volume_rate

    def generate_message(self):
        try:
            message = (
                f"Pair: {self.pair} \n"
                f"Timeframe: {self.timeframe}\n"
                f"Color: {self.bar_color}\n"
                f"Size:{self.price_move_size_percent}%\n"
            )
            if self.volume_rate is not None:
                message += f"Vol: x {self.volume_rate}"

            return message
        except Exception as e:
            print(e)
            custom_logging.error(f"TLGMessage.generate_message error: {e}.")