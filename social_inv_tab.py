import pandas as pd
import plotly.express as px
from maindash import app
from dash import html, dcc
from dash.dependencies import Input, Output

# Read csv

merged_filename = "data/merged_data.csv"
social_inv = pd.read_csv(merged_filename)

# Subset ward and crime-type columns
social_inv = social_inv.loc[:, 'WARD': 'MICRO LOANS']
social_inv.dropna( axis = 0, inplace = True)
print(social_inv)
col_names = social_inv.columns[1:] # without WARD column

# App Layout - DCC and HTML components
si_layout = html.Div([
        html.H2("Social Investment Data", style = {'text-align': 'left'}),
        html.Br(),
        html.Label(['Select Type of Intervention:'], style={'font-weight': 'bold', "text-align": "left"}),
        html.Br(),
        dcc.Dropdown(id = "select_type",
                    options = [{"label": str(x), "value": x} for x in col_names], 
                    value = col_names[0],
                    multi = False,
                    style = {'width': "40%"}),
        #html.Div(id = 'output_container', children = []),
        dcc.Graph(id = 'bar_social_inv_by_ward', figure = {})
    ])

# Connect Plotly graphs with Dash Core Components
@app.callback(
    Output(component_id = 'bar_social_inv_by_ward', component_property = 'figure'),
    [Input(component_id = 'select_type', component_property = 'value')]
    )

def update_graph(si_slctd):
    '''
    Define the callback function to render filtered
    pandas dataframe based on user's input value in Dropdown
    'small_bussines_incentives'
    '''
    #container_social investment = "The SI type selected by the user is {}".format(sb_slctd)
    SI_copy = social_inv.copy()
    SI_copy.dropna(subset=[si_slctd], inplace = True)
    graphtitle = si_slctd.lower().capitalize() + 'social investment disaggregated at ward-level'
    fig = px.bar(SI_copy, x = 'WARD', y = si_slctd, title = graphtitle)

    return fig