# import os
#
# import dash
# import dash_core_components as dcc
# import dash_html_components as html

import os.path
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
#import scipy
from scipy import io
import numpy as np
import rpca

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
PLOT_TYPE = ['X-component velocity', 'Y-component velocity', 'Velocity magnitude', ' Vorticity']

server = app.server

app.layout = html.Div([


html.Div([
    html.H2('PIView', id='title'),
    html.Img(src="http://www.arianamendible.com/images/bitmap.png", style={'height':120}})#bitmap.png
], className="banner", style={'backgroundColor':'darkslategray'}),

            html.Div([

                # dropdown
                html.Div([
                    #html.Label('Component to plot:'),
                    dcc.Dropdown(
                        id='crossfilter-yaxis-column',
                        options=[{'label':i, 'value':i} for i in PLOT_TYPE],
                        placeholder='Select the component to plot'
                    ),
                ], style={'width':'30%', 'display':'inline-block',
                          'margin':'auto', 'vertical-align':'bottom'}),

                #slider bar for lambda value
                html.Div([
                    #html.Label('Scale for \u03bb'),
                    html.Div(id='lambda-slider-output',
                             style={'textAlign':'center', 'marginTop':40, 'fontSize':16}),
                    html.Div([
                        dcc.Slider(
                            id='lambda-slider',
                            marks={i: '{}'.format(10 ** i/10) for i in range(3)},
                            max=2,
                            value=2,
                            step=0.1,
                            updatemode='mouseup',
                            included=False
                        )
                    ], style={'marginTop':25}),
                ], style={'width':'30%', 'display':'inline-block', 'margin-left':50}),
            ], style={'textAlign':'center'}),


            #run rpca button and plot button
            html.Div([
                html.Div([html.Button('Run RPCA', id='rpca-button'),
                          html.Div(id='rpca-output-container-button',
                                   style={'margin-top':20})],
                         style={'width':'30%', 'padding':'10px 10px', 'display':'inline-block'}),
                html.Div([html.Button('Plot RPCA', id='plot-button'),
                          html.Div(id='plot-output-container-button',
                                   style={'margin-top':20})],
                         style={'width':'30%', 'marginLeft':50, 'padding':'10px 10px',
                                'display':'inline-block', 'vertical-align':'top'}),
            ], style={'padding':'30px 30px', 'textAlign':'center'}),


        ], style={
            'border': 'thin lightgrey solid',
            'backgroundColor':'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),

    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
