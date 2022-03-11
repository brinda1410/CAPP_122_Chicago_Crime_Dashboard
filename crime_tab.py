'''
Render graph on Crime Tab only
'''

import pandas as pd
import plotly.express as px
from maindash import app
from dash import html, dcc
from dash.dependencies import Input, Output

# Read csv
merged_filename = "data/merged_data.csv"
crimes = pd.read_csv(merged_filename)

# Subset WARD and crime-type columns
crimes = crimes.loc[:, 'WARD': 'WEAPONS VIOLATION']
crimes.drop(['FS AGENCIES', 'SB FUNDS', 'MICRO LOANS'],
            axis = 1,
            inplace = True)

# Remove WARD column
col_names = crimes.columns[1:]

# ---------------------------- FRONT-END -------------------------------
# App layout for Crime tab

crime_layout = html.Div([
        html.H2("Crime Data", style = {'text-align': 'left'}),
        html.Br(),
        html.Label(['Select Type of Crime:'], style={'font-weight': 'bold',
                                                     "text-align": "left"}),
        html.Br(),
        dcc.Dropdown(id = "select_crimetype",
                    options = [{"label": str(x), "value": x} for x in col_names],
                    value = col_names[0],
                    multi = False,
                    style = {'width': "40%"}),
        dcc.Graph(id = 'bar_graph_crime_type_by_ward', figure = {})
    ])

# --------------------------- BACKEND -----------------------------------  
# Connect the figure contained in Dash Core Components with the frontend

@app.callback(Output(component_id = 'bar_graph_crime_type_by_ward', component_property = 'figure'),
            [Input(component_id = 'select_crimetype', component_property = 'value')])

def update_graph(crime_slctd):
    '''
    Render the graph on the Crime tab based on
    based on user's input value in Dropdown component
    'select_crimetype'. This returned figure
    feeds into the crime_layout variable which
    stores the frontend for Crime tab.

    Input: 
        crime_slctd - value selected by user in the dropdown component
    '''
    crimes_copy = crimes.copy()
    crimes_copy.dropna(subset=[crime_slctd], inplace = True)
    graphtitle = crime_slctd.lower().capitalize() + ' crimes disaggregated at ward-level'
    fig = px.bar(crimes_copy, x = 'WARD',
                            y = crime_slctd,
                            title = graphtitle)
    #fig.layout.plot_bgcolor = '#DCDCDC'
    #fig.layout.paper_bgcolor = '#fff'
    
    #color = crime_slctd,
    #                        color_continuous_scale = 'RdBu',
    return fig
