from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from components import dropdown
from utils import datasets

sidebar = dbc.Col([
    dropdown.template("Dataset", datasets.getDatasets()[0]),
    html.Label("Modelo"),
    dbc.Row(dcc.Upload(
        id="upload-data",
        children=html.Div(
            ["Cargar"]
        ),
        style={
            "cursor": "pointer",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
        },
        multiple=False,
    )),
    dbc.Row([
        html.Button("Print", id="print", className="btn btn-primary w-50")
    ], justify="center")

])
