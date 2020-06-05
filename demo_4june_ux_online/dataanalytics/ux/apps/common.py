import dash_bootstrap_components as dbc
import dash_html_components as html

import pandas as pd

def navbar(page_name: str):
    nav = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(page_name)),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Linear Regression", href="/apps/linear-regression", id = "linear-regression", style = {'font-size': '16px'}),
                    dbc.DropdownMenuItem("Higher Order Regression", href="/apps/higher-order-regression", id = "higher-order-regression", style = {'font-size': '16px'}),
                    dbc.DropdownMenuItem("Regression Comparison", href="/apps/regression-comparison", id = "regression-comparison", style = {'font-size': '16px'}),
                    dbc.DropdownMenuItem("Time Series Analysis", href="/apps/time-series-analysis", id = "time-series-analysis", style = {'font-size': '16px'})
                ],
                nav=True,
                in_navbar=True,
                label="Projects",
                style = {'padding-left': 20, 'padding-right': 50},
            ),
        ],
        brand="Data Analytics Tool - Online Team",
        brand_href="/",
        color="#25383C",
        dark=True,
        style = {'font-size': '16px'},
        brand_style = {'font-size': '16px'}
    )
    return nav

table_style = {'margin': '10px', 'font-size':'16px', 'padding': '20px'}

def msg(msg: str):
    if msg is None:
        return None
    return html.Div([
        html.H2(children = msg,
            style = {'margin': '10px', 'font-size': '16px'}),
            html.Br()])

def success_msg(msg: str):
    if msg is None:
        return None
    return html.Div([
        html.H2(children = msg,
            style = {'margin': '10px', 'font-size': '16px', 'color': 'green'}),
            html.Br()])

def error_msg(msg: str):
    if msg is None:
        return None
    return html.Div([
        html.H2(children = msg,
            style = {'margin': '10px', 'font-size': '16px', 'color': 'red'}),
            html.Br()])

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
    ], style = {'font-size': '12px'})


### Regression Common ###

def get_anova_div(anova: {}):
    anova_df = pd.DataFrame(columns=['Source', 'Sum of Squares', 'Degrees fo Freedom', 'Mean Square', 'F Statistic'])
    anova_df.loc[0] = ['Regression', anova['SSR'],anova['DFR'], anova['MSR'], round(anova['F'], 4)]
    anova_df.loc[1] = ['Error', anova['SSE'],anova['DFE'], anova['MSE'], '']
    anova_df.loc[2] = ['Total', anova['SST'],anova['DFT'], anova['S2'], '']
    anova_df = anova_df.round(4)

    anova_div = html.Div([
        dbc.Table.from_dataframe(anova_df, striped=True, bordered=True, hover=True, style = table_style)
    ], style = {'margin':'10px'})
    return anova_div

def get_stats_df(summary: {}, x_col: [], y_col: str):
    for dict_value in summary:
        for k, v in dict_value.items():
            dict_value[k] = round(v, 4)
    df_stats = pd.DataFrame(summary)
    c = x_col + [y_col]
    df_stats['Var_Name'] = c
    df_stats = df_stats[['Var_Name','count','min','max','mean','variance','std','covariance','r']]
    return df_stats

def get_coeff_df(params: [], x_col: []):
    col = []
    for c in x_col:
        col.append(c)
    col.append('Constant')
    params = [ '%.4f' % elem for elem in params ]
    df_coeff = pd.DataFrame(params, columns=['Coefficient'])
    df_coeff['Var_Name'] = col
    df_coeff = df_coeff[['Var_Name','Coefficient']]
    return df_coeff

def hor_get_coeff_df(params: []):
    row = ['β_0', 'β_1']
    for c in range(2,len(params)):
        temp = 'β_' + str(c)
        row.append(temp)
    params = [ '%.4f' % elem for elem in params ]
    df_coeff = pd.DataFrame(params, columns=['Value'])
    df_coeff['Coefficient'] = row
    df_coeff = df_coeff[['Coefficient','Value']]
    return df_coeff
