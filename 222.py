from dash_flow_diagrams import DashFlow, MiniMap, Background, Controls
from dash import Output, Input, callback, Dash, html


app = Dash(__name__)

app.layout = html.Div([
    DashFlow(
        id='flow',
        children=[
            MiniMap(),
            Controls(),
            Background(),
        ],
        nodes=[
            {
                "id": '1',
                "data": {
                    "html": """<div style="height: 50px; border: 1px solid #eee; padding: 5px; borderRadius: 5px; background: white">
                        <span style="fontSize: 10px; fontWeight: bold; color: red">zipcode</span>
                        <br/>
                        <span>dbo.addresses</span>
                        <div data-handlepos="right" class="react-flow__handle react-flow__handle-right source"></div>
                        </div>
                        """,
                },
                "type": 'customNode',
                "position": { "x": 250, "y": 0 },
                "sourcePosition": 'right',
                "targetPosition": 'left',
                "width": 150,
                "height": 35,
            },
            {
                "id": '2',
                "data": {
                    "label": "Default Node",
                },
                "position": { "x": 100, "y": 100 },
                "sourcePosition": 'right',
                "targetPosition": 'left',
                "width": 150,
                "height": 35,
            },
            {
                "id": '3',
                "data": {
                    "label": 'Heyyy',
                },
                "position": { "x": 300, "y": 100 },
                "sourcePosition": 'right',
                "targetPosition": 'left',
                "width": 150,
                "height": 35,
            },
        ],
        edges=[
            {"id": 'e1-2', "source": '1', "target": '2', "label": 'process', "type": "step"},
            {"id": 'e1-3', "source": '1', "target": '3', "animated": True, "label": 'process 1-3'},
        ],
        dagre_direction="LR",
    ),
    html.Div(id='output')
], style={"width": "800px", "height": "600px"})


@callback(
    Output('output', 'children'),
    Input('flow', 'clickedNode'),
    Input('flow', 'clickedEdge'),
    Input('flow', 'connectedEdge')
)
def display_output(clickedNode, clickedEdge, connectedEdge):
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'flow':
        if clickedNode:
            print(clickedNode)
            return str(clickedNode)
        elif clickedEdge:
            print(clickedEdge)
            return str(clickedEdge)
        elif connectedEdge:
            print(connectedEdge)
            return str(connectedEdge)
    else:
        return "No interaction yet" 


if __name__ == '__main__':
    app.run_server(debug=True)