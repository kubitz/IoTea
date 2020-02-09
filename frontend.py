import datetime
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
# import plotly
from dash.dependencies import Input, Output
import paho.mqtt.client as mqtt
import json

temp = 22

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Your IOTea Data'),
        html.Div(id='live-update-text'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    with open('data.txt') as json_file:
        data = json.load(json_file)
        for p in data['temp']:
            temp = p["Temperature"]

    lon, lat, alt = temp,3,4
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Temperature: {0:.3f}'.format(lon), style=style),
        html.Span('Time until cool: {0:.2f}'.format(lat), style=style),
        html.Span('Quality of conversation: {0:0.2f}'.format(alt), style=style)
    ]

if __name__ == '__main__':
    app.run_server(debug=True)

