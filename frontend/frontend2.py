import dash
import dash_core_components as dcc
import dash_html_components as html
import webbrowser
from dash.dependencies import Input, Output
import json

app = dash.Dash(__name__)

#Define HTML layout of app
app.layout = html.Div(children=[
    html.Div([
        html.H4('IoTea.', id='title'),
        html.Div(id='live-update-text'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),
        html.P(
            "  Tang Dynasty scholars believe the Gautama Buddha accidentally fell asleep meditating in front of a wall for nine years."
            " He woke up in such disgust at his weakness that he cut off his own eyelids."
            " They fell to the ground and took root, growing into tea bushes."
            " Legend says those who brew the fruit of the eyelids unlock the ability to memorise phone numbers with a 30% success rate.", id='blurb1'),
        # html.P(" Tea has played a significant role in Asian culture for centuries as a staple beverage and a curative."
        #        " At IoTea, we see it is a status symbol and a conversation starter."
        #        " Laud over your uncultured colleagues as you wrap your clammy hands around your boring novelty mug.", id='blurb2'),
        html.P(" In a world full of superfluous devices targeted at the unoriginal, that profit off your information and naïvety, you have found the only IoT device that makes you an individual."
               " Indulge yourself in this authentic moment. Laud over your uncultured colleagues as you wrap your clammy hands around your boring novelty mug.. Maybe consider buying an IoT toothbrush next?"
               " Brushing your teeth can be quite the complicated ordeal.", id='blurb3'), #EDIT
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

#Update the data to be displayed
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


#Function to update graph
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
                  "x": x,
                  "y": y,
                 'line': {'width': 0.5, 'color': 'black'}
                  }],
        "layout": {
                   "title": {"text": "Temperature vs. Time"},
                   'xaxis': {'title': "Time(s)"},
                   'yaxis': {'title': "Temperature(C)"}

                   }
    }

    return fig

#Main to launch frontend
if __name__ == '__main__':
    #open a webbrowser to the default IP adress
    webbrowser.open( 'http://127.0.0.1:8050/', new=2)

    #Launch the server
    app.run_server(debug=True)

