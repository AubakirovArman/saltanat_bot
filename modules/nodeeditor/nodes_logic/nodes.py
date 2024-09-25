from time import sleep
from typing import Literal, Union, Tuple, NewType
from dash import html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import asyncio
import dash
from flowfunc.types import date, time, month, color, week
from dataclasses import dataclass
import operator
from typing import Tuple
from enum import Enum
from typing import Tuple, Any, Callable   
from binance.client import Client

from binance.enums import *
from pybit.unified_trading import HTTP 
from typing import Literal


# Словарь доступных операций
operations = {
    'greater_than': operator.gt,    # Больше
    'less_than': operator.lt,       # Меньше
    'equal': operator.eq,           # Равно
    'not_equal': operator.ne,       # Не равно
    'greater_or_equal': operator.ge, # Больше или равно
    'less_or_equal': operator.le    # Меньше или равно
}

async def add_async(number1: int, number2: int) -> int:
    """Add Numbers"""
    sleeptime = np.random.randint(0, 5)
    print(f"sleeping for {sleeptime}")
    await asyncio.sleep(sleeptime)
    return number1 + number2


def add_sync(number1: Union[int, float], number2: int) -> int:
    return number1 + number2


def add_same_objects(object1, object2):
    return object1 + object2


def response_in(name: str, data: dict):
    """Node for handling incoming data with name, method, and data"""
    return {"name": name, "data": data}

def enter_string(in_string:str) -> str:
    """String"""
    return in_string


def enter_integer(in_int: int) -> int:
    """String"""
    return in_int


