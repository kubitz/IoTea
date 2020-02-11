import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly


from dash.dependencies import Input, Output
import json


import os
temp = 22

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.Div([
        html.H4('IoTea.', id='title'),
        html.Div(id='live-update-text'),
        html.Div(dcc.Input(id='input-box', type='text')),
        html.Button('Submit', id='button'),
        html.Div(id='output-container-button',
                 children='Enter a value and press submit'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),
        dcc.Checklist(
            options=[
                {'label': 'I agree to the terms and conditions', 'value': 'NYC'},
            ],
            value=['MTL', 'SF']
        )
    ], id='container'),
    html.Div([dcc.Graph(id='live-update-graph')])
    ]
)

@app.callback(Output('live-update-text', 'children'),
              [Input( 'interval-component', 'n_intervals')])
def update_metrics(n):
    with open('data.txt') as json_file:
        data = json.load(json_file)
        for p in data['temp']:
            temp = p["Temperature"]

    lon, lat, alt = temp,3,4

    return [
        html.Div('Your tea is at {0:.1f} C.'.format(lon), id = 'display'),
        html.Div('You should finish your tea in {0:.0f} minutes.'.format(lat), id = 'display'),
        html.Div('We\'d give your conversation a {0:0.0f}.'.format(alt), id = 'display')
    ]

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    x = [1,2,4]
    y = [1,2,4]
    # Create the graph with subplots
    fig = {
        "data": [{"type": "line",
                  "x":x ,
                  "y":y}],
        "layout": {"title": {"text": "Temperature vs. Time"},
                   'xaxis': {'title': "Time(s)"},
                   'yaxis': {'title': "Temperature(C)"}
                   }
    }

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

