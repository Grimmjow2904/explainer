import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

from dash import html

layout = dbc.Row([
    dbc.Col([
        dbc.Card(
            [
                dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
                dbc.CardBody(
                    [
                        html.H4("Clasificacion", className="card-title"),
                        html.P(
                            "Some quick example text to build on the card title and "
                            "make up the bulk of the card's content.",
                            className="card-text",
                        ),
                        dbc.Button([dbc.NavLink([
                            html.Div("Analizar", className="ms-2")
                        ], href="/classification")], color="primary"),
                    ]
                ),
            ],
            style={"width": "18rem"},
        )
    ]),
    dbc.Col([
        dbc.Card(
            [
                dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
                dbc.CardBody(
                    [
                        html.H4("Regresion", className="card-title"),
                        html.P(
                            "Some quick example text to build on the card title and "
                            "make up the bulk of the card's content.",
                            className="card-text",
                        ),
                        dbc.Button([dbc.NavLink([
                            html.Div("Analizar", className="ms-2")
                        ], href="/regression")], color="primary"),
                    ]
                ),
            ],
            style={"width": "18rem"},
        )
    ])
])
