# ref: https://towardsdatascience.com/creating-an-interactive-data-app-using-plotlys-dash-356428b4699c

import base64
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table

import pandas as pd


def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df

def cleaned_data(df):
    x_col_num = [1,2,3,4,5,6]
    y_col_num = 7
    col_num = x_col_num.copy()
    col_num.append(y_col_num)
    print(col_num)
    cleaned_df = df[df.columns[col_num]]
    print(cleaned_df.head())
    return cleaned_df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

cleaned_df_global = pd.DataFrame()
app.layout = html.Div(children=[
    
    html.H2(children='Welcome to Data Analytics Tool',
    style={'textAlign': 'center'}),
    html.Div(children='''A tool developed as part of IISc CCE Data Analytics Course, 2020''',
            style={'textAlign': 'center'}),
    html.Hr(),
    
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files'), 
            '  (Allowed file type is CSV only)'
        ]),
        style={
            'width': '60%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    html.Div(id='output-data-upload'),
        
    html.Div(id='cleaned-df', style={'display': 'none'}),
   
])

@app.callback(Output('output-data-upload', 'children'),
            [Input('upload-data', 'contents'),
             Input('upload-data', 'filename')
            ])
def update_table(contents, filename):
    table = html.Div()

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        table = html.Div([
            html.H5(filename),
            dash_table.DataTable(
                data=df.iloc[:5].to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in df.columns]
            ),
            html.Hr(),
        ])

    return table


@app.callback(Output('cleaned-df', 'children'),
            [Input('upload-data', 'contents'),
             Input('upload-data', 'filename')
            ])
def saving_cleaned_data(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        cleaned_df = cleaned_data(df)
        cleaned_df.to_csv('cleaned_df.csv')
    return cleaned_df.to_json(date_format='iso', orient='split')

if __name__ == '__main__':
    app.run_server(debug=True)

