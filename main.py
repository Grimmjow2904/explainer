from dash import html, dcc, Output, Input
import dash
import dash_bootstrap_components as dbc
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings

warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

from components import navbar

scripts = [{
    'src': 'https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js'
}]

# prevent callback at launch
app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                use_pages=True,
                external_stylesheets=[dbc.themes.FLATLY], external_scripts=scripts)

app.layout = dbc.Container([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id='store'),
    dbc.Row([
        navbar.template,
        dbc.Col(
            html.Div("", style={'fontSize': 50, "textAlign": 'center'})
        )
    ]),
    html.Hr(),
    dbc.Row([
        dash.page_container
    ]),

], fluid=True, style={"height": "100vh"})

app.clientside_callback(
    """
function nClicksToPDF(n_clicks){
  if(n_clicks > 0){
    
    const opt = {
      margin: 2,
      filename: 'myfile.pdf',
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 1},
      jsPDF: { unit: 'cm', format: 'a2', orientation: 'p' },
      pagebreak: { mode: ['avoid-all'] }
    };
    console.log('ok')

    html2pdf().from(document.getElementById("output-data-upload")).set(opt).save();
  }
}
    """,
    Output('print', 'disable'),
    Input('print', 'n_clicks')
)

if __name__ == "__main__":
    app.run_server(debug=True)
