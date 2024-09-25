import flowfunc
import time
import os
from dash import html, dcc
from flowfunc.config import Config 
from flowfunc.jobrunner import JobRunner
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_bootstrap_components as dbc
import json
import base64
from flask import Blueprint, request,jsonify
from flowfunc.models import OutNode, Node, Port
from modules.nodeeditor.nodes_logic.nodes import all_functions
from dash import Dash, html, dcc, Input, Output, callback, State
from typing import Any
from flowfunc.models import Node, Port



bp = Blueprint('routes', __name__)
# Конфигурация и инициализация JobRunner
fconfig = Config.from_function_list(all_functions)
job_runner = JobRunner(fconfig)

# Словарь для хранения зарегистрированных логик
registered_logics = {}

# Загрузка сохраненных логик при старте приложения
if os.path.exists("modules/nodeeditor/registered_logics.json"):
    with open("modules/nodeeditor/registered_logics.json", "r") as f:
        registered_logics = json.load(f)



node_editor=html.Div(
    [
        dbc.ButtonGroup(
            [
                dbc.Button(id="run", children="Run"),
                dbc.Button(id="save", children="Save"),
                dbc.Button(id="clear", children="Clear"),
                dbc.Button(id="save_logic", children="Save Logic to Registered"),
                dcc.Upload(
                    id="uploader", children=dbc.Button(id="load", children="Load")
                ),
                dcc.Download(id="download"),
            ],
        ),
        html.Div(
            id="nodeeditor_container",
            children=flowfunc.Flowfunc(
                id="input1",
                config=fconfig.dict(),
                context={"context": "initial"},
            ),
            style={
                "position": "relative",
                "width": "100%",
                "height": "70vh",
            },
        ),
    ]
)



# Основной интерфейс приложения
page = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(width=8, children=node_editor),
                dbc.Col(
                    id="output", width=4, style={"height": "100vh", "overflow": "auto"}
                ),
            ],
        ),
        # Компонент для отображения статуса сохранения логики
        html.Div(id="save-status"),
    ],
    style={"overflow": "hidden"},
)

# Маршрут для обработки запросов по пути /input/<name_logic>
@bp.route('/input/<name_logic>', methods=['POST','GET'])
def execute_logic(name_logic):

    # if registered_logics[name_logic] !='':
    #     print('11122')
    #     ss=registered_logics[name_logic]
    #     # dict(ss[list(ss.keys())[0]])['inputData']['data']['dict']={1:'ss'}
    #     print(dict(ss[list(ss.keys())[0]])['inputData']['data']['dict'])
    #     return ss[list(ss.keys())[0]]
    if request.method == 'POST':
        if name_logic not in registered_logics:
            return jsonify({"status": "error", "message": f"No logic found for {name_logic}"}), 404
        nodes = registered_logics[name_logic]
        # Получение данных из POST-запроса

        data = request.get_json()
        # Передача data в ноды

        for node in nodes.values():
            print(node['inputData'])
            if node['type'] == "modules.nodeeditor.nodes_logic.nodes.response_in":
                node['inputData']['data']['dict'] = dict(data['message'])

        # Выполнение логики с обновленными данными
        nodes_output = job_runner.run(nodes)
        output_results = {}
        for node_id, node in nodes_output.items():
            output_results[node_id] = {
                "result": node.result,
                "status": node.status,
                "error": str(node.error) if node.error else None
            }
        ss=registered_logics[name_logic]
        return ss[list(ss.keys())[0]]
    
    elif request.method == 'GET':
        # Обработка GET-запроса
        return f"hi {name_logic}", 200

# Функция для разбора загруженного содержимого
def parse_uploaded_contents(contents):
    print(parse_uploaded_contents)
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    data = json.loads(decoded.decode("utf-8"))
    try:
        for key, value in data.items():
            node = OutNode(**value)
        # Parsing succeeded
        return data
    except Exception as e:
        print(e)
        print("The uploaded file could not be parsed as a flow file.")
        return {}

# Callback для выполнения нод и отображения результатов
@callback(
    [
        Output("output", "children"),
        Output("input1", "nodes_status"),
    ],
    [
        Input("run", "n_clicks"),
        State("input1", "nodes"),
    ],
)
def display_output(runclicks, nodes):
    print("display_output")
    if not nodes:
        return [], {}
    starttime = time.perf_counter()
    nodes_output = job_runner.run(nodes)
    endtime = time.perf_counter()
    outdiv = html.Div(children=[])
    for node in nodes_output.values():
        if node.error:
            outdiv.children.append(str(node.error))
        if "display" in node.type:
            outdiv.children.append(node.result)

    return outdiv, {node_id: node.status for node_id, node in nodes_output.items()}

# Callback для сохранения нод в файл
@callback(
    Output("download", "data"),
    [Input("save", "n_clicks"), State("input1", "nodes")],
    prevent_initial_call=True,
)
def func(n_clicks, nodes):
    return dict(content=json.dumps(nodes), filename="nodes.json")

# Callback для загрузки нод из файла и очистки редактора
@callback(
    [
        Output("input1", "nodes"),
        Output("input1", "editor_status"),
    ],
    [
        Input("uploader", "contents"),
        Input("clear", "n_clicks"),
        State("input1", "nodes"),
    ],
    prevent_initial_call=True,
)
def update_output(contents, nclicks, nodes):
    ctx = dash.callback_context
    if not ctx.triggered:
        return nodes, "server"
    control = ctx.triggered[0]["prop_id"].split(".")[0]
    if control == "uploader":
        newnodes = parse_uploaded_contents(contents)
        return newnodes, "server"
    return {}, "server"

# Callback для сохранения логики в registered_logics
@callback(
    Output("save-status", "children"),
    [Input("save_logic", "n_clicks"), State("input1", "nodes")],
)
def save_logic(nclicks, nodes):
    print('savel ogiv')
    name_logic=''
    method=''
    print('step1')
    for node in nodes or {}:
        print(nodes[node])
        if(nodes[node]['type']=='modules.nodeeditor.nodes_logic.nodes.response_in'):
            name_logic = nodes[node]['inputData']['name']['in_string']
            print('nosave')
            break
    if name_logic=='':
        return "Logic name is missing. Logic not saved."
    print('step2')
    registered_logics[name_logic] = nodes
    print('save')
    with open("modules/nodeeditor/registered_logics.json", "w") as f:
        json.dump(registered_logics, f)

    
    return html.Div([f"Logic '{name_logic}' saved and registered!"])

