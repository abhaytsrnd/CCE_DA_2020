import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import base64

import pandas as pd

from dataanalytics.ux.app import app
from dataanalytics.ux.apps import common
from dataanalytics.ux.apps.common import *
from dataanalytics.framework.database import db
from dataanalytics.framework.file_utils import FileUtils
from dataanalytics.framework.data_utils import DataUtils
from dataanalytics.stats_linear_regression.Team3onlineLinearRegression import *
from dataanalytics.higher_order_regression.higher_order_regression_online_V1 import *
from dataanalytics.stat_anova.anova_online import *

file = db.get('hor.file')
if file is None:
    file = 'empty'
path = FileUtils.path('clean', file)
df_cleaned = pd.read_csv(path)

y_ycap_title = go.Layout(title = 'Actual vs Predicted Y Plot', hovermode = 'closest', xaxis={'title': 'Sequence of data points'}, yaxis={'title': 'y,ŷ'})
y_ycap_fig = go.Figure(data = [], layout = y_ycap_title)

error_title = go.Layout(title = 'Error Plot', hovermode = 'closest', xaxis={'title': 'Sequence of data points'}, yaxis={'title': 'Error = y - ŷ'})
error_fig = go.Figure(data = [], layout = error_title)

eq_option = ["polynomial", "logarithmic", "reciprocal", "power", "exponential"]

layout = html.Div(children=[
    common.navbar("Higher Order Regression"),
    html.Br(),
    html.Div([
        html.H2("Select a file from all the cleaned files:"),
        dbc.Button("Load Cleaned Files", color="info", id = 'hor-load-clean-files', className="mr-4"),
        html.Br(),
        html.Br(),
        dcc.Dropdown(
            id = 'hor-select-file',
            options=[{'label':file, 'value':file} for file in FileUtils.files('clean')],
            value='empty',
            multi=False
        ),
        html.Br(),
        dbc.Button("Select File", color="primary", id = 'hor-regression-select-file', className="mr-4")
    ],
    style = {'margin': '10px', 'width': '50%'}),


    html.Br(),
    html.Div([], id = "hor-regression", style = {'margin': '10px'}),
    html.Div([], id = "hor-regression-file-do-nothing")
])

@app.callback(
    Output("hor-select-file", "options"),
    [Input('hor-load-clean-files', 'n_clicks')]
)
def hor_load_cleaned_data(n_clicks):
    files = FileUtils.files('clean')
    print('Higher Order Load Clean')
    if len(files) == 0:
        options=[{'label':'No files cleaned yet!', 'value':'None'}]
    else:
        options=[{'label':file, 'value':file} for file in files]
    return options

@app.callback(Output('hor-regression-file-do-nothing', 'children'),
            [Input('hor-select-file', 'value')])
def hor_regression_file_value(value):
    if not value is None:
        db.clear('hor.')
        db.put('hor.file', value)
    return None

@app.callback(Output('hor-regression', 'children'),
            [Input('hor-regression-select-file', 'n_clicks')])
def higher_order_regression(n):
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
    html.H3(children='Variable Selection and Plotting'),
    html.Div([
        html.Div([
            html.Div(id='hor-ordered-df', style={'display': 'none'}),
            html.Hr(),
            html.Br(),
            html.H2('Perform Higher Order Regression'),
            html.Label('Select X variable from Dropdown'),
            dcc.Dropdown(
                id = 'hor-x-var-selection',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                multi=False
            ),

            html.Label('Select Y variable from Dropdown'),
            dcc.Dropdown(
                id = 'hor-y-var-selection',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                multi=False
            ),
            html.Label('Select Equation Type which you want to fit'),
            dcc.Dropdown(
                id = 'eq-selection',
                options=[{'label':i, 'value':i} for i in eq_option],
                multi=False
            ),
            
            html.Label('For polynomial - Select order of the desired equation'),
            dcc.Dropdown(
                id = 'hor-polynomial-order',
                options=[{'label':i, 'value':i} for i in range(2, 11)],
                multi=False
            ),
        ],style={'width': '40%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label('Scatter Plot'),
            dcc.Graph(id='hor-scatter-plot'),
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),
    ]),
    html.Hr(),

    html.Div([
        html.Div([], id = 'hor-regression-status'),
        html.Br(),
        html.H2('Statistics Summary Table'),
        html.Table(id='hor-stats-table'),
        html.H2('Higher Order Regression Coefficients'),
        html.Table(id='hor-coeff-table'),
        html.Img(id='image')
    ]),

    html.Br(),

    html.Div([
        html.H2('Plot'),
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
        html.H2('Predict Data - Independent Variables'),
        html.Div([], id='hor-predict-ind-var'),
        dbc.Input(id="hor-predict-data", placeholder="x", type="number"),
        html.Br(),
        dbc.Button("Predict", color="primary", id = 'hor-predict'),
        html.Div([], id='hor-predict-display'),
        html.Div([], id='hor-predict-data-do-nothing'),
        ]),
    html.Div([
        html.Hr(),
        html.H2('Save Model'),
        dbc.Input(id="hor-save-model", placeholder="Model Name", type="text"),
        html.Br(),
        dbc.Button("Save", color="primary", id = 'hor-save'),
        html.Div([], id='hor-save-display'),
        html.Div([], id='hor-save-model-do-nothing'),
        ])
    ]
    return div

