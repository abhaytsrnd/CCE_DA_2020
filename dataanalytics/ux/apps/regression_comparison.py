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
        dbc.Button("Load Regression Model", color="info", id = 'rc-load-model', className="mr-4"),
        html.Br(),
        html.Div([
            dbc.Label('Select Model 1'),
            dcc.Dropdown(
                id = 'rc-select-model-1',
                options=[{'label':'', 'value':''}],
                multi=False
            ),
            html.Br(),
        ],
        style = {'margin': '10px', 'width': '35%', 'display': 'inline-block'}),
        html.Div([
            dbc.Label('Select Model 2'),
            dcc.Dropdown(
                id = 'rc-select-model-2',
                options=[{'label':'', 'value':''}],
                multi=False
            ),
            html.Br(),
        ],
        style = {'margin': '10px', 'width': '35%', 'display': 'inline-block'}),
        html.Br(),
        dbc.Button("Compare", color="primary", id = 'rc-compare', className="mr-4")
    ], style={'textAlign': 'center'}),
    html.Hr(),
    html.Div([], id = "rc-compare-display", style = {'margin': '10px'}),
    html.Div([], id = "rc-select-model-1-do-nothing"),
    html.Div([], id = "rc-select-model-2-do-nothing"),
])

@app.callback(
    [Output("rc-select-model-1", "options"),
    Output("rc-select-model-2", "options")],
    [Input('rc-load-model', 'n_clicks')]
)
def cr_load_models(n_clicks):
    models = db.get('models')
    m = [{'label':'', 'value':''}]
    if models is None:
        return m, m
    for k, v in models.items():
        m.append({'label':k, 'value':k})
    return m, m

@app.callback(
    Output('rc-select-model-1-do-nothing' , "children"),
    [Input('rc-select-model-1', 'value')]
)
def rc_select_model_1(value):
    if not value is None:
        db.put("rc.model_1", value)
    return None

@app.callback(
    Output('rc-select-model-2-do-nothing' , "children"),
    [Input('rc-select-model-2', 'value')]
)
def rc_select_model_2(value):
    if not value is None:
        db.put("rc.model_2", value)
    return None

@app.callback(
    Output('rc-compare-display' , "children"),
    [Input('rc-compare', 'n_clicks')]
)
def rc_compare(n_clicks):
    model_1_key = db.get("rc.model_1")
    model_2_key = db.get("rc.model_2")
    if model_1_key is None:
        return common.error_msg("Select Models for Comparison!!")
    div_1 = get_model_div(model_1_key)
    if model_2_key is None or (model_1_key == model_2_key):
        return div_1
    div_2 = get_model_div(model_2_key)
    return html.Div([
        div_1,
        html.Br(),
        html.Hr(),
        div_2])

def get_model_div(key):
    models = db.get('models')
    model = models[key]
    summary = model['summary']
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
        html.H2('Statistics Summary Table'),
        stats_div,
        html.H2('Linear Regression Coefficients'),
        coeff_div,
        html.P('Error Mean = ' + str(error_mean)),
        html.Br(),
        html.H2('Anova'),
        anova_div
    ])
    return div
