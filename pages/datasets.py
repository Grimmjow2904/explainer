import os
import dash
import pandas as pd
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/datasets')

from dash import html, callback, Output, Input
from enviroment import settings

file_names = os.listdir(settings.data_path)

data = {
    "name": file_names,
    "description": file_names,
    "buy": ["Buy" for _ in range(len(file_names))],
    "sell": ["Sell" for _ in range(len(file_names))],
}
df = pd.DataFrame(data)

columnDefs = [
    {
        "headerName": "Nombre",
        "field": "name",
    },
    {
        "headerName": "Descripcion",
        "type": "rightAligned",
        "field": "description",
        "valueFormatter": {"function": """d3.format("($,.2f")(params.value)"""},
    },
    {
        "field": "Ver",
        "cellRenderer": "DMC_Button",
        "cellRendererParams": {
            "variant": "outline",
            "leftIcon": "ic:baseline-shopping-cart",
            "color": "green",
            "radius": "xl"
        },
    },
    {
        "field": "buy",
        "cellRenderer": "Button",
        "cellRendererParams": {"className": "btn btn-success"},
    },

]

defaultColDef = {
    "resizable": True,
    "sortable": True,
    "editable": False,
}

grid = dag.AgGrid(
    id="dataset_grid",
    columnDefs=columnDefs,
    rowData=df.to_dict("records"),
    columnSize="autoSize",
    defaultColDef=defaultColDef,
    dashGridOptions={"rowSelection": "single"},
)


@callback(
    Output("dataset_contend", "children"), Input("dataset_grid", "cellClicked"), prevent_initial_call=True
)
def display_cell_clicked_on(cell):
    index = cell['rowIndex']

    df = pd.read_csv(
        settings.data_path + "//" + file_names[index]
    )

    columnDefs = [{"field": t} for t in df.columns]

    if cell is None:
        return "Click on a cell"
    return dag.AgGrid(
        id="selection-single-grid",
        columnDefs=columnDefs,
        rowData=df.to_dict("records"),
        columnSize="sizeToFit",
        defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth": 125},
        dashGridOptions={"rowSelection": "single"},
    )
    # return f"clicked on cell value:  {cell['value']}, column:   {cell['colId']}, row index:   {cell['rowIndex']}"


layout = html.Div(children=[
    dbc.Row([
        dbc.Col([html.H1(children="Datasets")], width=5),
        dbc.Col([
            dbc.Row([
                dbc.Button("Agregar")
            ])
        ], align="center", width=1)
    ], justify="rigth"),
    dbc.Row([
        dbc.Col([grid]),
        dbc.Col([
            html.Div(id="dataset_contend")
        ])
    ])

])
