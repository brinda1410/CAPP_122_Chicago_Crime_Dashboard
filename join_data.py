'''
This module merge the csv files into one dataset with the chosen variables
aggregated at ward level.
'''

import pandas as pd

# Files directory
small_business = "data/SB.csv"
crimes = "data/Crimes.csv"
family_support = "data/FSA.csv"
microloans = "data/Microloans.csv"

sb_df = pd.read_csv(small_business)
crimes_df = pd.read_csv(crimes)
fs_df = pd.read_csv(family_support)
ml_df = pd.read_csv(microloans)

# Small Business DF
sb_df = sb_df[["INCENTIVE_AMOUNT", "WARD"]]
sb_df = sb_df.groupby("WARD").sum()
sb_df = sb_df.rename(columns={"INCENTIVE_AMOUNT": "SB FUNDS"})

# Family Support Agencies DF
fs_df = fs_df.dropna(subset=["WARD"])
fs_df["WARD"] = fs_df["WARD"].astype(int)
fs_df = fs_df.rename(columns={"AGENCY": "FS AGENCIES"})
fs_df = fs_df.groupby("WARD").count()
fs_df = fs_df[["FS AGENCIES"]]

# Micro Loans DF
ml_df = ml_df.dropna(subset=["WARD"])
ml_df["WARD"] = ml_df["WARD"].astype(int)
ml_df = ml_df.rename(columns={"LENDER": "MICRO LOANS"})
ml_df = ml_df.groupby("WARD").count()
ml_df = ml_df[["MICRO LOANS"]]

# Crimes
crimes_df = crimes_df.dropna(subset=["WARD"])
crimes_df["WARD"] = crimes_df["WARD"].astype(int)
crimes_df = crimes_df.rename(columns={"PRIMARY_TYPE": "TYPE OF CRIME"})
crimes_df = crimes_df.pivot_table(values="ID", index="WARD", columns="TYPE OF CRIME", aggfunc=pd.Series.nunique)

# Join
df = fs_df.join(sb_df)
df = df.join(ml_df)
df = df.join(crimes_df)

df.to_csv("data/merged_data.csv")