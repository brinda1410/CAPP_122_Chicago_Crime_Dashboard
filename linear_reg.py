import numpy as np
import pandas as pd
import plotly.express as px
import geopandas as gpd
import pyproj

from maindash import app
from dash import html, dcc
from dash.dependencies import Input, Output

# Creates the Index:

df = pd.read_csv("data/merged_data.csv")
crimes = ['ARSON', 'ASSAULT', 'BATTERY', 'BURGLARY',\
          'CONCEALED CARRY LICENSE VIOLATION', 'CRIM SEXUAL ASSAULT',\
          'CRIMINAL DAMAGE', 'CRIMINAL SEXUAL ASSAULT', 'CRIMINAL TRESPASS',\
          'DECEPTIVE PRACTICE', 'GAMBLING', 'HOMICIDE', 'HUMAN TRAFFICKING',\
          'INTERFERENCE WITH PUBLIC OFFICER', 'INTIMIDATION', 'KIDNAPPING',\
          'LIQUOR LAW VIOLATION', 'MOTOR VEHICLE THEFT', 'NARCOTICS', 'NON-CRIMINAL',\
          'OBSCENITY', 'OFFENSE INVOLVING CHILDREN', 'OTHER NARCOTIC VIOLATION',\
          'OTHER OFFENSE', 'PROSTITUTION', 'PUBLIC INDECENCY', 'PUBLIC PEACE VIOLATION',\
          'RITUALISM', 'ROBBERY', 'SEX OFFENSE', 'STALKING', 'THEFT', 'WEAPONS VIOLATION']

df['ALL CRIMES'] = df[crimes].sum(axis=1)
y = df.loc[:, ['ALL CRIMES']].values
X = df[['FS AGENCIES', 'SB FUNDS', 'MICRO LOANS']].fillna(0)
X = np.concatenate((X, np.ones((X.shape[0])).reshape(-1, 1)), axis = 1)
betas = np.linalg.lstsq(X, y,rcond = None)[0]
error = y - np.matmul(X, betas)

if min(error) >= 0:
    error = error / max(error)
else:
    div = max(max(error), -min(error))
    error = error / div

df["INDEX_ANALYSIS"] = error.reshape(1, 50)[0]
va_int = ['WARD', 'INDEX_ANALYSIS','FS AGENCIES', 'SB FUNDS', 'MICRO LOANS','ALL CRIMES']
col_names = va_int[1:]
df = df[va_int]
df["WARD"] = df["WARD"].astype(str)

fp = "wards geofiles/WARDS_2015.shx"
map_df = gpd.read_file(fp)
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
map_df = map_df.merge(df, on = 'WARD')

#for i in col_names:
#    ax = map_df.plot(i, cmap='bwr',legend=True, figsize=(10, 15), legend_kwds={'label': i, 'orientation': "horizontal"})
#    ax.set_axis_off();

# ---------------------------- FRONT-END -------------------------------
# App layout for Social Investment tab
hm_layout = html.Div([
        html.H2("Chicago Heatmap", style = {'text-align': 'left'}),
        html.Br(),
        html.Label(['Select Variable:'], style={'font-weight': 'bold', "text-align": "left"}),
        html.Br(),
        dcc.Dropdown(id = "select_type",
                    options = [{"label": str(x), "value": x} for x in col_names], 
                    value = col_names[0],
                    multi = False,
                    style = {'width': "40%"}),
        #html.Div(id = 'output_container', children = []),
        dcc.Graph(id = 'map_by_ward', figure = {})
    ])

# --------------------------- BACKEND -----------------------------------  
# Connect the figure contained in Dash Core Components with the frontend

@app.callback(
    Output(component_id = 'map_by_ward', component_property = 'figure'),
    [Input(component_id = 'select_type', component_property = 'value')]
    )
def update_graph(si_slvaluectd):
    '''
    ''' 
    map_df.set_index('WARD')
    fig = px.choropleth(map_df,
                   geojson=map_df.geometry,
                   locations=map_df.index,
                   color=si_slvaluectd)
    fig.update_geos(fitbounds="locations", visible=False)  
    return fig