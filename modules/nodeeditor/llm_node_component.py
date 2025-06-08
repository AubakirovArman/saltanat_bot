from dash import html, dcc
from extended_flowfunc.components import Component


class LLMNode(Component):
    """UI component for an LLM node in the Flowfunc editor."""

    def __init__(self, component_id: str = "llm-node"):
        super().__init__(component_id)
        self.component_id = component_id

    def layout(self) -> html.Div:
        """Return Dash layout for the node."""
        header = html.Div(
            [html.Span("\ud83e\udde0 LLM Node", className="fw-bold")],
            className="p-2 text-white",
            style={"background": "#4B5AA6", "borderRadius": "8px 8px 0 0"},
        )

        prompt = dcc.Textarea(
            id=f"{self.component_id}-prompt",
            placeholder="Enter your prompt...",
            className="form-control",
            style={"resize": "vertical"},
        )

        temp_slider = html.Div(
            [
                html.Small("Temperature"),
                dcc.Slider(
                    id=f"{self.component_id}-temperature",
                    min=0,
                    max=1,
                    step=0.05,
                    value=0.7,
                ),
            ],
            className="my-2",
        )

        model_dropdown = dcc.Dropdown(
            id=f"{self.component_id}-model",
            options=[
                {"label": "gpt-3.5-turbo", "value": "gpt-3.5-turbo"},
                {"label": "gpt-4", "value": "gpt-4"},
            ],
            value="gpt-3.5-turbo",
            clearable=False,
            className="mb-2",
        )

        response_area = html.Div(id=f"{self.component_id}-response", className="mt-2")

        body = html.Div(
            [prompt, temp_slider, model_dropdown, response_area],
            className="p-3",
        )

        return html.Div(
            [header, body],
            className="shadow",
            style={
                "width": "260px",
                "background": "#F9F9F9",
                "borderRadius": "8px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.15)",
            },
        )
