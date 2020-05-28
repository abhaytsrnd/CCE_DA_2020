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
from dataanalytics.higher_order_regression.higher_order_polynomial_V1 import *
from dataanalytics.stat_anova.anova import get_anova

app.config.suppress_callback_exceptions = True

file = db.get('hor.file')
if file is None:
    file = 'empty'
path = FileUtils.path('clean', file)
df_cleaned = pd.read_csv(path)

y_ycap_title = go.Layout(title = 'Actual vs Predicted Y Plot', hovermode = 'closest', xaxis={'title': 'X'}, yaxis={'title': 'y, ŷ'})
y_ycap_fig = go.Figure(data = [], layout = y_ycap_title)

error_title = go.Layout(title = 'Error Plot', hovermode = 'closest', xaxis={'title': 'X'}, yaxis={'title': 'Error = y - ŷ'})
error_fig = go.Figure(data = [], layout = error_title)


layout = html.Div(children=[
    common.navbar("Higher Order Regression"),
    html.Br(),
    html.Div([
        html.H2("Select a file from all the cleaned files:"),
        #dbc.Button("Load Cleaned Files", color="info", id = 'hor-load-clean-files', className="mr-4"),
        #html.Br(),
        #html.Br(),
        dcc.Dropdown(
            id = 'hor-select-file',
            options=[{'label':file, 'value':file} for file in FileUtils.files('clean')],
            value='empty',
            multi=False
        ),
        html.Br(),
        dbc.Button("Select File", color="primary", id = 'hor-select-file-button', className="mr-4")
    ],
    style = {'margin': '10px', 'width': '50%'}),
    
    html.Br(),
    html.Div([], id = "ho-regression", style = {'margin': '10px'}),
    html.Div([], id = "ho-regression-file-do-nothing")
])

@app.callback(Output('ho-regression-file-do-nothing', 'children'),
            [Input('hor-select-file', 'value')])
def ho_regression_file_value(value):
    if not value is None:
        db.clear('hor.')
        db.put('hor.file', value)
    return None
    
@app.callback(Output('ho-regression', 'children'),
            [Input('hor-select-file-button', 'n_clicks')])
def ho_regression(n):
    global df_cleaned
    file = db.get('hor.file')
    if file is None:
        file = 'empty'
    path = FileUtils.path('clean', file)
    df_cleaned = pd.read_csv(path)
    tdf = df_cleaned.head(10).round(4)
    div = [
    html.Div(children=[
        html.H2(children='Cleaned Data: ' + file),
        html.H2(children='Tag: Tag ' + str(db.get('tags')[file])),
        dbc.Table.from_dataframe(tdf, striped=True, bordered=True, hover=True, style = common.table_style)
    ]),
    html.Hr(),
    html.Div([
        html.Div([
            html.Div(id='ordered-df-hor', style={'display': 'none'}),
            html.Hr(),
            html.Br(),
            html.H2('Perform Higher Order Polynomial Regression'),
            html.Label('Select X variable from Dropdown'),
            dcc.Dropdown(
                id = 'x-var-selection',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                multi=False
            ),

            html.Label('Select Y variable from Dropdown'),
            dcc.Dropdown(
                id = 'y-var-selection',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                multi=False
            ),
            
            html.Label('Select order of the desired higher order polynomial equation'),
            dcc.Input(
                id="hor-polynomial-order", type="number", placeholder="Order of the polynomial equation",
                min=2, max=10, step=1,
            ),
                
        ],style={'width': '48%', 'display': 'inline-block'}),
    
    ]),
    html.Hr(),

    html.Div([
        html.Div([], id = 'ho-regression-status'),
        html.Br(),
        html.H2('Higher Order Polynomial Regression Coefficients'),
        html.Table(id='hor-coeff_table'),
        html.H2('Plot')
    ]),

    html.Br(),

    html.Div([
        dcc.Graph(id='hor-y-ycap-plot', figure=y_ycap_fig),
        dcc.Graph(id='hor-error-plot', figure=error_fig),
        html.Div([], id = 'hor-error-mean')]),
    html.Div([
        html.Hr(),
        html.H2('ANOVA Table'),
        html.Div([], id='hor-anova-table'),
        ]),
    html.Div([
        html.Hr(),
        dbc.Label('Predict Data: Input Independent Variable'),
        dbc.Input(id="hor-predict-data", placeholder="Input X", type="text"),
        html.Br(),
        dbc.Button("Predict", color="primary", id = 'hor-predict'),
        html.Div([], id='hor-predict-display'),
        html.Div([], id='hor-predict-data-do-nothing'),
        ]),
    html.Div([
        html.Hr(),
        dbc.Label('Save Model'),
        dbc.Input(id="hor-save-model", placeholder="Model Name", type="text"),
        html.Br(),
        dbc.Button("Save", color="primary", id = 'hor-save'),
        html.Div([], id='hor-save-display'),
        html.Div([], id='hor-save-model-do-nothing'),
        ])
    ]
    return div

@app.callback(Output('ordered-df-hor', 'children'),
            [Input('x-var-selection', 'value'),
             Input('y-var-selection', 'value') ])
