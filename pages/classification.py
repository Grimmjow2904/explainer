import base64
import io

import dash
import joblib
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/classification')

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 1!", className="card-text"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Tab 1"),
        dbc.Tab(tab2_content, label="Tab 2"),
        dbc.Tab(
            "This tab's content is never seen", label="Tab 3", disabled=True
        ),
    ]
)


def layout():
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(
                            ["Cargar Modelo"]
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
                    )
                ]),
                dbc.Row([
                    html.Div(id='output-data-upload')
                ])
            ], width=3),
            dbc.Col([
                dbc.Row([tabs]),
            ])
        ])
    ])

#
# @callback(Output('output-data-upload', 'children'),
#           Input('upload-data', 'contents'),
#           State('upload-data', 'filename'),
#           State('upload-data', 'last_modified'),
#           prevent_initial_call=True)
# def update_output(content, filename, date):
#     if content is not None:
#         return parse_contents(content, filename, date)
#
#
# def parse_contents(content, filename, date):
#     content_type, content_string = content.split(',')
#     decoded_model = base64.b64decode(content_string)
#     try:
#         if 'joblib' in filename:
#             # Assume that the user uploaded a joblib file
#             model = joblib.load(io.BytesIO(decoded_model))
#             # if model._estimator_type != "classifier":
#             #     raise Exception('Tipo de modelo incorrecto')
#     except Exception as e:
#         print(e)
#         return html.H6(
#             'There was an error processing this file.'
#         )
#     return html.Div([
#         html.H5(filename)
#     ])