@app.callback(Output('hor-ordered-df', 'children'),
            [Input('hor-x-var-selection', 'value'),
             Input('hor-y-var-selection', 'value') ])
def ordering_data(x_var_value, y_var_value):
    if x_var_value is None or y_var_value is None:
        return None
    dfx = df_cleaned[x_var_value]
    dfy = df_cleaned[y_var_value]
    ordered_df = pd.concat([dfx,dfy],axis=1)
    return ordered_df.to_json(date_format='iso', orient='split')

@app.callback(Output('hor-scatter-plot', 'figure'),
            [Input('hor-x-var-selection', 'value'),
             Input('hor-y-var-selection', 'value') ])
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

@app.callback([Output('hor-regression-status', 'children'),
                Output('hor-stats-table', 'children'),
                Output('hor-coeff-table', 'children'),
                Output('image', 'src'),
                Output('hor-y-ycap-plot','figure'),
                Output('hor-error-plot','figure'),
                Output('hor-error-mean', 'children'),
                Output('hor-anova-table','children'),
                Output('hor-predict-ind-var','children')],
            [Input('hor-ordered-df', 'children'),
            Input('eq-selection', 'value'),
            Input('hor-polynomial-order', 'value')])
def stats_table_and_hor_regression(json_ordered_data, reg_type, hor_order):
    if json_ordered_data is None or reg_type is None:
        return (common.msg(None),
        generate_table(pd.DataFrame(columns=[])),
        generate_table(pd.DataFrame(columns=[])),
        "",
        y_ycap_fig,
        error_fig,
        "",
        "",
        "")
    dff = pd.read_json(json_ordered_data, orient='split')
    col = list(dff.columns)
    x_col = [col[0]]
    y_col = col[1]
    dff = dff.sort_values(by=x_col)
    x = list(dff[col[0]])
    y = list(dff[col[1]])

    ##Team 4 API Integration
    try:
        db.put("hor.x_col", x_col)
        db.put("hor.y_col", y_col)
        db.put("hor.eq_type", reg_type)
        db.put("hor.eq_order", hor_order)
        input_data = InputData()
        input_data.sample_size = len(y)
        input_data.indep_vars = 1
        xa = np.zeros((len(x),1))
        for i in range(len(x)):
            xa[i,0] = x[i]
        input_data.indep_vars_matrix = xa
        input_data.dep_var_matrix = y
        
        if reg_type == "polynomial":
            ycap, params = performHigherOrderRegression(input_data, regression_type.polynomial, hor_order)
            image_filename = './asserts/poly_image.PNG'
        elif reg_type == "logarithmic":
            ycap, params = performHigherOrderRegression(input_data, regression_type.logarithmic, 0)
            image_filename = './asserts/log_image.PNG'
        elif reg_type == "reciprocal":
            ycap, params = performHigherOrderRegression(input_data, regression_type.reciprocal, 0)
            image_filename = './asserts/reci_image.PNG'
        elif reg_type == "power":
            ycap, params = performHigherOrderRegression(input_data, regression_type.power, 0)
            image_filename = './asserts/power_image.PNG'
        elif reg_type == "exponential":
            ycap, params = performHigherOrderRegression(input_data, regression_type.exponential, 0)
            image_filename = './asserts/exp_image.PNG'
        
        #print('param', type(params), params)
        encoded_image = base64.b64encode(open(image_filename, 'rb').read())
        db.put("hor.params", params)
        db.put("hor.ycap", ycap)
        db.put("hor.order", hor_order)
        error = 0.0
        for i in range(len(y)):
            error += y[i] - ycap[i]
        error_mean = error/len(y)
        db.put("hor.error_mean", error_mean)
        
        ## Team Online 3 API call for Summary Statistics
        model = Team3onlineLinearRegression([x], y)
        (params_ignore, summary, ycap_ignore) = model.fit()
        db.put("hor.summary", summary)
    except (Exception, ValueError) as e:
        return (common.error_msg("Higher Order Regression API Error: " + str(e)),
        generate_table(pd.DataFrame(columns=[])),
        generate_table(pd.DataFrame(columns=[])),
        "",
        y_ycap_fig,
        error_fig,
        "",
        "",
        "")
    eq_image = 'data:image/png;base64,{}'.format(encoded_image.decode())
    df_stats = common.get_stats_df(summary, x_col, y_col)
    table1 = dbc.Table.from_dataframe(df_stats, striped=True, bordered=True, hover=True, style = common.table_style)

    df_coeff = common.hor_get_coeff_df(params)
    table2 = dbc.Table.from_dataframe(df_coeff, striped=True, bordered=True, hover=True, style = common.table_style)

    trace_actual = go.Scatter(x = x, y = y,
                        name = 'Y Actual',
                        mode='markers',
                        marker=dict(color = 'rgb(106, 181, 135)'))

    trace_predict = go.Scatter(x = x, y = ycap,
                    name = 'Y Predicted (ŷ)',
                    line = dict(width = 2, color = 'rgb(229, 151, 50)'))

    ydiff = [y[i] - ycap[i] for i in range(len(y))]
    trace_error = go.Scatter(x = x, y = ydiff,
                        line = dict(width = 2, color = 'rgb(236, 10, 15)'))

    x_title = "x ("+ str(x_col[0]) +")"
    y_title = "y,ŷ("+ str(y_col) +")"
    y_ycap_title = go.Layout(title = 'Actual vs Predicted Y Plot', hovermode = 'closest', xaxis={'title': x_title}, yaxis={'title': y_title})
    error_title = go.Layout(title = 'Error Plot', hovermode = 'closest', xaxis={'title': x_title}, yaxis={'title': 'Error = y - ŷ'})

    fig1 = go.Figure(data = [trace_predict, trace_actual], layout = y_ycap_title)
    fig2 = go.Figure(data = [trace_error], layout = error_title)
    error_mean = html.H2('Error Mean = ' + str(round(db.get('hor.error_mean'), 4)))

    ##Team Online 5 API Integration
    anova = get_anova_online(y, ycap, len(params))
    db.put('hor.anova', anova)
    anova_div = common.get_anova_div(anova)

    independent_var = ','.join(x_col)

    return (common.success_msg("Higher Order Regression API Exceuted Successfully!!"),
    table1,
    table2,
    eq_image,
    fig1,
    fig2,
    error_mean,
    anova_div,
    html.H2(independent_var))

