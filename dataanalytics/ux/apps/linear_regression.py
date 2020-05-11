import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go

import pandas as pd

from dataanalytics.ux.app import app
from dataanalytics.ux.apps import common
from dataanalytics.ux.apps.common import *
from dataanalytics.framework.database import db
from dataanalytics.framework.file_utils import FileUtils
from dataanalytics.framework.data_utils import DataUtils
from dataanalytics.stats_linear_regression.linear_regression import LinearRegression

file = db.get('lr.file')
if file is None:
    file = 'empty'
path = FileUtils.path('clean', file)
df_cleaned = pd.read_csv(path)

y_ycap_title = go.Layout(title = 'Actual vs Predicted Y Plot', hovermode = 'closest')
y_ycap_fig = go.Figure(data = [], layout = y_ycap_title)

error_title = go.Layout(title = 'Error Plot', hovermode = 'closest')
error_fig = go.Figure(data = [], layout = error_title)

layout = html.Div(children=[
    common.navbar("Linear Regression"),
    html.Br(),

    html.Div([
        html.H2("Select a file from all the cleaned files:"),
        dcc.Dropdown(
            id = 'linear-regression-file',
            options=[{'label':file, 'value':file} for file in FileUtils.files('clean')],
            value='empty',
            multi=False
        ),
        html.Br(),
        dbc.Button("Select File", color="primary", id = 'linear-regression-select-file', className="mr-4")
    ],
    style = {'margin': '10px', 'width': '50%'}),


    html.Br(),
    html.Div([], id = "linear-regression", style = {'margin': '10px'}),
    html.Div([], id = "linear-regression-file-do-nothing")
])
@app.callback(Output('linear-regression-file-do-nothing', 'children'),
            [Input('linear-regression-file', 'value')])
def linear_regression_file_value(value):
    file = db.get('lr.file')
    if not value is None:
        file = value
        db.put('lr.file', file)
    return None

@app.callback(Output('linear-regression', 'children'),
            [Input('linear-regression-select-file', 'n_clicks')])
