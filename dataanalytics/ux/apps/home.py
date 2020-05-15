import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

from dataanalytics.ux.app import app
from dataanalytics.ux.apps import common
from dataanalytics.framework.file_utils import FileUtils
from dataanalytics.framework.data_utils import DataUtils
from dataanalytics.framework.database import db

import pandas as pd

from dataanalytics.data_cleaning.team2_data_cleaning import data_cleaning

layout = html.Div([
    common.navbar("Home"),
    html.Br(),
    html.Div(children='A tool developed as part of IISc CCE Data Analytics Course, 2020',
            style={'textAlign': 'center', 'font-size': '16px'}),
    html.Hr(),
    html.Br(),
    dcc.Upload(
        id='upload-data',
        children=html.Div([html.A('Drag and Drop or Select Files')],
        style = {'font-size': '16px'}),
        style={
            'width': '50%',
            'height': '50px',
            'lineHeight': '50px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True),
        html.Div([], id = "data-upload-msg"),
        html.Div([
            dbc.Button("Load Uploaded Files", color="info", id = 'home-load-raw-files', className="mr-4"),
            #dbc.Button("Reset App", color="danger", id = 'reset-app', className="mr-4"),
            html.Br()],
            style = {'margin': '10px', 'width': '50%'}),
        html.Div([
            html.H2("Select a file from all the uploaded files:"),
            dcc.Dropdown(
                id = 'selected-file',
                options=[{'label':file, 'value':file} for file in FileUtils.files('raw')],
                value=None,
                multi=False
            ),
            html.Br()
        ],
        style = {'margin': '10px', 'width': '50%'}),

        html.Div([], id = "display-file"),

        html.Div([], id = "file-properties"),
        html.Div([], id = "file-separator-do-nothing"),
        html.Div([], id = "file-header-do-nothing"),
        html.Div([], id = "clear-home-do-nothing"),
        html.Div([], id = "reset-app-do-nothing")
])

@app.callback(Output("data-upload-msg", "children"),
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename')]
)
def upload_data(contents, filename):
    """Upload Files and Regenerate the file list."""
    if contents:
        for i in range(len(filename)):
            FileUtils.upload(filename[i], contents[i])
        return common.success_msg('File Uploaded Successfully: ' + str(filename))
    return ""

@app.callback(
    Output("selected-file", "options"),
    [Input('home-load-raw-files', 'n_clicks')]
)
def load_upload_raw_data(n_clicks):
    files = FileUtils.files('raw')
    if len(files) == 0:
        options=[{'label':'No files uploaded yet!', 'value':'None'}]
        return options
    else:
        options=[{'label':file, 'value':file} for file in files]
        return options

@app.callback(
    Output("display-file", "children"),
    [Input('selected-file', 'value')]
)
def display_data(value):
    """Displaying the head for the selected file."""
    db_value = db.get("file")
    if value is None and db_value is None:
        return ""
    elif value is None and not db_value is None:
        value = db_value
    elif not value == db_value:
        db.reset()
    format = FileUtils.file_format(value)
    if format == 'csv' or format == 'txt':
        path = FileUtils.path('raw', value)
        head = DataUtils.read_text_head(path)
        table_col = [html.Col(style = {'width':"10%"}), html.Col(style = {'width':"90%"})]
        table_header = [html.Thead(html.Tr([html.Th("Row No"), html.Th("Data")]))]
        rows = []
        for i in range(len(head)):
            row = html.Tr([html.Td(i+1), html.Td(head[i])])
            rows.append(row)
        table_body = [html.Tbody(rows)]
        table = dbc.Table(table_col+ table_header + table_body, bordered=True, style = common.table_style)
        div =  [common.msg("Selected File: " + value),
                common.msg("Selected Format: " + format),
                table,
                html.Br(),
                csv_properties_div]
    elif format == 'xls' or format == 'xlsx':
        path = FileUtils.path('raw', value)
        xls = pd.ExcelFile(path)
        sheets = xls.sheet_names
        div =  [common.msg("Selected File: " + value),
                common.msg("Selected Format: " + format),
                common.msg("Select Sheet:"),
                html.Div([
                dcc.Dropdown(
                    id = 'xls-file-sheet',
                    options=[{'label':sheet, 'value':sheet} for sheet in sheets],
                    value=None,
                    multi=False)
                ],
                style = {'margin': '10px', 'width': '50%'}),
                html.Div([], id = "display-xls-file")]
    else:
        div = "Format Not Supported!!"
    db.put("file", value)
    db.put("format", format)
    return div

csv_properties = dbc.Card([
    dbc.FormGroup([
        html.H2("Apply File Properties"),
        dbc.Label("Header"),
        dcc.Dropdown(
            id="file-header",
            options=[{'label':"True", 'value':1}, {"label": "False", "value": 0}],
            value=None,
            multi=False),
        dbc.Label("Separator"),
        dbc.Input(id="file-separator", placeholder="Separator", type="text", step=1),
        html.Br(),
        dbc.Button("Apply", color="primary", id = 'file-apply-properties')],
        style = {'padding': '10px'})
    ])

csv_properties_div = html.Div([
    dbc.Row([
        dbc.Col(csv_properties, md=4)
    ],
    align="center")
],
style = {'margin': '10px', 'font-size': '16px'})

@app.callback(
    Output("file-properties", "children"),
    [Input('file-apply-properties', 'n_clicks')]
)
def apply_file_properties(n):
    file = db.get("file")
    format = db.get("format")
    sep = db.get("file_separator")
    header = db.get("file_header")
    div = None
    df = None
    if format is None:
        div = None
        return div
    elif (format == 'csv' or format == 'txt' or format == 'xls' or format == 'xlsx') and header is None:
        div= common.error_msg('Please Select Header!!')
        return div
    elif format == 'csv' or format == 'txt':
        if sep is None:
            sep = ','
            db.put("file_separator", sep)
        path = FileUtils.path('raw', file)
        df = DataUtils.read_csv(path, sep, header)
        msg = "Following Properties Applied. Separator=" + sep + " Header="+ str(header)
    elif format == 'xls' or format == 'xlsx':
        path = FileUtils.path('raw', file)
        sheet = db.get("sheet")
        df = DataUtils.read_xls(path, sheet, header)
        print(df)
        msg = "Following Properties Applied. Header="+ str(header)

    table = dbc.Table.from_dataframe(df.head(10), striped=True, bordered=True, hover=True, style = common.table_style)
    button = dbc.Button("Clean & Save", color="primary", id = 'clean-save-file')
    div = [common.msg(msg), table,
            html.Div([
                button,
                html.Br(),
                html.Div([], id = "cleaned-saved-file")
            ], style = {'padding': '10px', 'textAlign': 'center'})]
    db.put("raw_data", df)
    return div

@app.callback(
    Output("cleaned-saved-file", "children"),
    [Input('clean-save-file', 'n_clicks')]
)
def clean_save_file(n):
    ## Team 2 API Integration
    df = db.get("raw_data")
    file = db.get("file")
    sheet = db.get("sheet")
    msg = ""
    if (not n is None) and (not df is None):
        try:
            cleaned_df = data_cleaning(df)
            if not sheet is None:
                file = FileUtils.append_file_name(file, sheet)
            file = file.split('.')[0]
            path = FileUtils.path('clean', file)
            cleaned_df.to_csv(path, index=False)
            msg = "File is Cleaned & Saved Successfully!!"
        except Exception as e:
            return common.error_msg("Data Cleansing API Error: " + str(e))
    return common.msg(msg)


@app.callback(
    Output('file-separator-do-nothing' , "children"),
    [Input('file-separator', 'value')]
)
def file_separator(value):
    if not value is None:
        db.put("file_separator", value)
    return None

@app.callback(
    Output('file-header-do-nothing' , "children"),
    [Input('file-header', 'value')]
)
def file_header_true(value):
    if value == 1:
        db.put("file_header", True)
    elif value == 0:
        db.put("file_header", False)
    return None

@app.callback(
    Output('clear-home-do-nothing', 'children'),
    [Input('clear-home', 'value')]
)
def clear(value):
    return html.A(href='/')

@app.callback(
    Output('reset-app-do-nothing' , "children"),
    [Input('reset-app', 'value')]
)
def reset(value):
    return ""

@app.callback(
    Output('display-xls-file' , "children"),
    [Input('xls-file-sheet', 'value')]
)
def xls_file_sheet(value):
    file = db.get("file")
    div = None
    db_value = db.get("sheet")
    if value is None and db_value is None:
        div = []
    elif value is None and not db_value is None:
        value = db_value
    if not value is None:
        db.put('sheet', value)
        path = FileUtils.path('raw', file)
        xls = pd.ExcelFile(path)
        df = pd.read_excel(xls, value)
        table = html.Div([
            dash_table.DataTable(
                data=df.iloc[:10].to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in df.columns]
            ),
            html.Hr(),
        ])
        div = [html.Br(),
                table,
                html.Br(),
                xls_properties_div]
    return div

xls_properties = dbc.Card([
    dbc.FormGroup([
        html.H2("Apply File Properties"),
        dbc.Label("Header"),
        dcc.Dropdown(
            id="file-header",
            options=[{'label':"True", 'value':1}, {"label": "False", "value": 0}],
            value=None,
            multi=False),
        html.Br(),
        dbc.Button("Apply", color="primary", id = 'file-apply-properties'),
        ],
        style = {'padding': '10px'})
    ])

xls_properties_div = html.Div([
    dbc.Row([
        dbc.Col(xls_properties, md=4)
    ],
    align="center")
],
style = {'margin': '10px', 'font-size': '16px'})
