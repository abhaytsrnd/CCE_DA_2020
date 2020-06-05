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
        html.H2("Online Team-6 code not yet submitted"),
        html.Br(),
    ],
    style = {'margin': '10px', 'width': '50%'}),
])