def linear_regression(n):
    global df_cleaned
    file = db.get('lr.file')
    if file is None:
        file = 'empty'
    path = FileUtils.path('clean', file)
    df_cleaned = pd.read_csv(path)
    div = [
    html.Br(),
    html.Div(children=[
    html.H3(children='Cleaned Data: ' + file),
    generate_table(df_cleaned)],
    style={'width': '78%', 'display': 'inline-block'}),
    html.Hr(),

    html.H3(children='Variable Selection and Plotting'),

    html.Div([
        html.Div([
            html.Div(id='ordered-df', style={'display': 'none'}),
            html.Hr(),

            html.Label('Select X-axis variable for scatter plot'),
            dcc.Dropdown(
                id = 'x-var-plot',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                #value=['x_var_plot'],
                multi=False
            ),

            html.Label('Select Y-axis variable for scatter plot'),
            dcc.Dropdown(
                id = 'y-var-plot',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                #value=['y_var_plot'],
                multi=False
            ),

            html.Br(),
            html.H2('Perform Linear Regression'),
            html.Label('Select X variable from Dropdown'),
            dcc.Dropdown(
                id = 'x-var-selection',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                #value=['x_var_list'],
                multi=True
            ),

            html.Label('Select Y variable from Dropdown'),
            dcc.Dropdown(
                id = 'y-var-selection',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                #value=['y'],
                multi=False
            )
        ],style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Scatter Plot'),
            dcc.Graph(id='scatter-plot'),
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    ]),
    html.Hr(),

    html.Div([
        html.Div([], id = 'linear-regression-status'),
        html.Br(),
        html.H3('Statistics Summary Table'),
        html.Div([
            html.Table(id='stats_table'),
        ], style={'width': '60%', 'display': 'inline-block'}),

        html.Div([
            html.H2('Linear Regression Coefficients'),
            html.Table(id='coeff_table'),
        ],style={'width': '30%', 'float': 'right', 'display': 'inline-block'}),
    ]),

    html.Br(),

    html.Div([
        dcc.Graph(id='lr-y-ycap-plot', figure=y_ycap_fig),
        dcc.Graph(id='lr-error-plot', figure=error_fig)]),
    html.Div([
        html.H2('ANOVA Table'),
        html.Table(id='linear_anova_table'),
        ]),
    html.Hr()
    ]
    return div

@app.callback(Output('ordered-df', 'children'),
            [Input('x-var-selection', 'value'),
             Input('y-var-selection', 'value') ])
def ordering_data(x_var_value, y_var_value):
    print("Selected X Var Regression: ", x_var_value)
    print("Selected y Var Regression: ",y_var_value)
    if x_var_value is None or y_var_value is None:
        return None
    dfx = df_cleaned[x_var_value]
    dfy = df_cleaned[y_var_value]
    ordered_df = pd.concat([dfx,dfy],axis=1)
    return ordered_df.to_json(date_format='iso', orient='split')

@app.callback(Output('scatter-plot', 'figure'),
            [Input('x-var-plot', 'value'),
             Input('y-var-plot', 'value') ])
def scatter_plot(x_var_value, y_var_value):
    print("Selected X Var Plot: ", x_var_value)
    print("Selected y Var Plot: ",y_var_value)
    if x_var_value is None or y_var_value is None:
        return {}
    else:
        return {
        'data': [dict(
            x=df_cleaned[x_var_value],
            y=df_cleaned[y_var_value],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': x_var_value,
                'type': 'linear'
            },
            yaxis={
                'title': y_var_value,
                'type': 'linear'
            },
            margin={'l': 30, 'b': 30, 't': 10, 'r': 0},
            hovermode='closest',
            height=300,  # px
        )
    }

@app.callback([Output('linear-regression-status', 'children'),
                Output('stats_table', 'children'),
                Output('coeff_table', 'children'),
                Output('lr-y-ycap-plot','figure'),
                Output('lr-error-plot','figure')],
            [Input('ordered-df', 'children')])
def stats_table_and_linear_regression(json_ordered_data):
    if json_ordered_data is None:
        return (common.msg(None),
        generate_table(pd.DataFrame(columns=[])),
        generate_table(pd.DataFrame(columns=[])),
        y_ycap_fig,
        error_fig)
    dff = pd.read_json(json_ordered_data, orient='split')
    col = list(dff.columns)
    y = list(dff[col[-1]])
    data = []
    x_col = col[:-1]
    data = [[] for i in range(len(x_col))]
    for i in range(len(x_col)):
        x = dff[x_col[i]].values.tolist()
        data[i] = x

    ##Team 3 API Integration
    try:
        model = LinearRegression()
        db.put("lr.model", model)
        (summary, params, ycap) = model.fit(data, y)
        db.put("lr.summary", summary)
        db.put("lr.params", params)
        db.put("lr.ycap", ycap)
    except (Exception, ValueError) as e:
        print(str(e))
        return (common.error_msg("Linear Regression API Error: " + str(e)),
        generate_table(pd.DataFrame(columns=[])),
        generate_table(pd.DataFrame(columns=[])),
        y_ycap_fig,
        error_fig)

    for dict_value in summary:
        for k, v in dict_value.items():
            dict_value[k] = round(v, 4)
    df_stats = pd.DataFrame(summary)
    df_stats['Var_Name'] = col
    df_stats = df_stats[['Var_Name','count','min','max','mean','variance','std','covariance','r', 'pr']]
    table1 = generate_table(df_stats, len(col))

    x_col.append('Constant')
    params = [ '%.4f' % elem for elem in params ]
    df_coeff = pd.DataFrame(params, columns=['Coefficient'])
    df_coeff['Var_Name'] = x_col
    df_coeff = df_coeff[['Var_Name','Coefficient']]
    table2 = generate_table(df_coeff, len(x_col))

    trace_1 = go.Scatter(x = list(range(len(y))), y = ycap,
                    name = 'Y_Predicted',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
    trace_2 = go.Scatter(x = list(range(len(y))), y = y,
                        name = 'Y_Actual',
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)'))
    ydiff = [y[i] - ycap[i] for i in range(len(y))]
    trace_3 = go.Scatter(x = list(range(len(y))), y = ydiff,
                        name = 'Y_Error',
                        line = dict(width = 2,
                                    color = 'rgb(236, 10, 15)'))

    fig1 = go.Figure(data = [trace_1, trace_2], layout = y_ycap_title)
    fig2 = go.Figure(data = [trace_3], layout = error_title)
    return (common.success_msg("Linear Regression API Exceuted Successfully!!"),
    table1,
    table2,
    fig1,
    fig2)
