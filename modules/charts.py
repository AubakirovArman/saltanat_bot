import dash
from dash import html, dcc, Input, Output, callback, State
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
from datetime import datetime
# Инициализация приложения Dash

# Конфигурация Flowfunc
fconfig = Config.from_function_list(all_functions)
job_runner = JobRunner(fconfig)

# Layout приложения
page = dbc.Container([
    dcc.Store(id='indicator-store', data=False),
    dbc.Row([
        dbc.Col([
            dbc.ButtonGroup([
                dcc.Dropdown(
                    id='pair-dropdown',
                    options=[
                        {'label': 'BTC/USDT', 'value': 'BTCUSDT'},
                        {'label': 'ETH/USDT', 'value': 'ETHUSDT'},
                        {'label': 'BNB/USDT', 'value': 'BNBUSDT'},
                    ],
                    value='BTCUSDT',
                    clearable=False,
                    className='mr-2',
                    style={'minWidth': '150px'}
                ),
                dcc.Dropdown(
                    id='interval-dropdown',
                    options=[
                        {'label': '1m', 'value': '1m'},
                        {'label': '5m', 'value': '5m'},
                        {'label': '15m', 'value': '15m'},
                        {'label': '1h', 'value': '1h'},
                        {'label': '1d', 'value': '1d'}
                    ],
                    value='1h',
                    clearable=False,
                    style={'minWidth': '100px'}
                ),
                dbc.Button('Добавить индикатор', id='add-indicator-btn', color='secondary', className='ml-2'),
                dbc.Button('Запустить стратегию', id='run-strategy-btn', color='primary', className='ml-2'),
            ], className='flex flex-wrap gap-2'),
            dcc.Interval(id='update-interval', interval=5000, n_intervals=0)
        ], width=12)
    ], className='mb-2'),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='candlestick-graph', style={'height': '70vh'}),
            html.Div([
                html.H6('Логи стратегии', className='mt-2'),
                dcc.Textarea(id='log-output', style={'width': '100%', 'height': '15vh', 'backgroundColor': '#1e1e1e', 'color': '#fff'})
            ])
        ], width=8),
        dbc.Col(html.Div(
            id='nodeeditor_container',
            children=flowfunc.Flowfunc(
                id='node-editor',
                config=fconfig.dict(),
                context={},
            ),
            style={
                'position': 'relative',
                'height': '85vh',
                'border': '1px solid #444'
            },
        ), width=4)
    ], align='start')
], fluid=True)

# ----- callbacks -----
# Combined callback for graph updates and logging
@callback(
    [Output('candlestick-graph', 'figure'), Output('log-output', 'value'), Output('indicator-store', 'data')],
    [Input('update-interval', 'n_intervals'), Input('run-strategy-btn', 'n_clicks'), Input('add-indicator-btn', 'n_clicks')],
    [State('pair-dropdown', 'value'), State('interval-dropdown', 'value'), State('node-editor', 'nodes'), State('indicator-store', 'data'), State('log-output', 'value')],
)
def update_graph_and_logs(n_intervals, run_clicks, add_clicks, selected_pair, selected_interval, nodes, indicator, log):
    ctx = dash.callback_context
    
    # Handle add indicator button click
    if ctx.triggered and ctx.triggered[0]['prop_id'].startswith('add-indicator-btn'):
        if add_clicks:
            log = (log or '') + f"{datetime.now():%H:%M:%S} SMA indicator added\n"
            indicator = True
    
    df = get_price_data(symbol=selected_pair, interval=selected_interval)
    if indicator:
        df = calculate_sma(df)
    fig = create_candlestick_chart(df)

    if indicator and 'SMA' in df.columns:
        df['prev_close'] = df['close'].shift(1)
        df['prev_sma'] = df['SMA'].shift(1)
        buys = df[(df['prev_close'] < df['prev_sma']) & (df['close'] > df['SMA'])]
        sells = df[(df['prev_close'] > df['prev_sma']) & (df['close'] < df['SMA'])]
        fig.add_trace(go.Scatter(
            x=buys['timestamp'],
            y=buys['low'] * 0.995,
            mode='markers',
            marker_symbol='triangle-up',
            marker_color='green',
            marker_size=10,
            name='Buy'
        ))
        fig.add_trace(go.Scatter(
            x=sells['timestamp'],
            y=sells['high'] * 1.005,
            mode='markers',
            marker_symbol='triangle-down',
            marker_color='red',
            marker_size=10,
            name='Sell'
        ))

    # Handle run strategy button click
    if ctx.triggered and ctx.triggered[0]['prop_id'].startswith('run-strategy-btn'):
        if nodes:
            context = {'symbol': selected_pair, 'interval': selected_interval}
            try:
                job_runner.run(nodes, context=context)
                log = (log or '') + f"{datetime.now():%H:%M:%S} Strategy executed\n"
            except Exception as e:
                log = (log or '') + f"{datetime.now():%H:%M:%S} Error: {e}\n"
        else:
            log = (log or '') + f"{datetime.now():%H:%M:%S} No nodes to run\n"

    return fig, log, indicator
