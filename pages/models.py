import base64
import datetime
import io
import joblib
import dash

from explainers.explainers import ClassifierExplainer

dash.register_page(__name__, path='/models')

from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

from components import dropdown
from utils import datasets

# sidebar = dbc.Nav([
#     dbc.NavLink([
#         html.Div(page["name"], className="ms-2")
#     ],
#         href=page["path"],
#         active="exact"
#     )
#     for page in dash.page_registry.values()
# ],
#     vertical=True,
#     pills=True,
#     className="bg-light"
# )

sidebar = dbc.Col([
    dropdown.template("Dataset", datasets.getDatasets()),
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
        html.Button("Print", id="print")
    ])

])

layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.Row([dbc.Col([
            sidebar
        ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.H1("Analisis del modelo"), width=10, align="center"),

                ]),
                dbc.Row(
                    [
                        dbc.Col(html.Div(id='output-data-upload')),
                    ]
                )
            ], xs=4, sm=4, md=10, lg=10, xl=10, xxl=10), ]),

    ]
)


#
# @callback(Output("page-content", "children"), Input("url", "pathname"))
# def render_page_content(pathname):
#     if pathname == "/models":
#         return html.P("This is the content of the home page!")
#     elif pathname == "/models/matrix":
#         return html.P("This is the content of page 1. Yay!")
#     elif pathname == "/models/roc":
#         return html.P("Oh cool, this is page 2!")
#     # If the user tries to reach a different page, return a 404 message
#     return html.Div(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ],
#         className="p-3 bg-light rounded-3",
#     )


@callback(Output('output-data-upload', 'children'),
          Input('upload-data', 'contents'),
          Input('Dataset-dropdown', 'value'),
          State('upload-data', 'filename'),
          State('upload-data', 'last_modified'),
          prevent_initial_call=True)
def update_output(content, dataset, filename, date):
    if content is not None:
        return parse_contents(content, dataset, filename, date)


def parse_contents(content, dataset, filename, date):
    content_type, content_string = content.split(',')
    decoded_model = base64.b64decode(content_string)
    file = io.BytesIO(decoded_model)
    try:
        if 'joblib' in filename:
            # Assume that the user uploaded a joblib file
            model = joblib.load(file)

    except Exception as e:
        print(e)
        return html.H6(
            'There was an error processing this file.'
        )

    explainer = ClassifierExplainer(model, datasets.getDataset(dataset))
    sharp = explainer.shap()
    confux = explainer.confusion_matrix()
    roc = explainer.roc_auc_curve()

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date).strftime("%m/%d/%Y, %H:%M:%S")),
        confux,
        roc,
        sharp
    ])
