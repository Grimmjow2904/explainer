import base64
import datetime
import io
import joblib
import dash

dash.register_page(__name__, path='/classification')

from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

from utils import datasets
from explainers.explainers import ClassifierExplainer
from components.sidebar import sidebar

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
                        dcc.Tabs(id="tabs-example-graph", value='tab-metrics', children=[
                            dcc.Tab(label='Metricas', value='tab-metrics', id="metrics"),
                            dcc.Tab(label='SHAP', value='tab-SHAP', id="SHAP"),
                            dcc.Tab(label='LIME', value='tab-LIME', id="LIME"),
                        ]),
                    ])
                    ]
                )
            ], xs=4, sm=4, md=10, lg=10, xl=10, xxl=10), ]),

    ]
)


@callback(Output('metrics', 'children'),
          Output('SHAP', 'children'),
          Output('LIME', 'children'),
          Input('upload-data', 'contents'),
          State('Dataset-dropdown', 'value'),
          State('upload-data', 'filename'),
          State('upload-data', 'last_modified'),
          prevent_initial_call=True)
def model_load(content, dataset, filename, date):
    if content is not None:
        metrics, shap, lime = parse_contents(content, dataset, filename, date)
        return metrics, shap, lime


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
    metrics = []
    shap = explainer.shap()
    confux = dbc.Row([
        dbc.Col([explainer.confusion_matrix()]),
        dbc.Col("test")
    ])
    metrics.append(confux)
    roc = dbc.Row([
        dbc.Col([explainer.roc_auc_curve()]),
        dbc.Col("test")
    ])
    metrics.append(roc)
    # plio.write_image(explainer.confusion_matrix(), "../assets/test.pdf", format='pdf')
    # TODO: do lime
    return metrics, shap, html.Div("Aqui va lime")
