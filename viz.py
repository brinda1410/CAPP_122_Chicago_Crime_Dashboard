##############################################################
 
# ------ Type following in command line bash - python3 viz.py
# ------ Pending creation of virtual environment to run from 
#        command line
# ------ Explore if possible to work with merged data
##############################################################

import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
app = dash.Dash(__name__)

# Hard-coded filename
fsa_filename = "data/FSA.csv"
crimes_filename = "data/Crimes.csv"
mloans_filename = "data/Microloans.csv"
sb_filename = "data/SB.csv"

# Read csv
fsa = pd.read_csv(fsa_filename)
crimes = pd.read_csv(crimes_filename)
mloans = pd.read_csv(mloans_filename)
sb = pd.read_csv(sb_filename)

# Crime Data
crimes = crimes.loc[:,['Ward', 'Location', 'Primary Type', 'Domestic', 'Arrest', 'Beat']]
crimes.dropna(subset=['Ward', 'Primary Type'], inplace = True)
ward_ids = crimes['Ward'].unique()
#primary_typ = crimes['Primary Type'].unique()

# App Layout - DCC and HTML components
app.layout = html.Div([
    html.H1("Ward-Level Crime Data (Chicago, 2020)", style = {'text-align': 'center'}),
    
    html.Label(['Select Ward:'], style={'font-weight': 'bold', "text-align": "left"}),
    dcc.Dropdown(id = "select_ward",
                options = [{"label": str(x), "value": x} for x in ward_ids],
                value = ward_ids[0],
                multi = False,
                style = {'width': "40%"}
                ),
    html.Div(id = 'output_container', children = []),
    html.Br(),
    dcc.Graph(id = 'bar_graph_crime_type_by_ward', figure = {})
])

# Connect Plotly graphs with Dash Core Components

@app.callback(
    [Output(component_id = 'output_container', component_property = 'children'),
    #Output(component_id = '?', component_property = 'children'),
    Output(component_id = 'bar_graph_crime_type_by_ward' , component_property = 'figure')],
    [Input(component_id = 'select_ward', component_property = 'value')]
    #Input(component_id = 'select_crime_typ', component_property = 'value')
    )

def update_graph(ward_slctd): #add argument for crime_slctd
    '''
    Define the callback function to render filtered
    pandas dataframe based on user's input value in Dropdown
    'select_ward'
    '''
    print(ward_slctd)
    #print(crime_slctd)
    container_ward = "The ward selected by the user has the ID {}".format(ward_slctd)
    #container_crime = "The crime type selected by the user is {}".format(crime_slctd)
    
    crimes_copy = crimes.copy()
    crimes_copy = crimes_copy[(crimes_copy['Ward'] == ward_slctd)]
    # & (crimes_copy['Primary Type'] == crime_slctd)

    # Plotly Express
    crimes_count = crimes_copy['Primary Type'].value_counts().rename_axis('Primary Type').reset_index(name='Counts')
    fig = px.bar(crimes_count, x = 'Primary Type', y = 'Counts', title = 'Crimes disaggregated at ward-level')
    
    return container_ward, fig
    # add container_crime to return statement if another user input added

if __name__ == '__main__':
    app.run_server(debug=True)

