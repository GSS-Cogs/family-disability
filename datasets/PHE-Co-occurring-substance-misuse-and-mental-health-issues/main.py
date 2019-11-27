# # Notes:
#
# * There's a question around release date (and a whole lot of other trig related data). So for now I'm hard coding
# observations.trig.
# * I've also hard coded schema.json as it's reliant on the trig.
#

# +
import fingertips_py as ftp
import pandas as pd
import requests
import dateutil.parser

# TODO - this is just hacky "pre scraper" code
# this'll eventually become the scraper once we've worked the kinks out of it.
def get_data(url):

    # get the profile_key out of the url
    group_key = url.split("/profile/")[1].split("/")[0]

    # get the area id out of  the url
    area_type_id = url.split("/ati/")[1].split("/")[0]

    # use the group_key (from the url) to get the profile
    profile = [x for x in ftp.get_all_profiles() if x["Key"] == group_key]

    # if we have more than one profile, raise an error. Otherwise use the one.
    if len(profile) > 1:
        raise ValueError("Aborting, the provided url is identifying more than one profile.")
    profile = profile[0]

    # create a dataframe containing all profile metadata
    metadata = ftp.get_metadata_for_profile_as_dataframe(profile["Id"])

    data = ftp.get_all_data_for_profile(str(profile['Id']), parent_area_type_id=area_type_id)
    
    # get "Unit" from the metadata about each indicator into a lookup dict
    # get "Standard Population" from the metadata about each indicator into a lookup dict
    unit_lookup = {}
    stat_pop_lookup = {}
    for indicator in metadata["Indicator ID"].unique():
        stat_pop_lookup[indicator] = metadata["Standard population/values"][metadata["Indicator ID"] == indicator].unique()[0]
        unit_lookup[indicator] = metadata["Unit"][metadata["Indicator ID"] == indicator].unique()[0]
        
    data["Unit"] = data["Indicator ID"].map(lambda x: unit_lookup[int(x)])
    data["Standard population/values"] = data["Indicator ID"].map(lambda x: stat_pop_lookup[int(x)])
    
    return data

# TODO - I'm using the full link to get the geography level automatically, but im ignoring the provided group id and just
# getting all groups.... that can't be right.
data = get_data("https://fingertips.phe.org.uk/profile-group/mental-health/profile/drugsandmentalhealth/data#page/0/gid/1938132935/pat/6/par/E12000006/ati/102/are/E06000055")


# +
# Functions we'll make use of

def timeify(cell):
    """ Simple function to style time to match our requirments """
    
    if len(cell) == 4:
        return "year/"+cell
    elif len(cell) == 7:
        return "government-year/{}-{}".format(cell[:4], "20"+cell[-2:])
    elif " - " in cell:
        return "gregorian-interval/{}/PY2".format(cell.split(" - ")[0])
    else:
        raise ValueError("Unexpected time format: '{}'. We are expecting time values "
                         "with a length of either 4 or 7 characters".format(cell))
        


# +

# Copy the columns we want over into our tidy_sheet
tidy_sheet = pd.DataFrame()
tidy_sheet["Indicator"] = data["Indicator Name"]
tidy_sheet["Area"] = data["Area Code"]
tidy_sheet["Sex"] = data["Sex"]
tidy_sheet["Age"] = data["Age"]
tidy_sheet["Time period"] = data["Time period"].astype(str).apply(timeify)
tidy_sheet["Value"] = data["Value"]
tidy_sheet["Trend"] = data["Recent Trend"]
tidy_sheet["Unit"] = data["Unit"]

from pathlib import Path
out = Path('out')
out.mkdir(exist_ok=True)
tidy_sheet.to_csv(out / 'observations.csv', index = False)

# +

# Generate some codelist info - keeping for now but usually flagged to off
# TODO, should maybe output directly to ../../reference/codelists rather than here

generate_codelist_csvs = False
if generate_codelist_csvs:

    def make_notation(value):
        """ Take the value of on cell of a 'Label' column and modify to be suitable for a notation column """

        value = value.lower()
        replacers = [
            ["<", "-less-than-"],
            [" ", "-"],
            ["%", ""],
            [",", ""],
            [":", ""],
            [")", ""],
            ["(", ""],
            [" ", "-"],
            ["--", "-"]
        ]
        
        for replacer in replacers:
            value = value.replace(replacer[0], replacer[1])
            
        # reformat if its greater than
        if "+" in value:
            value_split = value.split("+")[0].split("-")
            value = "-".join(value_split[:-1])+"-greater-than-"+value_split[-1]+value.split("+")[1]

        return value.rstrip("-").lstrip("-")


    for col in tidy_sheet.columns.values:

        if col in ["Indicator", "Trend", "Age"]:

            df = pd.DataFrame()
            df["Label"] = tidy_sheet[col]
            df["Notation"] = df["Label"].astype(str).apply(make_notation)
            df["Parent Notation"] = ""
            df["Sort Priority"] = ""

            df = df.drop_duplicates()
            df = df.dropna()

            if col == "Age":
                output = "phe-co-occurring-substance-misuse-and-mental-health-issues-age.csv"
            else:
                output = col.lower()+".csv"
                
            df.to_csv(output, index=False)
            
