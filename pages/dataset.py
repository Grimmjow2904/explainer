import dash

dash.register_page(__name__, path='/dataset')

from dash import html

layout = html.Div(children=[
    html.H1(children="Dataset")
])
