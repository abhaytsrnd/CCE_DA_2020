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

file = db.get('lr.file')
if file is None:
    file = 'empty'
path = FileUtils.path('clean', file)
df_cleaned = pd.read_csv(path)

y_ycap_title = go.Layout(title = 'Actual vs Predicted Y Plot', hovermode = 'closest', xaxis={'title': 'Sequence of data points'}, yaxis={'title': 'y,ŷ'})
y_ycap_fig = go.Figure(data = [], layout = y_ycap_title)

error_title = go.Layout(title = 'Error Plot', hovermode = 'closest', xaxis={'title': 'Sequence of data points'}, yaxis={'title': 'Error = y - ŷ'})
error_fig = go.Figure(data = [], layout = error_title)

layout = html.Div(children=[
    common.navbar("Linear Regression"),
    html.Div([], style = {'padding': '30px'}),
    html.Br(),
    html.Div([
        html.H2("Select a file from all the cleaned files:"),
        dbc.Button("Load Cleaned Files", color="info", id = 'lr-load-clean-files', className="mr-4"),
        html.Br(),
        html.Br(),
        dcc.Dropdown(
            id = 'lr-select-file',
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

@app.callback(
    Output("lr-select-file", "options"),
    [Input('lr-load-clean-files', 'n_clicks')]
)
def lr_load_cleaned_data(n_clicks):
    files = FileUtils.files('clean')
    print('Linear Load Clean')
    if len(files) == 0:
        options=[{'label':'No files cleaned yet!', 'value':'None'}]
    else:
        options=[{'label':file, 'value':file} for file in files]
    return options

@app.callback(Output('linear-regression-file-do-nothing', 'children'),
            [Input('lr-select-file', 'value')])
def linear_regression_file_value(value):
    if not value is None:
        db.clear('lr.')
        db.put('lr.file', value)
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
    tdf = df_cleaned.head(10).round(4)
    div = [
    html.Div(children=[
        html.H2(children='Cleaned Data: ' + file),
        html.H2(children='Tag: Tag ' + str(db.get('tags')[file])),
        dbc.Table.from_dataframe(tdf, striped=True, bordered=True, hover=True, style = common.table_style)
    ]),
    html.Hr(),
    html.H3(children='Variable Selection and Plotting'),
    html.Div([
        html.Div([
            html.Div(id='lr-ordered-df', style={'display': 'none'}),
            html.Hr(),

            html.Label('Select X-axis variable for scatter plot'),
            dcc.Dropdown(
                id = 'lr-x-var-plot',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                multi=False
            ),

            html.Label('Select Y-axis variable for scatter plot'),
            dcc.Dropdown(
                id = 'lr-y-var-plot',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                multi=False
            ),

            html.Br(),
            html.H2('Perform Linear Regression'),
            html.Label('Select X variable from Dropdown'),
            dcc.Dropdown(
                id = 'lr-x-var-selection',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                multi=True
            ),

            html.Label('Select Y variable from Dropdown'),
            dcc.Dropdown(
                id = 'lr-y-var-selection',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                multi=False
            ),
        ],style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Scatter Plot'),
            dcc.Graph(id='lr-scatter-plot'),
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    ]),
    html.Hr(),

    html.Div([
        html.Div([], id = 'linear-regression-status'),
        html.Br(),
        html.H2('Statistics Summary Table'),
        html.Table(id='lr-stats-table'),
        html.H2('Linear Regression Coefficients'),
        html.Table(id='lr-coeff-table'),
        html.H2('Plot')
    ]),

    html.Br(),

    html.Div([
        dcc.Graph(id='lr-y-ycap-plot', figure=y_ycap_fig),
        dcc.Graph(id='lr-error-plot', figure=error_fig),
        html.Div([], id = 'lr-error-mean')]),
    html.Div([
        html.Hr(),
        html.H2('ANOVA Table'),
        html.Div([], id='lr-anova-table'),
        ]),
    html.Div([
        html.Hr(),
        html.H2('Predict Data (pass comma separated) Independent Variables'),
        html.Div([], id='lr-predict-ind-var'),
        dbc.Input(id="lr-predict-data", placeholder="x1,x2,x3,x4,x5, ...", type="text"),
        html.Br(),
        dbc.Button("Predict", color="primary", id = 'lr-predict'),
        html.Div([], id='lr-predict-display'),
        html.Div([], id='lr-predict-data-do-nothing'),
        ]),
    html.Div([
        html.Hr(),
        html.H2('Save Model'),
        dbc.Input(id="lr-save-model", placeholder="Model Name", type="text"),
        html.Br(),
        dbc.Button("Save", color="primary", id = 'lr-save'),
        html.Div([], id='lr-save-display'),
        html.Div([], id='lr-save-model-do-nothing'),
        ])
    ]
    return div

@app.callback(Output('lr-ordered-df', 'children'),
            [Input('lr-x-var-selection', 'value'),
             Input('lr-y-var-selection', 'value') ])
def ordering_data(x_var_value, y_var_value):
    if x_var_value is None or y_var_value is None:
        return None
    dfx = df_cleaned[x_var_value]
    dfy = df_cleaned[y_var_value]
    ordered_df = pd.concat([dfx,dfy],axis=1)
    return ordered_df.to_json(date_format='iso', orient='split')

@app.callback(Output('lr-scatter-plot', 'figure'),
            [Input('lr-x-var-plot', 'value'),
             Input('lr-y-var-plot', 'value') ])
def scatter_plot(x_var_value, y_var_value):
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
                Output('lr-stats-table', 'children'),
                Output('lr-coeff-table', 'children'),
                Output('lr-y-ycap-plot','figure'),
                Output('lr-error-plot','figure'),
                Output('lr-error-mean', 'children'),
                Output('lr-anova-table','children'),
                Output('lr-predict-ind-var','children')],
            [Input('lr-ordered-df', 'children')])
def stats_table_and_linear_regression(json_ordered_data):
    if json_ordered_data is None:
        return (common.msg(None),
        generate_table(pd.DataFrame(columns=[])),
        generate_table(pd.DataFrame(columns=[])),
        y_ycap_fig,
        error_fig,
        "",
        "",
        "")
    dff = pd.read_json(json_ordered_data, orient='split')
    col = list(dff.columns)
    x_col = col[:-1]
    y_col = col[-1]

    if len(x_col) == 1:
        dff = dff.sort_values(by=x_col)

    data = [[] for i in range(len(x_col))]
    for i in range(len(x_col)):
        x = dff[x_col[i]].values.tolist()
        data[i] = x
    y = list(dff[col[-1]])
    ##Team 3 API Integration
    try:
        model = LinearRegression()
        db.put("lr.model", model)
        db.put("lr.x_col", x_col)
        db.put("lr.y_col", y_col)
        (summary, params, ycap) = model.fit(data, y)
        db.put("lr.summary", summary)
        db.put("lr.params", params)
        db.put("lr.ycap", ycap)
        error_mean = model.model_stats()['mean']
        db.put("lr.error_mean", error_mean)
    except (Exception, ValueError) as e:
        return (common.error_msg("Linear Regression API Error: " + str(e)),
        generate_table(pd.DataFrame(columns=[])),
        generate_table(pd.DataFrame(columns=[])),
        y_ycap_fig,
        error_fig,
        "",
        "",
        "")

    df_stats = common.get_stats_df(summary, x_col, y_col)
    table1 = dbc.Table.from_dataframe(df_stats, striped=True, bordered=True, hover=True, style = common.table_style)

    df_coeff = common.get_coeff_df(params, x_col)
    table2 = dbc.Table.from_dataframe(df_coeff, striped=True, bordered=True, hover=True, style = common.table_style)

    if len(data) == 1:
        trace_x = data[0]
        x_title = "x ("+ str(x_col[0]) +")"
        trace_actual = go.Scatter(x = trace_x, y = y,
                            name = 'Y Actual',
                            mode='markers',
                            marker=dict(color = 'rgb(106, 181, 135)'))
    else:
        trace_x = list(range(len(y)))
        x_title = 'Sequence of data points'
        trace_actual = go.Scatter(x = trace_x, y = y,
                            name = 'Y Actual',
                            line = dict(width = 2, color ='rgb(106, 181, 135)'))

    trace_predict = go.Scatter(x = trace_x, y = ycap,
                    name = 'Y Predicted (ŷ)',
                    line = dict(width = 2, color = 'rgb(229, 151, 50)'))

    ydiff = [y[i] - ycap[i] for i in range(len(y))]
    trace_error = go.Scatter(x = trace_x, y = ydiff,
                        line = dict(width = 2, color = 'rgb(236, 10, 15)'))

    y_title = "y,ŷ("+ str(y_col) +")"
    y_ycap_title = go.Layout(title = 'Actual vs Predicted Y Plot', hovermode = 'closest', xaxis={'title': x_title}, yaxis={'title': y_title})
    error_title = go.Layout(title = 'Error Plot', hovermode = 'closest', xaxis={'title': x_title}, yaxis={'title': 'Error = y - ŷ'})

    fig1 = go.Figure(data = [trace_predict, trace_actual], layout = y_ycap_title)
    fig2 = go.Figure(data = [trace_error], layout = error_title)
    error_mean = html.H2('Error Mean = ' + str(round(db.get('lr.error_mean'), 4)))

    ##Team 5 API Integration
    anova = get_anova(y, ycap, len(params))
    db.put('lr.anova', anova)
    anova_div = common.get_anova_div(anova)

    independent_var = ','.join(x_col)

    return (common.success_msg("Linear Regression API Exceuted Successfully!!"),
    table1,
    table2,
    fig1,
    fig2,
    error_mean,
    anova_div,
    html.H2(independent_var))

@app.callback(
    Output('lr-predict-data-do-nothing' , "children"),
    [Input('lr-predict-data', 'value')]
)
def lr_predict_input(value):
    if not value is None:
        db.put("lr.predict_data", value)
    return None

@app.callback(
    Output('lr-save-model-do-nothing' , "children"),
    [Input('lr-save-model', 'value')]
)
def lr_model_name_input(value):
    if not value is None:
        db.put("lr.model_name", value)
    return None

@app.callback(
    Output("lr-predict-display", "children"),
    [Input('lr-predict', 'n_clicks')]
)
def lr_predict_data(n_clicks):
    predict_data = db.get('lr.predict_data')
    y_col = db.get("lr.y_col")
    if predict_data is None:
        return ""
    predict_data = get_predict_data_list(predict_data)
    model = db.get("lr.model")
    params = db.get("lr.params")
    if len(predict_data) != len(params) - 1:
        return common.error_msg('Pass Valid Independent Variables!!')
    predicted = model.predict(predict_data)
    return common.success_msg('Predicted Dependent Variable (' + y_col +') = ' + str(predicted))

@app.callback(
    [Output("lr-save-display", "children"),
    Output("lr-save-model", "value"),],
    [Input('lr-save', 'n_clicks')]
)
def lr_save_model(n_clicks):
    model_name = db.get('lr.model_name')
    if model_name is None or model_name == '':
        return ("","")
    file = db.get("lr.file")
    model = db.get("lr.model")
    params = db.get("lr.params")
    anova = db.get("lr.anova")
    error_mean = db.get('lr.error_mean')
    summary = db.get("lr.summary")
    x_col = db.get("lr.x_col")
    y_col = db.get("lr.y_col")
    m = {
        'file': file,
        'tag': db.get('tags')[file],
        'type': 'Linear',
        'name': model_name,
        'model': model,
        'order': '-',
        'params': params,
        'no_of_coeff': len(params),
        'anova': anova,
        'summary': summary,
        'x_col': x_col,
        'y_col': y_col,
        'error_mean': error_mean}
    models = db.get('models')
    if models is None:
        models = {}
        db.put('models', models)
    models[model_name] = m
    return (common.success_msg('Model "'+ model_name +'" Saved Successfully.'), "")

def get_predict_data_list(predict_data: str) -> []:
    predict_data = predict_data.split(',')
    feature_vector = []
    for d in predict_data:
        feature_vector.append(float(d))
    return feature_vector
