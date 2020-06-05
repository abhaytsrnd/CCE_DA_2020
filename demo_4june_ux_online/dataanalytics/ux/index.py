import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from dataanalytics.ux.app import app
from dataanalytics.ux.apps import home, linear_regression, higher_order_regression, regression_comparison, time_series_analysis

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/apps/linear-regression':
        return linear_regression.layout
    elif pathname == '/apps/higher-order-regression':
        return higher_order_regression.layout
    elif pathname == '/apps/regression-comparison':
        return regression_comparison.layout
    elif pathname == '/apps/time-series-analysis':
        return time_series_analysis.layout
    else:
        return '404'


app.run_server(debug=True)
