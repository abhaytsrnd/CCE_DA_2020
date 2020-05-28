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

from dataanalytics.ux.apps.ts_thread import TSThread

layout = html.Div(children=[
    common.navbar("Time Series Analysis"),
    html.Br(),
    html.Div([
        html.H2("Perform Time Series Analysis"),
        dbc.Button("Time Series Analysis", color="info", id = 'ts-do-time-series-analysis', className="mr-4"),
        html.Br(),
    ],
    style = {'margin': '10px', 'width': '50%'}),
    html.Div([], id = "ts-started-time-series-analysis")
])

@app.callback(
    Output("ts-started-time-series-analysis", "children"),
    [Input('ts-do-time-series-analysis', 'n_clicks')]
)
def ts_do_time_series_analysis(n_clicks):
    msg = 'Starting Time Series Analysis ...'
    print(msg)
    try:
        ts_thread_1 = TSThread(1, "Thread-1", 1)
        ts_thread_1.start()
        msg = 'Time Series Analysis Started on Thread-1'
    except:
        msg = 'Error: unable to start Thread!!'
    print(msg)
    return common.success_msg(msg)