def ordering_data(x_var_value, y_var_value):
    if x_var_value is None or y_var_value is None:
        return None
    dfx = df_cleaned[x_var_value]
    dfy = df_cleaned[y_var_value]
    ordered_df = pd.concat([dfx,dfy],axis=1)
    return ordered_df.to_json(date_format='iso', orient='split')

@app.callback([Output('ho-regression-status', 'children'),
                Output('hor-coeff_table', 'children'),
                Output('hor-y-ycap-plot','figure'),
                Output('hor-error-plot','figure'),
                Output('hor-error-mean', 'children'),
                Output('hor-anova-table','children')],
            [Input('ordered-df-hor', 'children'),
             Input("hor-polynomial-order", 'value')])
def higher_order_regression(json_ordered_data, hor_order):
    if json_ordered_data is None:
        return (common.msg(None),
        generate_table(pd.DataFrame(columns=[])),
        generate_table(pd.DataFrame(columns=[])),
        y_ycap_fig,
        error_fig,
        "",
        "")
    dff = pd.read_json(json_ordered_data, orient='split')
    col = list(dff.columns)
    x_col = col[0]
    y_col = col[1]
    dff = dff.sort_values(by=x_col)
    x = list(dff[col[0]])
    y = list(dff[col[1]])

    ##Team 4 API Integration
    try:
        db.put("hor.x_col", x_col)
        db.put("hor.y_col", y_col)
        (ycap, params) = Building_model_equation(x, y, hor_order)
        params = params.tolist()
        #print('type of param', type(params), params)
        db.put("hor.params", params)
        db.put("hor.ycap", ycap)
        error = 10.0
        for i in range(len(y)):
            error += y[i] - ycap[i]
        error_mean = error/len(y)
        db.put("hor.error_mean", error_mean)
    except (Exception, ValueError) as e:
        return (common.error_msg("Higher Order Regression API Error: " + str(e)),
        generate_table(pd.DataFrame(columns=[])),
        generate_table(pd.DataFrame(columns=[])),
        y_ycap_fig,
        error_fig,
        "",
        "")

    df_coeff = common.hor_get_coeff_df(params)
    table2 = dbc.Table.from_dataframe(df_coeff, striped=True, bordered=True, hover=True, style = common.table_style)

    trace_1 = go.Scatter(x = x, y = ycap,
                    name = 'Y Predicted (ŷ)',
                    line = dict(width = 2,
                                color = 'rgb(229, 151, 50)'))
    trace_2 = go.Scatter(x = x, y = y,
                        name = 'Y Actual',
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)'))
    ydiff = [y[i] - ycap[i] for i in range(len(y))]
    trace_3 = go.Scatter(x = x, y = ydiff,
                        line = dict(width = 2,
                                    color = 'rgb(236, 10, 15)'))

    fig1 = go.Figure(data = [trace_1, trace_2], layout = y_ycap_title)
    fig2 = go.Figure(data = [trace_3], layout = error_title)
    error_mean = html.H2('Error Mean = ' + str(round(db.get('hor.error_mean'), 4)))

    ##Team 5 API Integration
    anova = get_anova(y, ycap, len(params))
    db.put('hor.anova', anova)
    anova_div = common.get_anova_div(anova)

    return (common.success_msg("Higher Order Regression API Exceuted Successfully!!"),
    table2,
    fig1,
    fig2,
    error_mean,
    anova_div)
    
@app.callback(
    Output('hor-predict-data-do-nothing' , "children"),
    [Input('hor-predict-data', 'value')]
)
def hor_predict_input(value):
    if not value is None:
        db.put("cho.predict_data", value)
    return None
    
@app.callback(
    Output('hor-save-model-do-nothing' , "children"),
    [Input('hor-save-model', 'value')]
)
def cl_model_name_input(value):
    if not value is None:
        db.put("cho.model_name", value)
    return None
    
@app.callback(
    Output("hor-predict-display", "children"),
    [Input('hor-predict', 'n_clicks')]
)
def hor_predict_data(n_clicks):
    predict_data = db.get('cho.predict_data') 
    if predict_data is None:
        return ""
    params = db.get("hor.params")
    x = [float(predict_data)]
    predicted = Predict_final_values(x, params)
    return common.success_msg('Predicted Dependent Variable = ' + str(round(predicted[0], 4)))
    
@app.callback(
    [Output("hor-save-display", "children"),
    Output("hor-save-model", "value"),],
    [Input('hor-save', 'n_clicks')]
)
def hor_save_model(n_clicks):
    model_name = db.get('cho.model_name')
    if model_name is None or model_name == '':
        return ("","")
    file = db.get("hor.file")
    params = db.get("hor.params")
    anova = db.get("hor.anova")
    error_mean = db.get('hor.error_mean')
    x_col = db.get("hor.x_col")
    y_col = db.get("hor.y_col")
    m = {
        'file': file,
        'tag': db.get('tags')[file],
        'type': 'Higher Order Polynomial',
        'name': model_name,
        'params': params,
        'anova': anova,
        'x_col': x_col,
        'y_col': y_col,
        'error_mean': error_mean}
    models = db.get('models')
    if models is None:
        models = {}
        db.put('models', models)
    models[model_name] = m
    return (common.success_msg('Model "'+ model_name +'" Saved Successfully.'), "")