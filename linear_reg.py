import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #if using matplotlib
import plotly.express as px #if using plotly
import geopandas as gpd

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

df['y'] = df[crimes].sum(axis=1)
y = df.loc[:, ['y']].values
X = df[['FS AGENCIES', 'SB FUNDS', 'MICRO LOANS']].fillna(0)
X = np.concatenate((X, np.ones((X.shape[0])).reshape(-1, 1)), axis = 1)
betas = np.linalg.lstsq(X, y,rcond = None)[0]
error = y - np.matmul(X, betas)

if min(error) >= 0:
    error = error / max(error)
else:
    div = max(max(error), -min(error))
    error = error / div

df["index"] = error.reshape(1, 50)[0]
df = df[['WARD', 'index']]
df["WARD"] = df["WARD"].astype(str)

fp = "wards geofiles/WARDS_2015.shx"
map_df = gpd.read_file(fp)
map_df = map_df.merge(df, on = 'WARD')
map_df.plot('index', cmap='bwr',legend=True)