def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Multiply Numbers"""
    return a * b


def sum(list_of_items: list) -> Union[float, int, str]:
    return sum(list_of_items)

def convert_to_string(obj):
    return str(obj)


def convert_to_markdown(markdown: str):
    return dash.dcc.Markdown(markdown)

def display(output1="", output2="", output3="", output4="", output5=""):
    return html.Div([output1, output2, output3, output4, output5])


def scatter_plot(df: pd.DataFrame, x: str, y: str) -> dcc.Graph:
    """Create a scatter plot from a dataframe"""
    return dcc.Graph(figure=px.scatter(df, x=x, y=y))

def custom_controls(m: month, w: week, d: date, t: time, c: color) -> str:
    out = ""
    for item in [m, w, d, t, c]:
        out += f"{item} ({type(item)})\n"
    return out.strip()

@dataclass
class vector:
    x: int
    y: int
    z: int

    def magnitude(self):
        return (self.x **2 + self.y**2 + self.z **2)**0.5

def get_vector_magnitude(v: vector):
    """Using dataclass as a port with multiple controls"""
    return v.magnitude()

def send_telegram_message(runs:bool, botid='bot1434601883:AAFDS330oYhld1GttIMLh49gBDnetCezU2A',chat_id="854186602",message="hi"):
    if runs:
        import requests 
        url=f"https://api.telegram.org/{botid}/sendMessage?chat_id={chat_id}&text={message}"
        ss=requests.post(url)
        return ss
    else:
        return False
    



class ComparisonOperation(str, Enum):
    """Перечисление доступных операций сравнения"""
    РАВНО = "=="
    Больше_чем = ">"
    Меньше_чем = "<"
    Больше_или_равно = ">="
    Меньше_или_равно = "<="

    

def ifelse(a:Any,b:Any,operations:ComparisonOperation)->bool:
    if operations==ComparisonOperation.РАВНО:    
        return a == b
    elif operationse==ComparisonOperation.Меньше_или_равно:
        return a <= b
    elif operationse==ComparisonOperation.Больше_чем:
        return a > b
    elif operationse==ComparisonOperation.Меньше_чем:
        return a < b
    elif operationse==ComparisonOperation.Больше_или_равно:
        return a >= b

def reverse(a:bool):
    if a:
        return False
    else:
        return True 
    
def binance_spot_order(api_key: str, api_secret: str, symbol: str, side: Literal['BUY', 'SELL'], order_type: Literal['MARKET', 'LIMIT'] = 'MARKET', quantity: float = None, price: float = None, time_in_force: Literal['GTC', 'IOC', 'FOK'] = 'GTC'):
    """Binance Spot Order

    Открывает или закрывает ордер на Binance Spot.

    Parameters
    ----------
    api_key : str
        Ваш API ключ Binance.
    api_secret : str
        Ваш секретный ключ Binance.
    symbol : str
        Торговая пара (например, 'BTCUSDT').
    side : str
        'BUY' или 'SELL'.
    order_type : str
        Тип ордера: 'MARKET' или 'LIMIT'.
    quantity : float
        Количество для покупки или продажи.
    price : float, optional
        Цена для лимитного ордера.
    time_in_force : str
        'GTC', 'IOC', или 'FOK' для лимитного ордера.

    Returns
    -------
    order : dict
        Информация об ордере.
    """
    client = Client(api_key, api_secret)
    order_params = {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'quantity': quantity
    }

    if order_type == 'LIMIT':
        order_params['price'] = price
        order_params['timeInForce'] = time_in_force

    order = client.create_order(**order_params)
    return order


def binance_futures_order(api_key: str, api_secret: str, symbol: str, side: Literal['BUY', 'SELL'], position_side: Literal['LONG', 'SHORT'] = 'LONG', order_type: Literal['MARKET', 'LIMIT'] = 'MARKET', quantity: float = None, price: float = None, time_in_force: Literal['GTC', 'IOC', 'FOK'] = 'GTC'):
    """Binance Futures Order

    Открывает или закрывает ордер на Binance Futures.

    Parameters
    ----------
    api_key : str
        Ваш API ключ Binance.
    api_secret : str
        Ваш секретный ключ Binance.
    symbol : str
        Торговая пара (например, 'BTCUSDT').
    side : str
        'BUY' или 'SELL'.
    position_side : str
        'LONG' или 'SHORT'.
    order_type : str
        Тип ордера: 'MARKET' или 'LIMIT'.
    quantity : float
        Количество для покупки или продажи.
    price : float, optional
        Цена для лимитного ордера.
    time_in_force : str
        'GTC', 'IOC', или 'FOK' для лимитного ордера.

    Returns
    -------
    order : dict
        Информация об ордере.
    """
    client = Client(api_key, api_secret)
    order_params = {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'quantity': quantity,
        'positionSide': position_side
    }

    if order_type == 'LIMIT':
        order_params['price'] = price
        order_params['timeInForce'] = time_in_force

    order = client.futures_create_order(**order_params)
    return order



def bybit_futures_order(api_key: str, api_secret: str, symbol: str, side: Literal['Buy', 'Sell'], order_type: Literal['Market', 'Limit'] = 'Market', qty: float = None, price: float = None, time_in_force: Literal['GoodTillCancel', 'ImmediateOrCancel', 'FillOrKill', 'PostOnly'] = 'GoodTillCancel', reduce_only: bool = False, close_on_trigger: bool = False):
    """Bybit Futures Order

    Открывает или закрывает ордер на Bybit Futures.

    Parameters
    ----------
    api_key : str
        Ваш API ключ Bybit.
    api_secret : str
        Ваш секретный ключ Bybit.
    symbol : str
        Торговая пара (например, 'BTCUSDT').
    side : str
        'Buy' или 'Sell'.
    order_type : str
        Тип ордера: 'Market' или 'Limit'.
    qty : float
        Количество для покупки или продажи.
    price : float, optional
        Цена для лимитного ордера.
    time_in_force : str
        'GoodTillCancel', 'ImmediateOrCancel', 'FillOrKill', 'PostOnly'.
    reduce_only : bool
        Флаг для закрытия позиции.
    close_on_trigger : bool
        Флаг для закрытия по триггеру.

    Returns
    -------
    order : dict
        Информация об ордере.
    """
    session = HTTP(
        endpoint="https://api.bybit.com",
        api_key=api_key,
        api_secret=api_secret
    )
    order_params = {
        'symbol': symbol,
        'side': side,
        'order_type': order_type,
        'qty': qty,
        'time_in_force': time_in_force,
        'reduce_only': reduce_only,
        'close_on_trigger': close_on_trigger
    }

    if order_type == 'Limit':
        order_params['price'] = price

    order = session.place_active_order(**order_params)
    return order

def bybit_spot_order(api_key: str, api_secret: str, symbol: str, side: Literal['Buy', 'Sell'], order_type: Literal['MARKET', 'LIMIT'] = 'MARKET', qty: float = None, price: float = None, time_in_force: Literal['GTC', 'FOK', 'IOC'] = 'GTC'):
    """Bybit Spot Order

    Открывает или закрывает ордер на Bybit Spot.

    Parameters
    ----------
    api_key : str
        Ваш API ключ Bybit.
    api_secret : str
        Ваш секретный ключ Bybit.
    symbol : str
        Торговая пара (например, 'BTCUSDT').
    side : str
        'Buy' или 'Sell'.
    order_type : str
        Тип ордера: 'MARKET' или 'LIMIT'.
    qty : float
        Количество для покупки или продажи.
    price : float, optional
        Цена для лимитного ордера.
    time_in_force : str
        'GTC', 'FOK', 'IOC'.

    Returns
    -------
    order : dict
        Информация об ордере.
    """
    session = HTTP(
        endpoint="https://api.bybit.com",
        api_key=api_key,
        api_secret=api_secret
    )
    order_params = {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'qty': qty,
        'time_in_force': time_in_force,
    }

    if order_type == 'LIMIT':
        order_params['price'] = price

    order = session.place_active_order(**order_params)
    return order


def binance_spot_correct_price(symbol: str, price: float) -> float:
    """Binance Spot Correct Price

    Корректирует цену в соответствии с требованиями Binance Spot.

    Parameters
    ----------
    symbol : str
        Торговая пара (например, 'BTCUSDT').
    price : float
        Входящая цена для корректировки.

    Returns
    -------
    corrected_price : float
        Скорректированная цена, соответствующая правилам биржи.
    """
    client = Client()
    exchange_info = client.get_symbol_info(symbol)
    filters = exchange_info['filters']
    price_filter = next((f for f in filters if f['filterType'] == 'PRICE_FILTER'), None)
    if price_filter:
        min_price = float(price_filter['minPrice'])
        max_price = float(price_filter['maxPrice'])
        tick_size = float(price_filter['tickSize'])

        # Корректируем цену в пределах min и max
        price = max(min_price, min(price, max_price))

        # Приводим цену к шагу цены (tick size)
        corrected_price = (round((price - min_price) / tick_size) * tick_size) + min_price

        # Округляем цену до нужного количества знаков после запятой
        tick_size_decimal_places = len(str(tick_size).split('.')[1].rstrip('0'))
        corrected_price = round(corrected_price, tick_size_decimal_places)

        return corrected_price
    else:
        raise ValueError(f"PRICE_FILTER not found for symbol {symbol}")


def binance_futures_correct_price(symbol: str, price: float) -> float:
    """Binance Futures Correct Price

    Корректирует цену в соответствии с требованиями Binance Futures.

    Parameters
    ----------
    symbol : str
        Торговая пара (например, 'BTCUSDT').
    price : float
        Входящая цена для корректировки.

    Returns
    -------
    corrected_price : float
        Скорректированная цена, соответствующая правилам биржи.
    """
    client = Client()
    exchange_info = client.futures_exchange_info()
    symbol_info = next((s for s in exchange_info['symbols'] if s['symbol'] == symbol), None)
    if symbol_info:
        filters = symbol_info['filters']
        price_filter = next((f for f in filters if f['filterType'] == 'PRICE_FILTER'), None)
        if price_filter:
            min_price = float(price_filter['minPrice'])
            max_price = float(price_filter['maxPrice'])
            tick_size = float(price_filter['tickSize'])

            # Корректируем цену в пределах min и max
            price = max(min_price, min(price, max_price))

            # Приводим цену к шагу цены (tick size)
            corrected_price = (round((price - min_price) / tick_size) * tick_size) + min_price

            # Округляем цену до нужного количества знаков после запятой
            tick_size_decimal_places = len(str(tick_size).split('.')[1].rstrip('0'))
            corrected_price = round(corrected_price, tick_size_decimal_places)

            return corrected_price
        else:
            raise ValueError(f"PRICE_FILTER not found for symbol {symbol}")
    else:
        raise ValueError(f"Symbol {symbol} not found in futures exchange info")

def bybit_spot_correct_price(symbol: str, price: float) -> float:
    """Bybit Spot Correct Price

    Корректирует цену в соответствии с требованиями Bybit Spot.

    Parameters
    ----------
    symbol : str
        Торговая пара (например, 'BTCUSDT').
    price : float
        Входящая цена для корректировки.

    Returns
    -------
    corrected_price : float
        Скорректированная цена, соответствующая правилам биржи.
    """
    session = HTTP("https://api.bybit.com")
    response = session.query_symbol()
    symbol_info = response.get('result', [])
    info = next((item for item in symbol_info if item['name'] == symbol), None)
    if info:
        min_price = float(info['min_price'])
        max_price = float(info['max_price'])
        price_scale = int(info['price_scale'])
        tick_size = 1 / (10 ** price_scale)

        # Корректируем цену в пределах min и max
        price = max(min_price, min(price, max_price))

        # Приводим цену к шагу цены (tick size)
        corrected_price = round(price / tick_size) * tick_size

        # Округляем цену до нужного количества знаков после запятой
        corrected_price = round(corrected_price, price_scale)

        return corrected_price
    else:
        raise ValueError(f"Symbol {symbol} not found in Bybit symbols")


def bybit_futures_correct_price(symbol: str, price: float) -> float:
    """Bybit Futures Correct Price

    Корректирует цену в соответствии с требованиями Bybit Futures.

    Parameters
    ----------
    symbol : str
        Торговая пара (например, 'BTCUSDT').
    price : float
        Входящая цена для корректировки.

    Returns
    -------
    corrected_price : float
        Скорректированная цена, соответствующая правилам биржи.
    """
    session = HTTP("https://api.bybit.com")
    response = session.query_symbol()
    symbol_info = response.get('result', [])
    info = next((item for item in symbol_info if item['name'] == symbol), None)
    if info:
        min_price = float(info['min_price'])
        max_price = float(info['max_price'])
        price_scale = int(info['price_scale'])
        tick_size = 1 / (10 ** price_scale)

        # Корректируем цену в пределах min и max
        price = max(min_price, min(price, max_price))

        # Приводим цену к шагу цены (tick size)
        corrected_price = round(price / tick_size) * tick_size

        # Округляем цену до нужного количества знаков после запятой
        corrected_price = round(corrected_price, price_scale)

        return corrected_price
    else:
        raise ValueError(f"Symbol {symbol} not found in Bybit symbols")


def get_value_by_key(data: dict, key: str):
    """Get Value by Key

    Извлекает значение из словаря по заданному ключу.

    Parameters
    ----------
    data : dict
        Входной словарь.
    key : str
        Ключ для поиска значения.

    Returns
    -------
    value : Any
        Значение, соответствующее заданному ключу, или None, если ключ не найден.
    """
    return data.get(key)



all_functions = [
    add_async,
    add_sync,
    enter_string,
    enter_integer,
    response_in,
    add_same_objects,
    convert_to_string,
    convert_to_markdown,
    display,
    scatter_plot,
    custom_controls,
    get_vector_magnitude,
    send_telegram_message,
    ifelse,
    reverse,
    binance_spot_order,
    binance_futures_order,
    bybit_futures_order,
    bybit_spot_order,
    binance_spot_correct_price,
    binance_futures_correct_price,
    bybit_spot_correct_price,
    bybit_futures_correct_price,
    get_value_by_key
]