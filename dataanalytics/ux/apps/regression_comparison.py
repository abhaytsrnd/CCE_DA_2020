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
])
