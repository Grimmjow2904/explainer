import dash_bootstrap_components as dbc

template = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Modelos", href="/models")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Opciones", header=True),
                dbc.DropdownMenuItem("Exportar", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Analisis de Redes Neuronales",
    brand_href="/",
    color="primary",
    dark=True,
    sticky=True
)
