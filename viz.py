import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Hard-coded filename
fsa_filename = "data/FSA.csv"
crimes_filename = "data/Crimes.csv"
mloans_filename = "data/Microloans.csv"
sb_filename = "data/SB.csv"

def read_data(file1, file2, file3, file4):

    # Read csv
    fsa = pd.read_csv(file1)
    crimes = pd.read_csv(file2)
    mloans = pd.read_csv(file3)
    sb = pd.read_csv(file4)

    return (fsa, crimes, mloans, sb)

def scatter_plt(file1, file2, file3, file4):
    fsa, crimes, mloans, sb = read_data(fsa_filename, crimes_filename, mloans_filename, sb_filename)
    # Default theme for seaborn
    sns.set_style()
    # Scatterplot
    x_axis = "INCENTIVE AMOUNT"
    y_axis = "TOTAL PROJECT COST"
    axes = sns.scatterplot(x = sb[x_axis], y = sb[y_axis])
    title =  x_axis + " BY " + y_axis
    axes.set_title(title)
    axes.set_ylabel(y_axis)
    axes.set_xlabel(x_axis)
   
    return plt.show()