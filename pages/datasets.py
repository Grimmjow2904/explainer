import dash
import pandas as pd
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/datasets')

from dash import html, callback, Output, Input, State, dcc, no_update
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
                dbc.Button("Agregar", id="open-dataset-modal")
            ], className="w-25 ")
        ], className="d-flex justify-content-end")
    ], className="justify-content-between p-3"),
    dbc.Row([
        dbc.Col([grid]),
        dbc.Col([
            html.Div(id="dataset_contend")
        ])
    ]),
    dbc.Modal(
        [
            dbc.Toast([],
                      id="success-toast",
                      header="Subida",
                      icon="primary",
                      duration=3000,
                      is_open=False,
                      style={"position": "fixed", "top": 66, "right": 10, "width": 350},
                      ),
            dbc.ModalHeader(dbc.ModalTitle("Agregar dataset")),
            dbc.ModalBody([
                dcc.Upload(
                    id="upload-dataset",
                    children=html.Div(
                        ["Cargar"]
                    ),
                    style={
                        "cursor": "pointer",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                    },
                    multiple=False,
                )
            ]),
            dbc.ModalFooter(
                dbc.Button(
                    "Cerrar", id="close-dataset-modal", className="ms-auto", n_clicks=0
                )
            ),
        ],
        id="modal",
        is_open=False,
    ),

])


@callback(
    Output("modal", "is_open"),
    [Input("open-dataset-modal", "n_clicks"), Input("close-dataset-modal", "n_clicks")],
    [State("modal", "is_open")],
    config_prevent_initial_callbacks=True
)
def toggle_modal(n1, n2, is_open):
    return not is_open


@callback(Output("upload-dataset", "children"),
          Output("success-toast", "is_open"),
          Output("success-toast", "children"),
          Output("dataset_grid", "rowData"),
          Input('upload-dataset', 'contents'),
          State('upload-dataset', 'filename'),
          config_prevent_initial_callbacks=True)
def save_file(content, name):
    if datasets.save_dataset(name, content):
        datasetsData = datasets.getDatasets()

        data = {
            "name": datasetsData[0],
            "target": datasetsData[1],
            "delete": ["Delete" for _ in range(len(datasetsData[0]))],
        }
        return name, True, html.P("Archivo subido con exito", className="mb-0"), pd.DataFrame(data).to_dict("records")
    else:
        return name, True, html.P("Error al subir el archivo", className="mb-0")
