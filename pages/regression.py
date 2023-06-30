import dash
from dash import html

dash.register_page(__name__, path='/regression')


def layout():
    return html.Div("Regresion")
