import base64
import datetime
import io
import joblib

import dash

dash.register_page(__name__, path='/models')

from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

layout = html.Div(
    [
        dbc.Row([
            dbc.Col(html.H1("Analisis del modelo"), width=10),
            dbc.Col(dcc.Upload(
                id="upload-data",
                children=html.Div(
                    ["Cargar"]
                ),
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                },
                multiple=False,
            ))
        ]),
        dbc.Row(
            [
                dbc.Col(html.Div(id='output-data-upload')),

            ]
        ),
    ]
)


@callback(Output('output-data-upload', 'children'),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'),
          State('upload-data', 'last_modified'))
def update_output(content, filename, date):
    if content is not None:
        return parse_contents(content, filename, date)


def parse_contents(content, filename, date):
    content_type, content_string = content.split(',')
    decoded_model = base64.b64decode(content_string)
    try:
        if 'joblib' in filename:
            # Assume that the user uploaded a joblib file
            model = joblib.load(io.BytesIO(decoded_model))

    except Exception as e:
        print(e)
        return html.H6(
            'There was an error processing this file.'
        )

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
    ])
