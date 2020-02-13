import dash
import dash_core_components as dcc
import dash_html_components as html
import webbrowser
from dash.dependencies import Input, Output
import json

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
    try:
        with open('data.txt') as json_file:
                data = json.load(json_file)
        output = []
        if data['state'] == 'nodata':
            output = [html.Div('We have yet to receive data', id='display')]
        elif data['state'] == 'rising':
            sentiment = data['sentiment']
            output = [html.Div('Our temperature sensor is heating up', id='display'),
                      html.Div('We\'d give your conversation a {0:0.2f}.'.format(sentiment), id='display')
                      ]
        elif data['state'] == 'ready':
            time_left = data['time_left']
            current_temp = data['current_temp']
            sentiment = data['sentiment']
            output = [html.Div('Your tea is at {0:.1f} C.'.format(current_temp), id='display'),
                      html.Div('You should finish your tea in {0:.0f} minutes.'.format(time_left), id='display'),
                      html.Div('We\'d give your conversation a {0:0.2f}.'.format(sentiment), id='display')]
        else:
            current_temp = data['current_temp']
            sentiment = data['sentiment']
            output = [html.Div('Your tea is at {0:.1f} C.'.format(current_temp), id='display'),
            html.Div('We would not recommend drinking your tea. Make another!', id='display'),
            html.Div('We\'d give your conversation a {0:0.2f}.'.format(sentiment), id='display')]
    except:
        output = [html.Div('We have yet to receive data', id='display')]

    return output


@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    username = {}
    username['user'] = value

    with open('output.txt', 'w') as file:
        file.write(json.dumps(username))

    return 'The input value was "{}" and the button has been clicked {} times'.format(value, n_clicks)


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    try:
        with open('data.txt') as json_file:
            data = json.load(json_file)
            if data['state'] != 'nodata':
                x = data['times']
                y = data['temps']
            else:
                x = [0]
                y = [0]
    except:
        x = [0]
        y = [0]


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
    #open a webbrowser to the default IP adress
    webbrowser.open( 'http://127.0.0.1:8050/', new=2)
    #Launch the server
    app.run_server(debug=True)

