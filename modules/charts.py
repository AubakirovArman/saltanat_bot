import dash
from dash import Dash, html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import requests
import pandas as pd
import flowfunc
from flowfunc.config import Config
from flowfunc.jobrunner import JobRunner
from modules.nodeeditor.nodes_logic.nodes import all_functions


def get_price_data(symbol: str = None, interval: str = '1m', limit: int = 500, context: dict = None) -> pd.DataFrame:
    """Get Price Data"""
    if context:
        symbol = context.get('symbol', symbol)
        interval = context.get('interval', interval)
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
    return df

def calculate_sma(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """Calculate SMA"""
    df['SMA'] = df['close'].rolling(window=window).mean()
    return df

def create_candlestick_chart(df: pd.DataFrame) -> go.Figure:
    """Create Candlestick Chart"""
    fig = go.Figure(data=[go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Candlesticks'
    )])
    # Если в DataFrame есть колонка SMA, добавляем её на график
    if 'SMA' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['SMA'],
            mode='lines',
            line=dict(color='blue', width=2),
            name='SMA'
        ))
    fig.update_layout(
        title='График цены',
        xaxis_title='Время',
        yaxis_title='Цена',
        template='plotly_dark',
        xaxis_rangeslider_visible=False,
    )
    return fig

all_functions.append(get_price_data)
all_functions.append(calculate_sma)
all_functions.append(create_candlestick_chart)
# Инициализация приложения Dash

# Конфигурация Flowfunc
fconfig = Config.from_function_list(all_functions)
job_runner = JobRunner(fconfig)

# Layout приложения
page = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='pair-dropdown',
                options=[
                    {'label': 'BTC/USDT', 'value': 'BTCUSDT'},
                    {'label': 'ETH/USDT', 'value': 'ETHUSDT'},
                    {'label': 'BNB/USDT', 'value': 'BNBUSDT'},
                ],
                value='BTCUSDT',
                clearable=False,
                className='mb-2'
            ),
            dcc.Dropdown(
                id='interval-dropdown',
                options=[
                    {'label': '1 Minute', 'value': '1m'},
                    {'label': '5 Minutes', 'value': '5m'},
                    {'label': '15 Minutes', 'value': '15m'},
                    {'label': '1 Hour', 'value': '1h'},
                    {'label': '4 Hours', 'value': '4h'},
                    {'label': '1 Day', 'value': '1d'}
                ],
                value='1h',
                clearable=False,
            ),
            html.Button('Run Node Logic', id='run-node-logic', n_clicks=0, className='mt-2'),
        ], width=12)
    ], className='mb-2'),
    dbc.Row([
        dbc.Col(dcc.Graph(id='candlestick-graph', style={'height': '80vh'}), width=8),
        dbc.Col(html.Div(
            id='nodeeditor_container',
            children=flowfunc.Flowfunc(
                id='node-editor',
                config=fconfig.dict(),
                context={},
            ),
            style={
                'position': 'relative',
                'height': '80vh',
                'border': '1px solid black'
            },
        ), width=4)
    ], align='start')
], fluid=True)

# Коллбек для обновления графика на основе логики узлов
@callback(
    Output('candlestick-graph', 'figure'),
    Input('run-node-logic', 'n_clicks'),
    State('pair-dropdown', 'value'),
    State('interval-dropdown', 'value'),
    State('node-editor', 'nodes'),
)
def update_graph(n_clicks, selected_pair, selected_interval, nodes):
    if n_clicks == 0:
        # Возвращаем пустой график до нажатия кнопки
        return go.Figure()

    if not nodes:
        # Если узлы не настроены, возвращаем пустой график
        return go.Figure()

    # Контекст для передачи данных в узлы
    context = {
        'symbol': selected_pair,
        'interval': selected_interval
    }

    try:
        # Выполняем логику узлов с заданным контекстом
        nodes_output = job_runner.run(nodes, context=context)
    except Exception as e:
        print(f"Ошибка при выполнении логики узлов: {e}")
        return go.Figure()

    # Поиск графика в выходных данных узлов
    graph = None
    for node in nodes_output.values():
        if isinstance(node.result, go.Figure):
            graph = node.result
            break
        elif isinstance(node.result, dcc.Graph):
            graph = node.result
            break

    if graph:
        if isinstance(graph, dcc.Graph):
            return graph.figure
        elif isinstance(graph, go.Figure):
            return graph
        else:
            return go.Figure()
    else:
        # Если график не найден, возвращаем пустой график
        return go.Figure()
