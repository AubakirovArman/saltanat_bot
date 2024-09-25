from typing import Any, Dict, Tuple
from enum import Enum

import dash
from dash import html, Input, Output, State
from flowfunc import Flowfunc
from flowfunc.config import Config
from flowfunc.jobrunner import JobRunner
from flowfunc.models import OutNode, Control, ControlType

app = dash.Dash(__name__)

class ComparisonOperation(str, Enum):
    """Перечисление доступных операций сравнения"""
    РАВНО = "=="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_THAN_OR_EQUAL = ">="
    LESS_THAN_OR_EQUAL = "<="

# Модернизированная функция calculate с дополнительными операциями сравнения
def calculate(a: int, b: int, operation: ComparisonOperation) -> bool:
    """Выполняет выбранную операцию над двумя числами"""

    if operation == ComparisonOperation.РАВНО:
        return a == b
    elif operation == ComparisonOperation.GREATER_THAN:
        return a > b
    elif operation == ComparisonOperation.LESS_THAN:
        return a < b
    elif operation == ComparisonOperation.GREATER_THAN_OR_EQUAL:
        return a >= b
    elif operation == ComparisonOperation.LESS_THAN_OR_EQUAL:
        return a <= b
    else:
        print(f"Warning: Unsupported operation '{operation}'")
        return None

# Функция process_two_inputs с двумя входами и двумя выходами
def process_two_inputs(input1: Any, input2: Any) -> Tuple[Any, Any]:
    """
    Обрабатывает два входных значения и возвращает два выходных значения.

    Args:
        input1: Первое входное значение любого типа.
        input2: Второе входное значение любого типа.

    Returns:
        Кортеж из двух значений, представляющих результаты обработки входных данных.
    """

    # Здесь вы можете реализовать любую логику обработки входных данных
    # и формирования выходных значений.
    # В данном примере просто возвращаем входные значения без изменений.

    return input1, input2

# Обновление конфигурации для использования обеих функций
nodeeditor_config = Config.from_function_list([calculate, process_two_inputs])
runner = JobRunner(nodeeditor_config)

app.layout = html.Div(
    [
        html.Button(id="btn_run", children="Run"),
        Flowfunc(id="nodeeditor", config=nodeeditor_config.dict()),
        html.Div(id="output"),
    ], style={"height": "600px"}
)


@app.callback(
    Output("output", "children"),
    Input("btn_run", "n_clicks"),
    State("nodeeditor", "nodes"),
)
def run_nodes(nclicks: int, output_nodes: Dict[str, OutNode]):
    """Run the node layout"""
    # The result is a dictionary of OutNode objects
    result = runner.run(output_nodes)
    output = []
    for node in result.values():
        # node.result contains the result of the node
        output.append(
            html.Div([html.H1(f"{node.type}: {node.id}"), html.P(str(node.result))])
        )
    return output

if __name__ == "__main__":
    app.run() 