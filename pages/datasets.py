import dash
import pandas as pd
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/datasets')

from dash import html, callback, Output, Input
from enviroment import settings
from utils import datasets

datasetsData = datasets.getDatasets()

data = {
    "name": datasetsData[0],
    "target": datasetsData[1],
    "delete": ["Delete" for _ in range(len(datasetsData[0]))],
}

columnDefs = [
    {
        "headerName": "Nombre",
        "field": "name",
    },
    {
        "headerName": "Objetivo",
        "type": "rightAligned",
        "field": "target",
    },
    {
        "field": "Eliminar",
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
    rowData=pd.DataFrame(data).to_dict("records"),
    columnSize="sizeToFit",
    defaultColDef=defaultColDef,
    dashGridOptions={"rowSelection": "single"},
)


@callback(
    Output("dataset_contend", "children"), Input("dataset_grid", "cellClicked"), prevent_initial_call=True
)
def display_cell_clicked_on(cell):
    index = cell['rowIndex']

    df = pd.read_csv(
        settings.data_path + "//" + datasetsData[0][index]
    )

    columns = [{"field": t} for t in df.columns]

    if cell is None:
        return "Click on a cell"
    return dag.AgGrid(
        id="selection-single-grid",
        columnDefs=columns,
        rowData=df.to_dict("records"),
        columnSize="sizeToFit",
        defaultColDef={"resizable": True, "sortable": True, "filter": True, "minWidth": 125},
        dashGridOptions={"rowSelection": "single"},
    )
    # return f"clicked on cell value:  {cell['value']}, column:   {cell['colId']}, row index:   {cell['rowIndex']}"


layout = html.Div(children=[
    dbc.Row([
        dbc.Col([html.H1(children="Datasets")]),
        dbc.Col([
            dbc.Row([
                dbc.Button("Agregar")
            ], align="end", className="w-25")
        ])
    ], className="justify-content-between p-3"),
    dbc.Row([
        dbc.Col([grid]),
        dbc.Col([
            html.Div(id="dataset_contend")
        ])
    ])

])
