from dash import html, dcc
from dash.dependencies import Input, Output
from maindash import app
import plotly.express as px

# Connect to the layout and callback of different tabs
from crime_tab import crime_layout
from social_inv_tab import si_layout

# App Layout with Tabs
def make_layout():
    '''
    App layout with tabs
    '''
    return html.Div([
        html.H1("Ward-level data, Chicago (2020)", style = {"textAlign": "center"}),
        html.Hr(),
        dcc.Tabs(id = "tabs", value = "tab-crime", children = 
            [
                dcc.Tab(label="Crime", value="tab-crime"),
                dcc.Tab(label="Social Investment", value = "tab-si"),
                #dcc.Tab(label="Small Businesses", value = "tab-sb"),
               # dcc.Tab(label="Microloans", value = "tab-microloan")
            ]),
        html.Div(id = 'content', children = [])
    ])

# Connect Plotly graphs with Dash Core Components
@app.callback(
    Output("content", "children"),
    [Input("tabs", "value")]
)

# Render the selected tab
def select_tab(tab_slctd):
    '''
    Define the callback function to render the 
    chosen tab
    '''
    if tab_slctd == "tab-crime":
        return crime_layout
    elif tab_slctd == "tab-si":
        return si_layout