import dash_bootstrap_components as dbc
import dash_html_components as html

def navbar(page_name: str):
    nav = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(page_name)),
            dbc.DropdownMenu(
                children=[
                    #dbc.DropdownMenuItem("Home", href="/home", id = "home-refresh", style = {'font-size': '16px'}),
                    dbc.DropdownMenuItem("Linear Regression", href="/apps/linear-regression", id = "linear-regression", style = {'font-size': '16px'}),
                    dbc.DropdownMenuItem("Higher Order Regression", href="/apps/higher-order-regression", id = "higher-order-regression", style = {'font-size': '16px'})
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
