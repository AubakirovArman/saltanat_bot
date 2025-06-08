import dash
from dash import Dash, html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import extended_flowfunc as flowfunc
from extended_flowfunc import Config
from flowfunc.jobrunner import JobRunner
from modules.nodeeditor.nodes_logic.nodes import (
    all_functions,
    get_price_data,
    calculate_sma,
    create_candlestick_chart,
)
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
            dcc.Interval(id='update-interval', interval=5000, n_intervals=0),
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
    Input('update-interval', 'n_intervals'),
    State('pair-dropdown', 'value'),
    State('interval-dropdown', 'value'),
    State('node-editor', 'nodes'),
)
def update_graph(n_intervals, selected_pair, selected_interval, nodes):

    if not nodes:
        df = get_price_data(symbol=selected_pair, interval=selected_interval)
        return create_candlestick_chart(df)

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
