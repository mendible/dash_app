'''This is our RPCA app for CSE 583'''


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



EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

PLOT_TYPE = ['X-component velocity', 'Y-component velocity', 'Velocity magnitude', ' Vorticity']

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

# lambda slider
@app.callback(Output('lambda-slider-output', 'children'),
              [Input('lambda-slider', 'value')])
def lambda_output(slider_value):
    'updates the lambda slider in a text box'
    return '\u03bb = {:0.2f}'.format(10**(slider_value-1))


# button stuff
@app.callback(Output('rpca-output-container-button', 'children'),
              [Input('rpca-button', 'n_clicks')],
              [State('upload-data', 'filename'),
               State('lambda-slider', 'value')])
def run_rpca(n_clicks, filename, slider_value):
    '''
    This function runs the RPCA on the loaded file and saves the data.
    '''
    if n_clicks is not None:
        lambda_value = 10**(slider_value-1)
        filename, _ = os.path.splitext(filename) # new fix for filename
        rpca_filename = '{}_lam{:0.2f}_rpca.mat'.format(filename, lambda_value)
        if os.path.isfile(rpca_filename):
            return 'RPCA already run on this data with \u03bb = {:0.2f}.'.format(lambda_value)
        mat = io.loadmat(filename, mat_dtype=True)
        locals().update(mat) # this line converts everything in dict to a variable
        full_data = mat['u_x']
        lowrank_mat, sparse_mat = rpca.rpca(full_data, lambda_value)
        color_limits = [0.5*np.min(full_data), 0.5*np.max(full_data)]
        my_dict = {'sparse':sparse_mat, 'lowrank':lowrank_mat,
                   'fulldata':full_data, 'color_limits':color_limits}
        io.savemat(file_name=rpca_filename, mdict=my_dict)
        return 'RPCA run on {} with \u03bb = {:0.2f} and saved'.format(filename, lambda_value)
    return None

# make output if there is no data loaded upon plot click
#this doesn't work right now, not executing upon click, just always
@app.callback(Output('plot-output-container-button', 'children'),
              [Input('plot-button', 'n_clicks')],
              [State('upload-data', 'filename')])
def plot_check(_, filename):
    '''
    This function prompts the user to select a data file before plotting
    '''
    if filename is None:
        return 'First select the data to plot.'
    return None


@app.callback(Output('video-output-container-button', 'children'),
              [Input('save-video-button', 'n_clicks')],
              [State('video-filename', 'value'),
               State('vid-file-type', 'value')])
def save_video(_, filename, filetype):
    '''
    This function saves the videos of the full, low rank or sparse data.
    '''
    ## replace this code with a video saving function
    if filename is not None and filetype is not None:
        my_dict = {'test':1}
        io.savemat(file_name='{}{}'.format(filename, filetype), mdict=my_dict)
        return 'The video {}{} has been saved.'.format(filename, filetype)
    return None
# plotting stuff
@app.callback(Output('full-data-plot', 'figure'),
              [Input('plot-button', 'n_clicks')],
              [State('crossfilter-yaxis-column', 'value'),
               State('lambda-slider', 'value'),
               State('upload-data', 'filename')])
def update_graph_full(n_clicks, yaxis_column_name, slider_value, filename):
    '''
    This function updates the plot of the raw data.
    '''
    if n_clicks is not None:
        lambda_value = 10**(slider_value-1)
        filename, _ = os.path.splitext(filename) # new fix for filename
        rpca_filename = '{}_lam{:0.2f}_rpca.mat'.format(filename, lambda_value)
        if os.path.isfile(rpca_filename):
            mat = io.loadmat(rpca_filename, mat_dtype=True)
            color_limits = mat['color_limits']
            fulldata = mat['fulldata']
            plot_z = fulldata[:, :, 1]
        else: plot_z = 1
        return {
            'data': [go.Heatmap(
                z=plot_z,
                colorbar={'x':-0.15}, # position of the colorbar
                zmin=color_limits[0][0],
                zmax=color_limits[0][1],
            )],
            'layout': go.Layout(
                xaxis={'showticklabels':False, 'ticks':''},
                yaxis={'showticklabels':False, 'ticks':''},
                title='Full Data: ' + str(yaxis_column_name),
                margin={'l':40, 'b':40, 't':40, 'r':40},
                height=450,
                #hovermode='closest'
            )
        }
    return None

@app.callback(Output('low-rank-data-plot', 'figure'),
              [Input('plot-button', 'n_clicks')],
              [State('crossfilter-yaxis-column', 'value'),
               State('lambda-slider', 'value'),
               State('upload-data', 'filename')])
def update_graph_lowrank(n_clicks, yaxis_column_name, slider_value, filename):
    '''
    This function updates the plot of the low rank data.
    '''
    if n_clicks is not None:
        lambda_value = 10**(slider_value-1)
        filename, _ = os.path.splitext(filename) # new fix for filename
        rpca_filename = '{}_lam{:0.2f}_rpca.mat'.format(filename, lambda_value)
        if os.path.isfile(rpca_filename):
            mat = io.loadmat(rpca_filename, mat_dtype=True)
            lowrank = mat['lowrank']
            color_limits = mat['color_limits']
            plot_z = lowrank[:, :, 1]
        else: plot_z = 1
        return {
            'data': [go.Heatmap(
                z=plot_z,
                zmin=color_limits[0][0],
                zmax=color_limits[0][1],
                showscale=False
            )],
            'layout': go.Layout(
                xaxis={'showticklabels':False, 'ticks':''},
                yaxis={'showticklabels':False, 'ticks':''},
                title='Low Rank Data: ' + str(yaxis_column_name),
                margin={'l':40, 'b':40, 't':40, 'r':40},
                height=450,
                #hovermode='closest'
            )
        }
    return None
@app.callback(Output('sparse-data-plot', 'figure'),
              [Input('plot-button', 'n_clicks')],
              [State('crossfilter-yaxis-column', 'value'),
               State('lambda-slider', 'value'),
               State('upload-data', 'filename')])
def update_graph_sparse(n_clicks, yaxis_column_name, slider_value, filename):
    '''
    This function updates the plot of the sparse data.
    '''
    if n_clicks is not None:
        lambda_value = 10**(slider_value-1)
        filename, _ = os.path.splitext(filename) # new fix for filename
        rpca_filename = '{}_lam{:0.2f}_rpca.mat'.format(filename, lambda_value)
        if os.path.isfile(rpca_filename):
            mat = io.loadmat(rpca_filename, mat_dtype=True)
            color_limits = mat['color_limits']
            sparse_data = mat['sparse']
            plot_z = sparse_data[:, :, 1]
        else: plot_z = 1
        return {
            'data': [go.Heatmap(
                z=plot_z,
                zmin=color_limits[0][0],
                zmax=color_limits[0][1],
                showscale=False
            )],
            'layout': go.Layout(
                xaxis={'showticklabels':False, 'ticks':''},
                yaxis={'showticklabels':False, 'ticks':''},
                title='Sparse Data: '+str(yaxis_column_name),
                margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                height=450,
                #hovermode='closest'
            )
        }
    return None

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
