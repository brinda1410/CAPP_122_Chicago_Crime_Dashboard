'''
This module downloads the datasets from the Chicago Data Portal through an API.
'''

import sodapy
from sodapy import Socrata
import csv
import pandas as pd

data_identifiers = {"Crimes": ("qzdf-xmn8", "id, primary_type, arrest, domestic, beat, ward"),
                    "SB": ("etqr-sz5x", "project_name, ward, incentive_amount,"\
                            "total_project_cost, jobs_created_aspirational, jobs_retained_aspirational"),
                    "Microloans": ("dpkg-upyz", "loan_date, lender, city, state, ward, industry"),
                    "FSA": ("jmw7-ijg5", "agency, program_model, city, state, ward")}  

client = Socrata("data.cityofchicago.org", "zHR9MYQ5MjXuTZZ19OL8PYuVT")
client = Socrata("data.cityofchicago.org", "zHR9MYQ5MjXuTZZ19OL8PYuVT")

for key, tup in data_identifiers.items():
    identifier, columns = tup
    results = client.get(identifier, select = columns, limit = 250000)
    file_namename = "data/" + key + ".csv"
    df = pd.DataFrame(results)
    df.columns = df.columns.str.upper()
    df.to_csv(file_namename, index = False)
