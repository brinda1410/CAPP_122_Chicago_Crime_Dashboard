'''
This module runs the lineal regression, computes the index and build the heatmap layout. 
'''

import numpy as np
import pandas as pd
import plotly.express as px
import geopandas as gpd
import pyproj
from crimes_app.dashboard.maindash import app
from dash import html, dcc
from dash.dependencies import Input, Output
import os

BASE_DIR = os.path.join( os.path.dirname( __file__ ), '..' )
TEST_DATA_DIR = os.path.join(BASE_DIR, "data")

# Read csv
merged_filename = os.path.join(TEST_DATA_DIR, "merged_data.csv")
df = pd.read_csv(merged_filename)

crimes = df.columns.tolist()[4:]

# Run the regression model and predict errors:
df['ALL CRIMES'] = df[crimes].sum(axis=1)
y = df.loc[:, ['ALL CRIMES']].values
X = df[['FS AGENCIES', 'SB FUNDS', 'MICRO LOANS']].fillna(0)
X = np.concatenate((X, np.ones((X.shape[0])).reshape(-1, 1)), axis = 1)
betas = np.linalg.lstsq(X, y,rcond = None)[0]
error = y - np.matmul(X, betas)

# Calculate index from errors
if min(error) >= 0:
    error = error / max(error)
else:
    div = max(max(error), -min(error))
    error = error / div

# Reduced dataframe with target variables
df["INDEX ANALYSIS"] = error.reshape(1, 50)[0]
va_int = ['WARD', 'INDEX ANALYSIS','FS AGENCIES',
          'SB FUNDS', 'MICRO LOANS','ALL CRIMES']
col_names = va_int[1:]
df = df[va_int].fillna(0)
df["WARD"] = df["WARD"].astype(str)

# GeoPandas dataframe
fp = os.path.join(TEST_DATA_DIR, "WARDS_2015.shx")
map_df = gpd.read_file(fp)
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
map_df = map_df.merge(df, on = 'WARD').set_index('WARD')

# ---------------------------- FRONT-END -------------------------------
# App layout for the Chicago choropleth map tab
hm_layout = html.Div([
        html.H4('Chicago Choropleth Map'),
        html.P("Select Variable:"),
        dcc.RadioItems(
            id="select_type", 
            options=[{"label": str(x), "value": x} for x in col_names],
            value=col_names[0],
            inline=True),
        dcc.Graph(id = 'map_by_ward', figure = {}),
        dcc.Textarea(readOnly = True,
                     wrap  = True,
                     value = 'Based on the idea that policymakers should direct more funding to the most vulnerable communities to equate opportunities, ' +
                            'we explore the relationship between crimes incidence and social investment through a multivariate regression model using the ' + 
                            'number of crimes (ALL CRIMES) at ward level as dependent variable, and multiple proxies of social investment described in previous ' +
                            'tabs as regressors. Using the residuals of this model, we build an index (INDEX ANALYSIS) between -1 and 1 which shows how this ' + 
                            'relationship across wards. In a ideal scenario, the choroplet must be "uninformative" as far as the ratio "investment"/"crime" would be homogeneous '+
                            'across wards. Otherwise, negative values could give us signals social underinvestment.',
                     style = {"width" : "100%", 'height': 80})
        ])

# --------------------------- BACKEND -----------------------------------  
# Connect the figure contained in Dash Core Components with the frontend

@app.callback(Output(component_id = 'map_by_ward', component_property = 'figure'),
            [Input(component_id = 'select_type', component_property = 'value')])

def update_graph(si_slvaluectd):
    '''
    Render the Chicago choropleth map based on user's input value in Dropdown
    component 'select_type'. This returned figure feeds into the si_layout variable
    which stores the frontend for Chicago choropleth map tab.
    Input: 
        si_slctd - value selected by user in the dropdown component
    '''

    fig = px.choropleth(map_df,
                    geojson=map_df.geometry,
                    locations=map_df.index,
                    color_continuous_scale = 'RdBu',
                    color=si_slvaluectd)
    fig.update_geos(fitbounds="locations", visible=False)  
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig