# # Get the data
#
# Pull all the relevant data from fingertips. This is slow and can probably be improved.

# +
import fingertips_py as ftp
import pandas as pd
import requests
import dateutil.parser
from pathlib import Path

def get_data_by_domain(url):
    
    # get the profile_key out of the url
    group_key = url.split("/profile/")[1].split("/")[0]

    # get the area id out of  the url
    area_type_id = url.split("/ati/")[1].split("/")[0]

    # use the group_key (from the url) to get the profile
    profile = [x for x in ftp.get_all_profiles() if x["Key"] == group_key]
    
    # For each domain within this profile
    all_indicator_dataframes = []
    for i, domain in enumerate(profile[0]["GroupIds"]):
        
        # Get the indicator metadata for the domain
        r = requests.get("https://fingertips.phe.org.uk/api/indicator_metadata/by_group_id?group_ids=" + str(domain))
        if r.status_code != 200:
            raise ValueError("Aborting, unable to acquire domain metadata for domain:" + str(domain))
        
        indicator_metadata = r.json()
        
        # Get all the indicator data for this domain
        indicators = list(indicator_metadata.keys())
        indicator_data = ftp.get_data_by_indicator_ids(indicators, area_type_id)

        # get domain name as a string
        r2 = requests.get("https://fingertips.phe.org.uk/api/group_metadata?group_ids=" + str(domain))
        if r2.status_code != 200:
            raise ValueError("Aborting. Cant get domain level data for: " + str(domain))
        domain_name = r2.json()[0]["Name"]
        
        # attach the domain name to the indicator data
        indicator_data["Domain"] = domain_name
        all_indicator_dataframes.append(indicator_data)
            
    # create a dataframe containing all profile level metadata
    metadata = ftp.get_metadata_for_profile_as_dataframe(profile[0]["Id"])
    metadata.to_csv("metadata_for_profile.csv", index=False)
    
    data = pd.concat(all_indicator_dataframes)
    unit_lookup = {}
    stat_pop_lookup = {}
    for indicator in metadata["Indicator ID"].unique():
        stat_pop_lookup[indicator] = metadata["Standard population/values"][metadata["Indicator ID"] == indicator].unique()[0]
        unit_lookup[indicator] = metadata["Unit"][metadata["Indicator ID"] == indicator].unique()[0]
        
    data["Unit"] = data["Indicator ID"].map(lambda x: unit_lookup[int(x)])
    data["Standard population/values"] = data["Indicator ID"].map(lambda x: stat_pop_lookup[int(x)])
            
    data.to_csv("all_data.csv", index=False)
    
get_data_by_domain("https://fingertips.phe.org.uk/profile-group/mental-health/profile/drugsandmentalhealth/data#page/0/gid/1938132935/pat/6/par/E12000006/ati/102/are/E06000055")

# -


# # Functions
#
# Some functions we'll reuse a few times

# +
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
        
def pathify_label(value):
    """ As it says, change into something we can use for an output file name """
    
    unwanted = [")", "(", ",", ".", "/", "&"]
    for u in unwanted:
        value = value.lower().replace(u, "").replace(" ", "-").replace("---", "-").replace("--", "-")
    return value

def make_notation(value):
        """ Take the value of on cell of a 'Label' column and modify to be suitable for a notation column """

        value = value.lower()
        replacers = [
            ["<", "-less-than-"],
            [" ", "-"],
            ["%", "percentage"],
            [",", ""],
            [":", ""],
            [")", ""],
            ["(", ""],
            ["/", ""],
            [".", ""],
            ["--", "-"]
        ]
        
        for replacer in replacers:
            value = value.replace(replacer[0], replacer[1])
            
        # reformat if its greater than
        if "+" in value:
            value_split = value.split("+")[0].split("-")
            value = "-".join(value_split[:-1])+"-greater-than-"+value_split[-1]+value.split("+")[1]

        return value.rstrip("-").lstrip("-")
    


# -

# # Clean the data
#
# We're keeping the data within a single dataframe while we clean up the entires (it's simpler this way)

# +

all_data = pd.read_csv("all_data.csv")

# Dimensions that we want
# Copy the columns we want over into our tidy_sheet
tidy_sheet = pd.DataFrame()
tidy_sheet["Indicator"] = all_data["Indicator Name"]
tidy_sheet["Area"] = all_data["Area Code"]
tidy_sheet["Sex"] = all_data["Sex"]
tidy_sheet["Age"] = all_data["Age"]
tidy_sheet["Period"] = all_data["Time period"].astype(str).apply(timeify)
tidy_sheet["Value"] = all_data["Value"]
tidy_sheet["Trend"] = all_data["Recent Trend"]
tidy_sheet["Unit"] = all_data["Unit"]
tidy_sheet["Category Type"] = all_data["Category Type"]
tidy_sheet["Category"] = all_data["Category"]
tidy_sheet["Standard Population"] = all_data["Standard population/values"]

# Remove blank Value Rows
tidy_sheet = tidy_sheet[tidy_sheet["Value"].astype(str) != "nan"]

tidy_sheet.to_csv("all_but_tidied.csv", index=False)
# -
# # Split the data
#
# Now the data is ready, we're going to split it up along category lines.

# +

for cat in tidy_sheet["Category Type"].unique():
    
    temp_sheet = tidy_sheet[tidy_sheet["Category Type"].astype(str) == cat]
    
    if str(cat) == "nan":
        temp_sheet = temp_sheet.drop("Category", axis=1)
        cat = "Uncategorised"
    else:
        temp_sheet = temp_sheet.rename({'Category': cat}, axis=1)
        
    cat = pathify_label(cat)
    
    out = Path('out')
    out.mkdir(exist_ok=True)
    tidy_sheet.to_csv(out / "obs_{}.csv".format(cat), index = False)

# -
# # Generate Codelists
#
# We'll need codelists for of the above codes.
#
# Note - we're not generating codleists for area or period as they'll alreadye exist.
#
# **IMPORTANT** We're derriving codelists from the combined file (all_data.csv) with the exception of Categories which will change per putputted datacube. 

# +

# TODO - always switch me off before you push
GENERATE_REFERENCE_DATA = True

if GENERATE_REFERENCE_DATA:
    
    # ---------------------------
    # First the generic codelists
    generic_codelists_required = ["Indicator", "Sex", "Trend", "Unit", "Standard Population"]

    # Generic codelists
    for col in [x for x in tidy_sheet.columns.values if x in generic_codelists_required]:

        df = pd.DataFrame()
        df["Label"] = tidy_sheet[col]
        df = df.drop_duplicates()
        df = df[df["Label"].astype(str) != "nan"]

        df["Notation"] = df["Label"].astype(str).apply(make_notation)
        df["Parent Notation"] = ""
        df["Sort Priority"] = ""

        df.to_csv("PHE-{}.csv".format(pathify_label(col)), index=False)
        
    # ---------------------------
    # Then the category codelists
    
    for cat in tidy_sheet["Category Type"].unique():
        
        if str(cat) == "nan":
            continue
            
        df = pd.DataFrame()
        df["Label"] = tidy_sheet["Category"][tidy_sheet["Category Type"] == cat]
        
        df = df.drop_duplicates()
        df = df[df["Label"].astype(str) != "nan"]

        df["Notation"] = df["Label"].astype(str).apply(make_notation)
        df["Parent Notation"] = ""
        df["Sort Priority"] = ""

        df.to_csv("PHE-{}.csv".format(pathify_label(cat)), index=False)
        
    # --------------------------
    # Generate entries for columns.csv
    # For this one we'll just print to jupyter so it can be copy-pasted in
    
        
