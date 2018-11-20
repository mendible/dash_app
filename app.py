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

    # html.Div([
    #     html.Img(src=app.get_asset_url('PIView.png'),
    #              style={'height':'100px', 'display':'inline-block', 'padding':'0px 20px'}),
    # ]),
    #
    # html.Div([
    #     html.Div('PIView', style={'font-family':'helvetica',
    #                               'textAlign':'center', 'fontSize':'72px'}),
    # ], style={'marginBottom':50, 'marginTop':25}),
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value'),

    html.Div([
        html.H2('PIView', id='title'),
        html.Img(src="http://www.arianamendible.com/images/bitmap.png")#bitmap.png
    ], className="banner", style={'backgroundColor':'darkslategray'}),


    # header seaction
    html.Div(className="container", children=[
        html.Div([
            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '30%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': 'auto'
                        }),
            ], style={'margin':'auto', 'textAlign':'center'}),

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

        # graphs section
        html.Div([
            html.Div([
                dcc.Graph(id='full-data-plot')
            ], style={'width': '30%', 'display': 'inline-block', 'padding':'10 10'}),

            html.Div([
                dcc.Graph(id='low-rank-data-plot')
            ], style={'width': '30%', 'display': 'inline-block', 'padding':'10 10'}),

            html.Div([
                dcc.Graph(id='sparse-data-plot')
            ], style={'width': '30%', 'display': 'inline-block', 'padding':'10 10'}),
        ], style={'textAlign': 'center'}),

        # save movie button
        html.Div([
            dcc.Input(id='video-filename', type='text',
                      placeholder='Video file name', debounce=True),
            dcc.RadioItems(id='vid-file-type',
                           options=[{'label': ' .mp4 ', 'value': '.mp4'},
                                    {'label': ' .avi ', 'value': '.avi'},
                                    {'label': ' .gif ', 'value': '.gif'}
                                   ],
                           labelStyle={'display': 'inline-block'}),
            html.Button('Save Video', id='save-video-button'),
        ], style={'width':'30%', 'display':'inline-block', 'margin-bottom':30, 'margin-left':50}),

        html.Div(id='output-video-button', style={'margin-top':20, 'display':'inline-block'}),

        html.Div(id='video-output-container-button',
                 style={'margin-top':20, 'display':'inline-block'}),
    ]),
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
EXTERNAL_CSS = [
    # Normalize the CSS
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
    # Fonts
    "https://fonts.googleapis.com/css?family=Open+Sans|Roboto"
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    # For production
    "https://cdn.rawgit.com/xhlulu/0acba79000a3fd1e6f552ed82edb8a64/raw/dash_template.css",
    # Custom CSS
    "https://cdn.rawgit.com/xhlulu/dash-image-processing/1d2ec55e/custom_styles.css",
]

for css in EXTERNAL_CSS:
    app.css.append_css({"external_url": css})
if __name__ == '__main__':
    app.run_server(debug=True)
