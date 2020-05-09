# ref: https://towardsdatascience.com/creating-an-interactive-data-app-using-plotlys-dash-356428b4699c

import base64
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table

import pandas as pd

from dataanalytics.stats_linear_regression.linear_regression import LinearRegression
#from dataanalytics.stats_linear_regression.statistics import describe

df_original = pd.read_csv('.\data\original_data.csv')
df_original = df_original[df_original.columns[1:]]
df_cleaned = pd.read_csv('.\data\cleaned_df.csv')
df_cleaned = df_cleaned[df_cleaned.columns[1:]]

def generate_table(dataframe, max_rows=5):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.H2(children='Welcome to Data Analytics Tool',
    style={'textAlign': 'center'}),
    html.Div(children='''A tool developed as part of IISc CCE Data Analytics Course, 2020''',
            style={'textAlign': 'center'}),
    html.Hr(),

    html.Div(children=[
    html.H3(children='Original Imported Data'),
    generate_table(df_original) ],
    style={'width': '78%', 'display': 'inline-block'}),
        
    html.Div(children=[
    html.H3(children='Cleaned Data'),
    generate_table(df_cleaned) ],
    style={'width': '78%', 'display': 'inline-block'}),
    html.Hr(),

    html.Div([
        html.Div([
            html.Label('Select X variable from Dropdown'),
            dcc.Dropdown(
                id = 'x-var-selection',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                value=['x_var_list'],
                multi=True
            ),

            html.Label('Select Y variable from Dropdown'),
            dcc.Dropdown(
                id = 'y-var-selection',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                value=['y'],
            ),
        
            html.Div(id='ordered-df', style={'display': 'none'}),
            html.Hr(),
            
            html.Label('Select X-axis variable for scatter plot'),
            dcc.Dropdown(
                id = 'x-var-plot',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                value=['x_var_plot'],
                multi=False,
            ),

            html.Label('Select Y-axis variable for scatter plot'),
            dcc.Dropdown(
                id = 'y-var-plot',
                options=[{'label':i, 'value':i} for i in df_cleaned.columns],
                value=['y_var_plot'],
                multi=False,
            ),
        ],style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Scatter Plot'),
            dcc.Graph(id='scatter-plot'),
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),        
    ]),
    
    html.H3('Statistics Summary Table'),
    html.Table(id='stats_table'),
    html.Hr(),
    
    html.Div([
        html.Div([
            html.H4('Linear Regression Coefficients'),
            html.Table(id='coeff_table'),
        ],style={'width': '40%', 'display': 'inline-block'}),
        
        html.Div([
            html.H4('Linear Regression ANOVA Table'),
            html.Table(id='linear_anova_table'),
            ], style={'width': '60%', 'float': 'right', 'display': 'inline-block'}),        
    ]),
    html.Hr(),
    
])

@app.callback(Output('ordered-df', 'children'),
            [Input('x-var-selection', 'value'),
             Input('y-var-selection', 'value') ])
def ordering_data(x_var_value, y_var_value):
    print("Selected X Var: ", x_var_value)
    print("Selected y Var: ",y_var_value)
    dfx = df_cleaned[x_var_value]
    dfy = df_cleaned[y_var_value]
    ordered_df = pd.concat([dfx,dfy],axis=1)
    #print(ordered_df)
    return ordered_df.to_json(date_format='iso', orient='split')

@app.callback(Output('scatter-plot', 'figure'),
            [Input('x-var-plot', 'value'),
             Input('y-var-plot', 'value') ])
def scatter_plot(x_var_value, y_var_value):
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
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }
    
@app.callback(Output('stats_table', 'children'), 
            [Input('ordered-df', 'children')])
def update_stats_table(json_ordered_data):
    dff = pd.read_json(json_ordered_data, orient='split')
    col = list(dff.columns)
    y = list(dff[col[-1]])
    data = []
    x_col = col[:-1]
    data = [[] for i in range(len(x_col))]
    for i in range(len(x_col)):
        x = dff[x_col[i]].values.tolist()
        data[i] = x

    model = LinearRegression()
    (summary, params, ycap) = model.fit(data, y)
    df_stats = pd.DataFrame(summary)
    df_stats['Var_Name'] = col 
    df_stats = df_stats[['Var_Name','count','min','max','mean','variance','std','covariance','r']]
    #print(summary)
    table = generate_table(df_stats, len(col))
    return table
    
@app.callback(Output('coeff_table', 'children'), 
            [Input('ordered-df', 'children')])
def update_stats_table(json_ordered_data):
    dff = pd.read_json(json_ordered_data, orient='split')
    col = list(dff.columns)
    y = list(dff[col[-1]])
    data = []
    x_col = col[:-1]
    data = [[] for i in range(len(x_col))]
    for i in range(len(x_col)):
        x = dff[x_col[i]].values.tolist()
        data[i] = x

    model = LinearRegression()
    (summary, params, ycap) = model.fit(data, y)
    x_col.append('Constant')
    print('param col:',x_col)
    print('param:',params)
    df_coeff = pd.DataFrame(params, columns=['Coefficient'])
    df_coeff['Var_Name'] = x_col 
    df_coeff = df_coeff[['Var_Name','Coefficient']]
    table = generate_table(df_coeff, len(x_col))
    return table

if __name__ == '__main__':
    app.run_server(debug=True)