@app.callback(
    Output('hor-predict-data-do-nothing' , "children"),
    [Input('hor-predict-data', 'value')]
)
def hor_predict_input(value):
    if not value is None:
        db.put("hor.predict_data", value)
    return None

@app.callback(
    Output('hor-save-model-do-nothing' , "children"),
    [Input('hor-save-model', 'value')]
)
def hor_model_name_input(value):
    if not value is None:
        db.put("hor.model_name", value)
    return None

@app.callback(
    Output("hor-predict-display", "children"),
    [Input('hor-predict', 'n_clicks')]
)
def hor_predict_data(n_clicks):
    predict_data = db.get('hor.predict_data')
    y_col = db.get("hor.y_col")
    if predict_data is None:
        return ""
    params = db.get("hor.params")
    reg_type = db.get("hor.eq_type")
    hor_order = db.get("hor.eq_order")    
    x = [float(predict_data)]
    if reg_type == "polynomial":
        predicted = pedictHigherOrderRegression(x, params, regression_type.polynomial, hor_order)
    elif reg_type == "logarithmic":
        predicted = pedictHigherOrderRegression(x, params, regression_type.logarithmic, hor_order)
    elif reg_type == "reciprocal":
        predicted = pedictHigherOrderRegression(x, params, regression_type.reciprocal, hor_order)
    elif reg_type == "power":
        predicted = pedictHigherOrderRegression(x, params, regression_type.power, hor_order)
    elif reg_type == "exponential":
        predicted = pedictHigherOrderRegression(x, params, regression_type.exponential, hor_order)
    print(type(predicted), predicted)
    return common.success_msg('Predicted Dependent Variable (' + y_col +') = ' + str(round(predicted, 4)))

@app.callback(
    [Output("hor-save-display", "children"),
    Output("hor-save-model", "value"),],
    [Input('hor-save', 'n_clicks')]
)
def hor_save_model(n_clicks):
    model_name = db.get('hor.model_name')
    if model_name is None or model_name == '':
        return ("","")
    file = db.get("hor.file")
    model = db.get("hor.model")
    order = db.get("hor.order")
    params = db.get("hor.params")
    anova = db.get("hor.anova")
    error_mean = db.get('hor.error_mean')
    summary = db.get("hor.summary")
    x_col = db.get("hor.x_col")
    y_col = db.get("hor.y_col")
    m = {
        'file': file,
        'tag': db.get('tags')[file],
        'type': db.get("hor.eq_type"),
        'name': model_name,
        'model': model,
        'order': order,
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