'''

html.Label(['Select Crime Type:'], style={'font-weight': 'bold', "text-align": "left"}),
dcc.Dropdown(id = "select_crime_typ",
            options = [{"label": str(x), "value": x} for x in primary_typ],
            value = primary_typ[0],
            multi = False,
            style = {'width': "60%"}
            ), 
html.Br(),

options = [    
                    {"label": "1", "value": 1},
                    {"label": "2", "value": 2},
                    {"label": "3", "value": 3},
                    {"label": "4", "value": 4},
                    {"label": "5", "value": 5},
                    {"label": "6", "value": 6},
                    {"label": "7", "value": 7},
                    {"label": "8", "value": 8},
                    {"label": "9", "value": 9},
                    {"label": "10", "value": 10},                    
                    {"label": "11", "value": 11},
                    {"label": "12", "value": 12},
                    {"label": "13", "value": 13},
                    {"label": "14", "value": 14},
                    {"label": "15", "value": 15},
                    {"label": "16", "value": 16},
                    {"label": "17", "value": 17},
                    {"label": "18", "value": 18},
                    {"label": "19", "value": 19},
                    {"label": "20", "value": 20},                
                    {"label": "21", "value": 21},
                    {"label": "22", "value": 22},
                    {"label": "23", "value": 23},
                    {"label": "24", "value": 24},
                    {"label": "25", "value": 25},                
                    {"label": "26", "value": 26},
                    {"label": "27", "value": 27},
                    {"label": "28", "value": 28},
                    {"label": "29", "value": 29},
                    {"label": "30", "value": 30},
                    {"label": "31", "value": 31},
                    {"label": "32", "value": 32},
                    {"label": "33", "value": 33},
                    {"label": "34", "value": 34},
                    {"label": "35", "value": 35},
                    {"label": "36", "value": 36},
                    {"label": "37", "value": 37},
                    {"label": "38", "value": 38},
                    {"label": "39", "value": 39},
                    {"label": "40", "value": 40},
                    {"label": "41", "value": 41},
                    {"label": "42", "value": 42},
                    {"label": "43", "value": 43},
                    {"label": "44", "value": 44},
                    {"label": "45", "value": 45},
                    {"label": "46", "value": 46},
                    {"label": "47", "value": 47},
                    {"label": "48", "value": 48},
                    {"label": "49", "value": 49},
                    {"label": "50", "value": 50}
                    ]

options = [    
                    {"label": "BATTERY", "value": BATTERY},
                    {"label": "THEFT", "value": THEFT},
                    {"label": "CRIMINAL DAMAGE", "value": CRIMINAL DAMAGE},
                    {"label": "ASSAULT", "value": ASSAULT},
                    {"label": "DECEPTIVE PRACTICE", "value": DECEPTIVE PRACTICE},
                    {"label": "OTHER OFFENSE ", "value": OTHER OFFENSE },
                    {"label": "MOTOR VEHICLE THEFT", "value": MOTOR VEHICLE THEFT},
                    {"label": "BURGLARY", "value": BURGLARY},
                    {"label": "WEAPONS VIOLATION ", "value": WEAPONS VIOLATION },
                    {"label": "ROBBERY", "value": ROBBERY},                    
                    {"label": "NARCOTICS", "value": NARCOTICS},
                    {"label": "CRIMINAL TRESPASS", "value": CRIMINAL TRESPASS},
                    {"label": "OFFENSE INVOLVING CHILDREN", "value": OFFENSE INVOLVING CHILDREN},
                    {"label": "PUBLIC PEACE VIOLATION", "value": PUBLIC PEACE VIOLATION},
                    {"label": "CRIMINAL SEXUAL ASSAULT", "value": CRIMINAL SEXUAL ASSAULT},
                    {"label": "SEX OFFENSE", "value": SEX OFFENSE},
                    {"label": "HOMICIDE", "value": HOMICIDE},
                    {"label": "INTERFERENCE WITH PUBLIC OFFICER", "value": INTERFERENCE WITH PUBLIC OFFICER},
                    {"label": "ARSON", "value": ARSON},
                    {"label": "PROSTITUTION", "value": PROSTITUTION},                
                    {"label": "STALKING", "value": STALKING},
                    {"label": "INTIMIDATION", "value": INTIMIDATION},
                    {"label": "CONCEALED CARRY LICENSE VIOLATION", "value": CONCEALED CARRY LICENSE VIOLATION},
                    {"label": "LIQUOR LAW VIOLATION", "value": LIQUOR LAW VIOLATION},
                    {"label": "KIDNAPPING", "value": KIDNAPPING},                
                    {"label": "CRIM SEXUAL ASSAULT", "value": CRIM SEXUAL ASSAULT},
                    {"label": "OBSCENITY", "value": OBSCENITY},
                    {"label": "GAMBLING", "value": GAMBLING},
                    {"label": "PUBLIC INDECENCY", "value": PUBLIC INDECENCY},
                    {"label": "OTHER NARCOTIC VIOLATION", "value": OTHER NARCOTIC VIOLATION},
                    {"label": "HUMAN TRAFFICKING", "value": HUMAN TRAFFICKING},
                    {"label": "NON-CRIMINAL", "value": NON-CRIMINAL},
                    {"label": "RITUALISM", "value": RITUALISM}
                    ]
'''