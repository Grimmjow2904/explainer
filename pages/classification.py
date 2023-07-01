import base64
import datetime
import io
import joblib
import dash

from explainers.explainers import ClassifierExplainer

dash.register_page(__name__, path='/classification')

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

layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id='model-value'),
        dbc.Row([dbc.Col([
            sidebar
        ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.H1("Analisis del modelo"), width=10, align="center"),

                ]),
                dbc.Row(
                    [dcc.Loading([
                        dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
                            dcc.Tab(label='Tab One', value='tab-1-example-graph', id="matriz"),
                            dcc.Tab(label='Tab Two', value='tab-2-example-graph', id="ROC"),
                        ]),
                    ])
                    ]
                )
            ], xs=4, sm=4, md=10, lg=10, xl=10, xxl=10), ]),

    ]
)


@callback(Output('matriz', 'children'),
          Output('ROC', 'children'),
          Input('upload-data', 'contents'),
          State('Dataset-dropdown', 'value'),
          State('upload-data', 'filename'),
          State('upload-data', 'last_modified'),
          prevent_initial_call=True)
def update_output(content, dataset, filename, date):
    if content is not None:
        matriz, roc = parse_contents(content, dataset, filename, date)
        return matriz, roc


def parse_contents(content, dataset, filename, date):
    try:
        if filename.endswith(".joblib"):
            content_type, content_string = content.split(',')
            decoded_model = base64.b64decode(content_string)
            file = io.BytesIO(decoded_model)
            model = joblib.load(file)

    except Exception as e:
        print(e)

    explainer = ClassifierExplainer(model, datasets.getDataset(dataset))
    # sharp = explainer.shap()
    confux = explainer.confusion_matrix()
    roc = explainer.roc_auc_curve()
    return confux, roc
