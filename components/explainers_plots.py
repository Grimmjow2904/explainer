from dash import dcc, callback, Output, Input, State, html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px


class Plot:
    def graph(self) -> dcc.Graph:
        pass


class PlotlyConfusionMatrix(Plot):

    def __init__(self, cm, labels, annotations):
        self.cm = cm
        self.labels = labels
        self.annotations = annotations

    def graph(self):
        try:
            fig = px.imshow(self.cm, x=self.labels, y=self.labels, color_continuous_scale='Blues', aspect="auto")
            fig.update_traces(text=self.annotations, texttemplate="%{text}")
            fig.update_xaxes(side="top")
            fig.update_layout(title="Matriz de Confusion")
        except Exception as error:
            print("An exception occurred:", error)
            return

        return dcc.Graph(figure=fig)


class PlotlyRocCurve(Plot):

    def __init__(self, data):
        self.data = data

    def graph(self):
        fig = go.Figure()
        fig.add_shape(
            type='line', line=dict(dash='dash'),
            x0=0, x1=1, y0=0, y1=1
        )
        for i in range(len(self.data)):
            fig.add_trace(go.Scatter(x=self.data[i][1], y=self.data[i][2], name=self.data[i][0], mode='lines'))

        fig.update_layout(
            title="Curva ROC",
            xaxis_title='Falsos Positivos',
            yaxis_title='Verdaderos Positivos',
            # yaxis=dict(scaleanchor="x", scaleratio=1),
            # xaxis=dict(constrain='domain'),
            legend_title_text="Atributos",
            legend=dict(orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1)
        )
        return dcc.Graph(figure=fig)
