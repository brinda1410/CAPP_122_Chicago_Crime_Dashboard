from dash import html, dcc
from dash.dependencies import Input, Output
from maindash import app
import plotly.express as px

# Import the rendered layouts of all tabs
from crime_tab import crime_layout
from social_inv_tab import si_layout

# ---------------------------- FRONT-END -------------------------------
# App layout with a collection of tabs

def make_layout():
    '''
    Creates an app layout with 4 tabs.
    '''
    return html.Div([
        html.H1("Ward-level data, Chicago (2020)", style = {"textAlign": "center"}),
        html.Hr(),
        dcc.Tabs(id = "tabs", value = "tab-crime", children = 
            [
                dcc.Tab(label="Crime", value="tab-crime"),
                dcc.Tab(label="Social Investment", value = "tab-si")
            ]),
        html.Div(id = 'content', children = [])
    ])

# --------------------------- BACKEND -----------------------------------  
# Connect the figure contained in Dash Core Components with the frontend

@app.callback(
    Output("content", "children"),
    [Input("tabs", "value")]
)

def select_tab(tab_slctd):
    '''
    Render the graph on the tab selected by the user.
    Each return statement corresponds to a module for 
    that tab and it returns a figure. This returned figure
    feeds into the function make_layout() to be displayed
    to the user through html div component with id = 'content'.

    Input: 
        tab_slctd - value of current tab selected by the user
    '''
    if tab_slctd == "tab-crime":
        return crime_layout

    elif tab_slctd == "tab-si":
        return si_layout