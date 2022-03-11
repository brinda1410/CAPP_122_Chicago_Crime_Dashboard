'''
This module runs the lineal regression, computes the index and build the heatmap layout. 
'''

import numpy as np
import pandas as pd
import plotly.express as px
import geopandas as gpd
import pyproj
from maindash import app
from dash import html, dcc
from dash.dependencies import Input, Output

# Reads the file:
df = pd.read_csv("data/merged_data.csv")
crimes = ['ARSON', 'ASSAULT', 'BATTERY', 'BURGLARY',
          'CONCEALED CARRY LICENSE VIOLATION', 'CRIM SEXUAL ASSAULT',
          'CRIMINAL DAMAGE', 'CRIMINAL SEXUAL ASSAULT', 'CRIMINAL TRESPASS',
          'DECEPTIVE PRACTICE', 'GAMBLING', 'HOMICIDE', 'HUMAN TRAFFICKING',
          'INTERFERENCE WITH PUBLIC OFFICER', 'INTIMIDATION', 'KIDNAPPING',
          'LIQUOR LAW VIOLATION', 'MOTOR VEHICLE THEFT', 'NARCOTICS', 'NON-CRIMINAL',
          'OBSCENITY', 'OFFENSE INVOLVING CHILDREN', 'OTHER NARCOTIC VIOLATION',
          'OTHER OFFENSE', 'PROSTITUTION', 'PUBLIC INDECENCY', 'PUBLIC PEACE VIOLATION',
          'RITUALISM', 'ROBBERY', 'SEX OFFENSE', 'STALKING', 'THEFT', 'WEAPONS VIOLATION']

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
fp = "wards geofiles/WARDS_2015.shx"
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
        dcc.Graph(id = 'map_by_ward', figure = {})
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
