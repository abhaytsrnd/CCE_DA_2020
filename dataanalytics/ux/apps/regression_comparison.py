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
from dataanalytics.stat_anova.anova import get_anova

layout = html.Div(children=[
    common.navbar("Regression Comparison"),
    html.Br(),
    html.Div([
        dbc.Button("Load Cleaned Files & Regression Model", color="info", id = 'rc-load-model', className="mr-4"),
        html.Br(),
        html.Hr(),
        html.H2('Model Comparision'),
        html.Div([
            dbc.Label('Select Cleaned Data'),
            dcc.Dropdown(
                id = 'rc-select-data',
                options=[{'label':'', 'value':''}],
                multi=False
            ),
            html.Br(),
        ],
        style = {'width': '35%', 'display': 'inline-block'}),
        html.Br(),
        dbc.Button("Compare", color="primary", id = 'rc-compare', className="mr-4")
    ],style = {'margin': '10px'}),
    html.Div([], id = "rc-compare-display", style = {'margin': '10px'}),
    html.Div([], id = "rc-select-data-do-nothing"),
    html.Div([
        html.Br(),
        html.Hr(),
        html.H2('Model Details'),
        html.Div([
            dbc.Label('Select Model'),
            dcc.Dropdown(
                id = 'rc-select-model',
                options=[{'label':'', 'value':''}],
                multi=False
            ),
            html.Br(),
        ],
        style = {'width': '35%', 'display': 'inline-block'}),
        html.Br(),
        dbc.Button("Model Details", color="primary", id = 'rc-model', className="mr-4")
    ],style = {'margin': '10px'}),
    html.Div([], id = "rc-model-display", style = {'margin': '10px'}),
    html.Div([], id = "rc-select-model-do-nothing"),
])

@app.callback(
    [Output("rc-select-data", "options"),
    Output("rc-select-model", "options")],
    [Input('rc-load-model', 'n_clicks')]
)
def cr_load_models(n_clicks):
    files = FileUtils.files('clean')
    f = []
    for file in files:
        f.append({'label':file, 'value':file})
    models = db.get('models')
    m = []
    if models is None:
        return f,m
    for k,v in models.items():
        m.append({'label':k, 'value':k})
    return f,m

@app.callback(
    Output('rc-select-data-do-nothing' , "children"),
    [Input('rc-select-data', 'value')]
)
def rc_select_file(value):
    if not value is None:
        db.put("rc.file", value)
    return None

@app.callback(
    Output('rc-select-model-do-nothing' , "children"),
    [Input('rc-select-model', 'value')]
)
def rc_select_file(value):
    if not value is None:
        db.put("rc.model", value)
    return None

@app.callback(
    Output('rc-compare-display' , "children"),
    [Input('rc-compare', 'n_clicks')]
)
def rc_compare(n_clicks):
    file = db.get("rc.file")
    models = db.get('models')
    if file is None:
        return common.error_msg("Select Models for Comparison!!")
    if models is None:
        return common.error_msg("No Model has been trainned, Please Train Models First!!")
    compare_div = get_compare_div(file)
    return html.Div([
        compare_div,
        html.Br(),
        html.Hr()])

def get_compare_div(file):
    models = db.get('models')
    keys = []
    for key, value in models.items():
        f = value['file']
        if f == file:
            keys.append(key)
    if len(keys) == 0:
        return common.error_msg("No Model has been trainned for "+ file +". Please Train Models First!!")

    tags = []
    for tag in get_property(keys, 'tag'):
        tags.append('Tag '+ str(tag))
    df = pd.DataFrame(columns = ['Model Name'] + keys)
    df.loc[0] = ['Tag :'] + tags
    df.loc[1] = ['Type :'] + get_property(keys, 'type')
    df.loc[2] = ['No of Coefficients :'] + get_property(keys, 'params')
    df.loc[3] = ['F Statistics :'] + get_property(keys, 'anova', 'F')
    df.loc[4] = ['Cofficient of Determination :'] + get_property(keys, 'anova', 'R2')
    df.loc[5] = ['Error Mean :'] + get_property(keys, 'error_mean')
    df.round(4)
    div = html.Div([
        dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, style = common.table_style)
    ])
    return div

def get_property(keys, access_key, second_access_key = None) -> []:
    models = db.get('models')
    prop = []
    for key in keys:
        if second_access_key is None:
            value = models[key][access_key]
        else:
            value  = models[key][access_key][second_access_key]
        if isinstance(value, int) or isinstance(value, float):
            value = round(value, 4)
        if isinstance(value, list):
            value = len(value)
        prop.append(value)
    return prop


@app.callback(
    Output('rc-model-display' , "children"),
    [Input('rc-model', 'n_clicks')]
)
def rc_compare(n_clicks):
    key = db.get("rc.model")
    models = db.get('models')
    if key is None:
        return common.error_msg("Select Model for Details!!")
    if models is None:
        return common.error_msg("No Model has been trainned, Please Train Models First!!")
    return get_model_div(key)

def get_model_div(key):
    models = db.get('models')
    model = models[key]
    summary = model['summary']
    tag = model['tag']
    type = model['type']
    params = model['params']
    anova = model['anova']
    x_col = model['x_col']
    y_col = model['y_col']
    error_mean = model['error_mean']

    df_stats = common.get_stats_df(summary, x_col, y_col)
    stats_div = dbc.Table.from_dataframe(df_stats, striped=True, bordered=True, hover=True, style = common.table_style)

    df_coeff = common.get_coeff_df(params, x_col)
    coeff_div = dbc.Table.from_dataframe(df_coeff, striped=True, bordered=True, hover=True, style = common.table_style)

    anova_div = common.get_anova_div(anova)

    div = html.Div([
        html.H2("Model: " + key),
        html.H2("Tag: Tag" + str(tag)),
        html.H2("Type: " + type),
        html.H2('Statistics Summary Table'),
        stats_div,
        html.H2('Linear Regression Coefficients'),
        coeff_div,
        html.H2('Error Mean = ' + str(round(error_mean,4))),
        html.Br(),
        html.H2('Anova'),
        anova_div
    ])
    return div
