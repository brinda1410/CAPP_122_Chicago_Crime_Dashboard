'''
Render graph on Social Investment Tab only
'''

import pandas as pd
import plotly.express as px
from crimes_app.dashboard.maindash import app
from dash import html, dcc
from dash.dependencies import Input, Output
import os

BASE_DIR = os.path.join( os.path.dirname( __file__ ), '..' )
TEST_DATA_DIR = os.path.join(BASE_DIR, "data")

# Read csv
merged_filename = os.path.join(TEST_DATA_DIR, "merged_data.csv")
social_inv = pd.read_csv(merged_filename)

# Subset ward and social-inv-type columns
social_inv = social_inv.loc[:, 'WARD': 'MICRO LOANS']
social_inv.dropna( axis = 0, inplace = True)
col_names = social_inv.columns[1:] # without WARD column

# ---------------------------- FRONT-END -------------------------------
# App layout for Social Investment tab
si_layout = html.Div([
        html.H2("Social Investment Data", style = {'text-align': 'left'}),
        html.Br(),
        html.Label(['Select Type of Intervention:'], style={'font-weight':'bold',
                                                            "text-align": "left"}),
        html.Br(),
        dcc.Dropdown(id = "select_type",
                    options = [{"label": str(x), "value": x} for x in col_names], 
                    value = col_names[0],
                    multi = False,
                    style = {'width': "40%"}),
        dcc.Graph(id = 'bar_social_inv_by_ward', figure = {})
    ])

# --------------------------- BACKEND -----------------------------------  
# Connect the figure contained in Dash Core Components with the frontend
@app.callback(Output(component_id = 'bar_social_inv_by_ward', component_property = 'figure'),
            [Input(component_id = 'select_type', component_property = 'value')])

def update_graph(si_slctd):
    '''
    Render the graph on the Social Investment tab based on based on user's input
    value in Dropdown component 'select_type'. This returned figure feeds into
    the si_layout variable which stores the frontend for Social Investment tab.
    Input: 
        si_slctd - value selected by user in the dropdown component
    '''
    SI_copy = social_inv.copy()
    SI_copy.dropna(subset=[si_slctd], inplace = True)

    if si_slctd == "FS AGENCIES":
        graphtitle = "Number of Family Support Agencies disaggregated at ward-level"
    elif si_slctd == "SB FUNDS":
        graphtitle = "Total investment through the Small Business Improvement Fund disaggregated at ward-level"
    else:
        graphtitle = "Number of loans given by the Chicago Microlending institute disaggregated at ward-level"

    fig = px.bar(SI_copy, x = 'WARD',
                        y = si_slctd,
                        title = graphtitle)
    fig.layout.plot_bgcolor = '#f3f3f0'

    return fig