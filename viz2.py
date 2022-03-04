##############################################################
 
# ------ Run in command line bash: python3 viz.py
# ------ Pending creation of virtual environment to run from 
#        command line
# ------ Explore if possible to work with merged data
##############################################################

import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# Connect to the layout and callback of crime_tab.py
from crime_tab import crime_layout

# Initialize app
app = dash.Dash(__name__)

# App Layout with Tabs
app.layout = html.Div([
    html.H1("Ward-level data, Chicago (2020)", style = {"textAlign": "center"}),
    html.Hr(),
    dcc.Tabs(id = "tabs", value = "tab-crime", children = 
        [
            dcc.Tab(label="Crime", value="tab-crime"),
            dcc.Tab(label="FSA", value = "tab-fsa"),
            dcc.Tab(label="Small Businesses", value = "tab-sb"),
            dcc.Tab(label="Microloans", value = "tab-microloan")
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
    # add other if-statements for other tabs

if __name__ == '__main__':
    app.run_server(debug=True)
