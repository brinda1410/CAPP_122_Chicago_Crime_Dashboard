import pandas as pd

#Files directory
small_business = "data\SB.csv"
crimes = "data\Crimes.csv"
family_support = "data\FSA.csv"
microloans = "data\Microloans.csv"

sb_df = pd.read_csv(small_business)
crimes_df = pd.read_csv(crimes)
fs_df = pd.read_csv(family_support)
ml_df = pd.read_csv(microloans)

# Small Business DF - Collapsing the counts and grouping them by WARD
sb_df = sb_df[["TOTAL PROJECT COST", "WARD"]]
sb_df = sb_df.groupby("WARD").sum()
sb_df = sb_df.rename(columns={"TOTAL PROJECT COST": "SB FUNDS"})

# Family Support Agencies DF - Fixing Ward variable and grouping the observations
fs_df = fs_df.dropna(subset=["Ward"])
fs_df["Ward"] = fs_df["Ward"].astype(int)
fs_df = fs_df.rename(columns={"Ward": "WARD", "Agency": "FS AGENCIES"})
fs_df = fs_df.groupby("WARD").count()
fs_df = fs_df[["FS AGENCIES"]]

# Micro Loans DF
ml_df = ml_df.dropna(subset=["Ward"])
ml_df["Ward"] = ml_df["Ward"].astype(int)
ml_df = ml_df.rename(columns={"Ward": "WARD", "Lender": "MICRO LOANS"})
ml_df = ml_df.groupby("WARD").count()
ml_df = ml_df[["MICRO LOANS"]]

#Crimes
crimes_df = crimes_df.dropna(subset=["Ward"])
crimes_df["Ward"] = crimes_df["Ward"].astype(int)
crimes_df = crimes_df.rename(columns={"Ward": "WARD", "Primary Type": "TYPE OF CRIME"})
crimes_df = crimes_df.pivot_table(values="ID", index="WARD", columns="TYPE OF CRIME", aggfunc=pd.Series.nunique)

# Join
df = fs_df.join(sb_df)
df = df.join(ml_df)
df = df.join(crimes_df)
