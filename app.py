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
    html.Img(src="http://www.arianamendible.com/images/bitmap.png")#bitmap.png
], className="banner", style={'backgroundColor':'darkslategray'}),

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
