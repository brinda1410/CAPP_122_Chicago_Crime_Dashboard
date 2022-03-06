import pandas as pd
import plotly.express as px
from maindash import app
from dash import html, dcc
from dash.dependencies import Input, Output

# Read csv
merged_filename = "data/merged_data.csv"
crimes = pd.read_csv(merged_filename)

# Subset ward and crime-type columns
crimes = crimes.loc[:, 'WARD': 'WEAPONS VIOLATION']
crimes.drop(['FS AGENCIES', 'SB FUNDS', 'MICRO LOANS'], axis = 1, inplace = True)
col_names = crimes.columns[1:] # without WARD column

# App Layout - DCC and HTML components
crime_layout = html.Div([
        html.H2("Crime Data", style = {'text-align': 'left'}),
        html.Br(),
        html.Label(['Select Type of Crime:'], style={'font-weight': 'bold', "text-align": "left"}),
        html.Br(),
        dcc.Dropdown(id = "select_crimetype",
                    options = [{"label": str(x), "value": x} for x in col_names],
                    value = col_names[0],
                    multi = False,
                    style = {'width': "40%"}),
        #html.Div(id = 'output_container', children = []),
        dcc.Graph(id = 'bar_graph_crime_type_by_ward', figure = {})
    ])

# Connect Plotly graphs with Dash Core Components
@app.callback(
    Output(component_id = 'bar_graph_crime_type_by_ward', component_property = 'figure'),
    [Input(component_id = 'select_crimetype', component_property = 'value')]
    )

def update_graph(crime_slctd):
    '''
    Define the callback function to render filtered
    pandas dataframe based on user's input value in Dropdown
    'select_crimetype'
    '''
    #container_crime = "The crime type selected by the user is {}".format(crime_slctd)
    crimes_copy = crimes.copy()
    crimes_copy.dropna(subset=[crime_slctd], inplace = True)
    graphtitle = crime_slctd.lower().capitalize() + ' crimes disaggregated at ward-level'
    fig = px.bar(crimes_copy, x = 'WARD', y = crime_slctd, title = graphtitle)
    return fig

