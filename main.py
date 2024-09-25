import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_bootstrap_components as dbc
from ui.navbar import navbar
from flask import request
from modules.nodeeditor import nodes
from modules import charts

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE], suppress_callback_exceptions=True)
server = app.server

server.register_blueprint(nodes.bp)

# Интерфейс редактора нод

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Container(navbar),
    dbc.Container(html.Div(id='content'))
])


@app.callback(
    Output('content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    print(pathname)
    if pathname in ['/','']:
        return "пока тут пусто"
    elif pathname =='/nodes':
        return nodes.page   
    elif pathname =='/charts':
        return charts.page     
    else:
        return "error"

@server.route('/inpu/aaaa', methods=['POST'])
def handle_post_request():
    if request.method == 'POST':
        data = request.get_json()  # Получаем JSON данные из запроса
        print(f"Received data: {data}")
        return {'status': 'success', 'message': 'Data received successfully'}, 200


if __name__ == "__main__":
    app.run_server(debug=True)
