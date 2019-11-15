# # Needs a scraper!
#
# For now, am just loading from a local source.
#
# Note, the included file `indicators-CountyUApre419.data.csv` is the plain csv download from the provided url which I'm using for now.
#

# # NOTES
#
# What Ive done and why for the next person.
#
# * Have serious concerns about the actual worth of the dataset, have raised it.
# * I've also dropped the category dimension, it's entirely blank, there was no point keeping it.
# * Alex has mentioned the data might be availible on gov.uk (which we DO have a scraper for), had a quick look and couldnt see it. Was a _very_ quick look though.
# * A (hopefully) usable `observations.csv` will be ouput into /out
# * Had a stab at codelists for this data by creating `../reference/columns.csv`. Have tried to use existing codelists where possible, curious
# if they'll work.
# * Have created two supprting codelists in `../reference/codelists`
# * Have created `../reference/codelist-metadata.json` which _I think_ ties it all together.
# * Basically, I was working towards creating valid reference data, from there we can work towards createing a valid schema (probably manually to start) and check that everything lints correctly (it won't, but if we can get that far it's just a case of working through issues).
#
# ### Needs investigating:
#
# In columns.csv I've made reference to eg `http://gss-data.org.uk/def/dimension/indicator/{indicator}` I don't know if this is generated
# by the reference repo from the codelist I added or if other steps are required.
#
# I'm also not sure what the part of `components.csv` is, but there's usually one of them.
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

# output observations to ./out
# TODO - should probably be consistent with the other recipes
out_dir = os.getcwd()+"/out"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
tidy_sheet.to_csv(out_dir+"/observations.csv")
# -

# # Generating Codelists
#
# The following cell is what I used to generated the codelists. Have left it in for now as I imagine they'll need tweaking.
#
# Have put it in a contitional statement so they wont run by accident.
#

# +

generate_codelist_csvs = False

if generate_codelist_csvs:

    def make_notation(value):
        """ Take the value of on cell of a 'Label' column and modify to be suitable for a notation column """
        
        # lower case and change spaces to -
        value = value.replace(" ", "-").lower()
        
        # remove commas and special symbols
        for txt in ["%", ",", ":", ")", "("]:
            value = value.replace(txt, "")
            
        # hacky repair where we've ended up with -- or --- between word
        value = value.replace("---", "-")
        value = value.replace("--", "-")
        
        return value
        

    for col in tidy_sheet.columns.values:

        if col in ["Indicator", "Trend"]:

            df = pd.DataFrame()
            df["Label"] = tidy_sheet[col]
            df["Notation"] = df["Label"].apply(make_notation)
            df["Parent Notation"] = ""
            df["Sort Priority"] = ""

            df = df.drop_duplicates()

            df.to_csv(col.lower()+".csv", index=False)
    
# -


