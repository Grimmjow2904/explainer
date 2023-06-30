import dash_bootstrap_components as dbc
from dash import html, dcc


def template(label, options, value=None):
    return dbc.Row([
        html.Label(label),
        dcc.Dropdown(
            options=options,
            value=value,
            id=f'{label}-dropdown',
            multi=False
        )
    ])
