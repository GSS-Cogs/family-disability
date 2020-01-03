# # Scrape
#
# Using a temporary scraper for now, the existing one might be ok but its set to a different path. Needs investigating.
#
# I'd rather have used the csv zips than the excels but they don't have the a plain english description of the indicator.
# I figured it's better to use the excels than have a hard-coded or external lookup to translate codes.
#

# +
from gssutils import *
from gssutils.metadata import *
import calendar

# TODO - this may well work but is being rejected for wrong path, investigate
#scrape = Scraper("https://digital.nhs.uk/data-and-information/publications/clinical-indicators/ccg-outcomes-indicator-set/current#related-links")
#scrape

def temp_scrape(scraper, tree):
    scraper.dataset.title = 'CCG Outcomes Indicator Set: December 2019'
    dist = Distribution(scraper)
    dist.title = 'A distribution'
    dist.downloadURL = "https://files.digital.nhs.uk/A2/563648/CCG_OIS_DEC_2019_Excel_Files.zip"
    dist.mediaType = ZIP
    scraper.distributions.append(dist)
    scraper.dataset.family = 'disability'
    return

scrapers.scraper_list = [('https://digital.nhs.uk/data-and-information/publications/', temp_scrape)]
scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/clinical-indicators/ccg-outcomes-indicator-set')
scraper
# -

# # Extraction
#
# There's some differences in formatting of headers between sheets (i.e "My header" vs "My Header"), to get around this I've used an add both them assert one pattern a lot. Example:
#
# ```
# data = tab.filter("Foo") | tab.filter("foo")    # gets us either or both cell values
# data.assert_one().do_whatever()                 # guarantees we've only got the one
# ```
#
# there might already be a "one of" matcher in hamcrest, if not, we should make one.

# +

from zipfile import ZipFile
from io import BytesIO
import requests

# Get the zip file at the given url
zipdata = BytesIO()
r = requests.get(scraper.distributions[0].downloadURL, stream=True)
zipdata.write(r.content)
myzipfile = ZipFile(zipdata)

# Dump the lot to disk
myzipfile.extractall()

# For each extracted file
df_list = []
for file_name in myzipfile.namelist():
    
    print(file_name)
    tabs = loadxlstabs(file_name)
    
    # --- IMPORTANT: SAFETY CATCH ---
    # Hard coded for december, so blow up if its not (as the metadata will not match)
    title_tabs = [x for x in tabs if x.name in ["Title sheet", "Title Sheet"]]
    if len(title_tabs) != 1:
        raise ValueError("Aborting, spreadsheet should have exactly 1 title tab.")
        
    # Hard code for december, so check the simpler formatted sheets (have "Data" tab)
    # and blow up if its not the expected December date (as the metadata will not match)
    release_date_cell = title_tabs[0].excel_ref("B12")
    if len([x for x in tabs if x.name == "Data"]) > 0  and release_date_cell.value != "December 2019":
        raise ValueError("Aborting. Data has changed since this hard coded pipeline last ran")
        
    # if we've no errors by here, we're good to continue
    # -------------------------------
    
    # We want a tab called either Data or 'Table 1', blow up if not
    wanted_tabs = [x for x in tabs if x.name in ["Data", "Table 1"]]
    if len(wanted_tabs) != 1:
        raise ValueError("Aborting. Sheet '{}' should have a tab named either 'Data' or 'Table 1' "
                         " but has: ".format(file_name) + ",".join([x.name for x in tabs]))
        
    # All good, use the data tab from here
    tab = wanted_tabs[0]

    # Find the header row
    # both cases to counteract inconsistency....
    header_row = tab.excel_ref("A").filter("Reporting Period") | tab.excel_ref("A").filter("Reporting period")
    header_row = header_row.assert_one().expand(RIGHT)
    
    if len(header_row) == 0:
        raise ValueError("Unable to find header row for '{}', aborting operation.".format(file_name))
    
    # Dimension: Reporting Period
    reporting_period = header_row.filter(contains_string("Reporting")).assert_one().fill(DOWN)
    
    # Dimension: Breakdown
    breakdown = header_row.filter("Breakdown").assert_one().fill(DOWN)
    
    # Dimension: Area
    area = header_row.filter("ONSCode") | header_row.filter("ONS code")
    area = area.assert_one().fill(DOWN)
        
    # Dimension: Level
    level = header_row.filter("Level").assert_one().fill(DOWN)
    
    # Dimensions from spreadsheet meta headings
    indicator = tab.excel_ref("A").filter(contains_string("CCG OIS Indicator")).value
    if not indicator.startswith("CCG OIS Indicator"):
        raise ValueError("Indicator does not appear to be in cell A11 for spreadsheet: " + file_name)
    indicator = indicator.split("-")[1].strip()
    
    # Get the obs
    observations = header_row.filter("Indicator value") | header_row.filter("Indicator Value")
    observations = observations.assert_one().fill(DOWN)
    
    # Where there are sub-levels for "Mental health care super cluster" (eg CCG_3.17_I01986_D)
    # only take the N/A and Total observations
    # TODO - this is brittle, add some assertions etc
    mhsc_header = header_row.filter("Mental health care super cluster")
    if len(mhsc_header) > 0:
        mhsc = header_row.filter("Mental health care super cluster").fill(DOWN).filter("N/A")
        mhsc = mhsc | header_row.filter("Mental health care super cluster").fill(DOWN).filter("Total")
        observations = observations = mhsc.shift(RIGHT)
    
    # Make dimensions
    dimensions = [
        HDim(reporting_period, "Reporting Period", DIRECTLY, LEFT),
        HDim(breakdown, "Breakdown", DIRECTLY, LEFT),
        HDim(area, "Area", DIRECTLY, LEFT),
        HDim(level, "Level", DIRECTLY, LEFT),
        HDimConst("Indicator", indicator)
    ]
    
    cs = ConversionSegment(tab, dimensions, observations) # < --- processing
    
    p = cs.topandas()
    
    df_list.append(p)

