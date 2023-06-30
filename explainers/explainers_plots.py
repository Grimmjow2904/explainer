from dash import dcc, callback, Output, Input, State, html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import plotly.express as px


def plotly_confusion_matrix(cm, labels, annotations):
    try:
        fig = px.imshow(cm, x=labels, y=labels, color_continuous_scale='Viridis', aspect="auto")
        fig.update_traces(text=annotations, texttemplate="%{text}")
        fig.update_xaxes(side="top")
    except Exception as error:
        print("An exception occurred:", error)
        return

    return dcc.Graph(figure=fig)


def plotly_roc_curve(data):
    fig = go.Figure()
    fig.add_shape(
        type='line', line=dict(dash='dash'),
        x0=0, x1=1, y0=0, y1=1
    )
    for i in range(len(data)):
        fig.add_trace(go.Scatter(x=data[i][1], y=data[i][2], name=data[i][0], mode='lines'))

    fig.update_layout(
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        yaxis=dict(scaleanchor="x", scaleratio=1),
        xaxis=dict(constrain='domain'),
        height=500
    )
    return dcc.Graph(figure=fig)
