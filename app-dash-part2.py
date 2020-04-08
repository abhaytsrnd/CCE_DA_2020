# ref: https://towardsdatascience.com/creating-an-interactive-data-app-using-plotlys-dash-356428b4699c

import base64
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table

import pandas as pd

df = pd.read_csv('cleaned_df.csv')
df = df[df.columns[1:]]

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
    html.H3(children='Cleaned Data'),
    generate_table(df) ],
    style={'width': '78%', 'display': 'inline-block'}),
    html.Hr(),
    
    html.Div([
        html.Label('Select X variable from Dropdown'),
        dcc.Dropdown(
            id = 'x-var-selection',
            options=[{'label':i, 'value':i} for i in df.columns],
            value=['x_var_list'],
            multi=True
        ),
        
        html.Label('Select Y variable from Dropdown'),
        dcc.Dropdown(
            id = 'y-var-selection',
            options=[{'label':i, 'value':i} for i in df.columns],
            value=['y'],
        )
    ],
    style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div(id='ordered-df', style={'display': 'none'}),
   
    html.Label('Select X-axis variable for scatter plot'),
    dcc.Dropdown(
        id = 'x-var-plot',
        options=[{'label':i, 'value':i} for i in df.columns],
        value=['x_var_plot'],
        multi=False,
        style={'width': '48%', 'display': 'inline-block'}
    ),
    
    html.Label('Select Y-axis variable for scatter plot'),
    dcc.Dropdown(
        id = 'y-var-plot',
        options=[{'label':i, 'value':i} for i in df.columns],
        value=['y_var_plot'],
        multi=False,
        style={'width': '48%', 'display': 'inline-block'}
    ),
        
    dcc.Graph(id='scatter-plot'),
])

@app.callback(Output('ordered-df', 'children'),
            [Input('x-var-selection', 'value'),
             Input('y-var-selection', 'value') ])
def ordering_data(x_var_value, y_var_value):
    print(x_var_value)
    print(y_var_value)
    dfx = df[x_var_value]
    dfy = df[y_var_value]
    ordered_df = pd.concat([dfx,dfy],axis=1)
    print(ordered_df)
    return ordered_df.to_json(date_format='iso', orient='split')
    
@app.callback(Output('scatter-plot', 'figure'),
            [Input('x-var-plot', 'value'),
             Input('y-var-plot', 'value') ])
def scatter_plot(x_var_value, y_var_value):
    return { 
        'data': [dict(
            x=df[x_var_value],
            y=df[y_var_value],
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
     

if __name__ == '__main__':
    app.run_server(debug=True)