# -
# We'll join them up here and print a quick preview of what we're looking at.

tidy_data = pd.concat(df_list)
tidy_data[:5] # 5 line preview


# +

# Switch to True to remake reference data files in this directory
make_reference = False

if make_reference:
    
    for col in ["Breakdown", "Indicator", "Level"]:
        
        df = pd.DataFrame()
        df["Label"] = tidy_data[col]
        df["Notation"] = df["Label"].apply(pathify)
        df["Parent Notation"] = ""
        df["Sort Priority"] = ""
        df = df.drop_duplicates()
        df.to_csv("nhs-" + pathify(col), index=False)

# -

# # Post processing
#
# So now we just tidy up and finalise the flattened and joined data

# +

def timeify(cell):
    """Helper function to create the desired time format"""
    
    # Because I'm nice :)
    if cell.startswith("gregorian-interval"):
        raise ValueError("You've already run this function against the column, re running it will" 
                         " throw errors. You need to start your rerun from the previous code cell.")
        
    # Scenario 1:
    # Split by 3 hyphens, its a 3 year period
    # example: april-2016-march-2019
    elif len(cell.split("-")) >= 3:
        month_abreviated = cell.split("-")[0][:3].title() # first three characters of start month
        month_number = str(list(calendar.month_abbr).index(month_abreviated))

        # bulk our single digit months with a prefixed 0
        month_number = "0" + month_number if len(month_number) < 2 else month_number

        # the years is always at the start
        year = cell.split("-")[1]

        return "gregorian-interval/{}-{}-01T00:00:00/PY3".format(year, month_number)
    
    # Scenario 2:
    # Single month of a single year
    # example: june-2019
    elif len(cell.split("-")) == 2:
        splitted = cell.split("-")
        return "month/{}-{}".format(splitted[1], splitted[0])
    
    # Scenario 3:
    # Financial year
    # example: 2018/19
    elif len(cell.split("/")) == 2:
        splitted = cell.split("/")
        return "government-year/{}-{}".format(splitted[0], splitted[0][:2]+splitted[1])
    else:
        raise ValueError("Cannot identify time type for: " + cell)
    
# Rename columns
tidy_data = tidy_data.rename(columns={
    "OBS":"Value", 
    "DATAMARKER":"Markers",
    "Indicator": "CCG Indicator",
    "Level": "NHS Level"
})

# Clear out the nans
tidy_data["Value"].fillna("", inplace=True)
tidy_data["Markers"].fillna("", inplace=True)
tidy_data["Markers"] = tidy_data["Markers"].map(lambda x: x.replace("*", "suppressed"))

# Pathify all the things
for column in ["Reporting Period", "Breakdown", "NHS Level", "CCG Indicator"]:
    tidy_data[column] = tidy_data[column].apply(pathify)

# Correct formatting for time
tidy_data["Reporting Period"] = tidy_data["Reporting Period"].apply(timeify)

tidy_data["Markers"].unique()
# + {}

# Output observations file
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True)
tidy_data.to_csv("out/observations.csv", index=False)

# Trig and metadata
with open(destinationFolder / f'observations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
    
csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
csvw.create(destinationFolder / 'observations.csv', destinationFolder / 'observations.csv-schema.json')

