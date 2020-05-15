import dash_bootstrap_components as dbc
import dash_html_components as html

import pandas as pd

def navbar(page_name: str):
    nav = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(page_name)),
            dbc.DropdownMenu(
                children=[
                    #dbc.DropdownMenuItem("Home", href="/home", id = "home-refresh", style = {'font-size': '16px'}),
                    dbc.DropdownMenuItem("Linear Regression", href="/apps/linear-regression", id = "linear-regression", style = {'font-size': '16px'}),
                    dbc.DropdownMenuItem("Higher Order Regression", href="/apps/higher-order-regression", id = "higher-order-regression", style = {'font-size': '16px'}),
                    dbc.DropdownMenuItem("Regression Comparison", href="/apps/regression-comparison", id = "regression-comparison", style = {'font-size': '16px'})
                ],
                nav=True,
                in_navbar=True,
                label="Projects",
                style = {'padding-left': 20, 'padding-right': 50},
            ),
        ],
        brand="Data Analytics Tool",
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
    anova_df = pd.DataFrame(columns=['Source', 'Sum of Squares', 'Degrees fo Freedom', 'Mean Square'])
    anova_df.loc[0] = ['Regression', anova['ssr'],anova['dfR'], anova['msr']]
    anova_df.loc[1] = ['Error', anova['sse'],anova['dfE'], anova['mse']]
    anova_df.loc[2] = ['Total', anova['sst'],anova['dfT'], anova['s2']]

    anova_div = html.Div([
        dbc.Table.from_dataframe(anova_df, striped=True, bordered=True, hover=True, style = table_style),
        html.P('F Statistics = ' + str(anova['f']))
    ], style = {'margin':'10px'})
    return anova_div

def get_stats_df(summary: {}, x_col: [], y_col: str):
    for dict_value in summary:
        for k, v in dict_value.items():
            dict_value[k] = round(v, 4)
    df_stats = pd.DataFrame(summary)
    c = [y_col] + x_col
    df_stats['Var_Name'] = c
    df_stats = df_stats[['Var_Name','count','min','max','mean','variance','std','covariance','r', 'pr']]
    del df_stats['pr']
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
