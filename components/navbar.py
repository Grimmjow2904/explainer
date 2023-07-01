import dash_bootstrap_components as dbc

template = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Modelos", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Datasets", href="/datasets"),
                dbc.DropdownMenuItem("Exportar", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="Mas",
        ),
    ],
    brand="Analisis de Redes Neuronales",
    brand_href="/",
    color="primary",
    dark=True,
    sticky=True
)
