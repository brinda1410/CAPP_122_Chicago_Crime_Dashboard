import requests
import json
import pandas as pd

URL_dic = {"crimes": "https://data.cityofchicago.org/resource/qzdf-xmn8.json",\
    "family_support": "https://data.cityofchicago.org/resource/jmw7-ijg5.json",\
    "small_business": "https://data.cityofchicago.org/resource/etqr-sz5x.json",\
    "microloans": "https://data.cityofchicago.org/resource/dpkg-upyz.json"}


def get_pandas_df(URL_dic):
    
    df_lst = []
    for url in URL_dic.values():
        response = requests.get(url)
        text_data = json.dumps(response.json())
        pandas_df = pd.read_json(text_data)
        df_lst.append(pandas_df)
    
    return tuple(df_lst)