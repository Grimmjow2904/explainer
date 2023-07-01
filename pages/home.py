import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

from dash import html

layout = dbc.Row([
    dbc.Col([
        dbc.Row([dbc.Card(
            [
                dbc.CardImg(src="../assets/img/clasificacion.png", top=True),
                dbc.CardBody(
                    [
                        html.H4("Clasificacion", className="card-title"),
                        html.P(
                            "Cuando usamos clasificación, el resultado es una clase, entre un número limitado de clases. Con clases nos referimos a categorías arbitrarias según el tipo de problema.",
                            className="card-text",
                        ),
                        dbc.Button([dbc.NavLink([
                            html.Div("Analizar", className="ms-2 ")
                        ], href="/classification")], color="primary"),
                    ]
                    , className="d-flex flex-column"),
            ],
            style={"width": "20rem"},
        )], justify="center")
    ]),
    dbc.Col([
        dbc.Row([
            dbc.Card(
                [
                    dbc.CardImg(src="../assets/img/regresion.gif", top=True),
                    dbc.CardBody(
                        [
                            html.H4("Regresion", className="card-title"),
                            html.P(
                                "Cuando usamos regresión, el resultado es un número. Es decir, el resultado de la técnica de machine learning que estemos usando será un valor numérico, dentro de un conjunto infinito de posibles resultados.",
                                className="card-text",
                            ),
                            dbc.Button([dbc.NavLink([
                                html.Div("Analizar", className="ms-2")
                            ], href="/regression")], color="primary"),
                        ], className="d-flex flex-column"),
                ],
                style={"width": "20rem"},
            )], justify="center")
    ])
])
