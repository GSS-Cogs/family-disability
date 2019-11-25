# # Needs a scraper!
#
# For now, am just loading from a local source.
#
# Note, the included file `indicators-CountyUApre419.data.csv` is the plain csv download from the provided url which I'm using for now.
#

# +
import os

from gssutils import *
import pandas as pd

#load data from local
df = pd.read_csv("indicators-CountyUApre419.data.csv")


# +
# Function we'll make use of

def timeify(cell):
    """ Simple function to style time to match our requirments """
    
    if len(cell) == 4:
        return "year/"+cell
    elif len(cell) == 7:
        return "government-year/{}-{}".format(cell[:4], "20"+cell[-2:])
    else:
        raise ValueError("Unexpected time format: '{}'. We are expecting time values "
                         "with a length of either 4 or 7 characters".format(cell))
        


# +

# Copy the columns we want over into our tidy_sheet
tidy_sheet = pd.DataFrame()
tidy_sheet["Indicator"] = df["Indicator Name"]
tidy_sheet["Area"] = df["Area Code"]
tidy_sheet["Sex"] = df["Sex"]
tidy_sheet["Age"] = df["Age"]
tidy_sheet["Time period"] = df["Time period"].apply(timeify)
tidy_sheet["Value"] = df["Value"]
tidy_sheet["Trend"] = df["Recent Trend"]

from pathlib import Path
out = Path('out')
out.mkdir(exist_ok=True)
tidy_sheet.to_csv(out / 'observations.csv', index = False)

