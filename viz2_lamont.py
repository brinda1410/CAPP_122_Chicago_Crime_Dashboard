##############################################################
 
# ------ Run in command line bash: python3 viz.py
# ------ Pending creation of virtual environment to run from 
#        command line
# ------ Explore if possible to work with merged data
##############################################################

import plotly.express as px
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output


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


# Hardcoded filename
merged_filename = "data/merged_data.csv"

# Read csv
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
    html.Div(id = 'output_container', children = []),
    dcc.Graph(id = 'bar_graph_crime_type_by_ward', figure = {})
])

# Connect Plotly graphs with Dash Core Components

@app.callback(
    [Output(component_id = 'output_container', component_property = 'children'),
    Output(component_id = 'bar_graph_crime_type_by_ward' , component_property = 'figure')],
    [Input(component_id = 'select_crimetype', component_property = 'value')]
    )

def update_graph(crime_slctd):
    '''
    Define the callback function to render filtered
    pandas dataframe based on user's input value in Dropdown
    'select_crimetype'
    '''
    container_crime = "The crime type selected by the user is {}".format(crime_slctd)
    print(container_crime)
    crimes_copy = crimes.copy()
    crimes_copy.dropna(subset=[crime_slctd], inplace = True)
    print(crime_slctd)
    fig = px.bar(crimes_copy, x = 'WARD', y = crime_slctd, title = 'Crimes disaggregated at ward-level')
    return container_crime, fig


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
    print("Got here")
    if tab_slctd == "tab-crime":
        return crime_layout
    # add other if-statements for other tabs

if __name__ == '__main__':
    app.run_server(debug=True)
