# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from gssutils import *
import json
import pandas as pd
import numpy as np
info = json.load(open('info.json'))
scraper = Scraper(info['landingPage'])
scraper.select_dataset(latest=True)


#Table 1: Cases of Guardianship under the Mental Health Act 1983 by year, Section and relationship of guardian, 2003-04 to 2017-18 England
tabs = {tab.name: tab for tab in scraper.distribution(latest=True, mediaType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet').as_databaker()}
tab = tabs['Table 1']

# +
status_type = ['NEW CASES DURING THE YEAR', 'CASES CONTINUING AT THE END OF THE YEAR', 'CASES CLOSED DURING THE YEAR']
section_guardianship_type = ['By application (Section 7)', 'Following conviction (Section 37)',
                             'Local Authority', 'Other person', 'No. of non-responding LAs']

year = tab.excel_ref('B12').expand(RIGHT).is_not_blank()
section_guardianship = tab.excel_ref('B12').expand(DOWN).one_of(section_guardianship_type)
status = tab.excel_ref('B12').expand(DOWN).one_of(status_type)
percentage = tab.excel_ref('B42').expand(RIGHT)
totals = year.fill(DOWN).is_not_blank() - section_guardianship.expand(RIGHT)

observations = year.fill(DOWN).is_not_blank() - percentage - totals
#savepreviewhtml(observations)
# -

dimensions = [
    HDimConst('Measure Type', 'Count'),
    HDim(year, 'Period', CLOSEST, LEFT),
    HDim(status, 'Status', CLOSEST, ABOVE),
    HDim(section_guardianship, 'Temp', DIRECTLY, LEFT)
]
#TODO, maybe extract totals and percentage the same way ? 
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c1, fname="Preview.html")
new_table = c1.topandas()

guardanship_values = ['Local Authority', '       Other person', 'No. of non-responding LAs']
section_values = ['By application (Section 7)', 'Following conviction (Section 37)']
def guardianship_or_all(cell_value):
    if cell_value in guardanship_values:
        return cell_value
    else:
        return "all"
def section_or_all(cell_value):
    if cell_value in section_values:
        return cell_value
    else:
        return "all"
new_table["Guardianship"] = new_table["Temp"].apply(guardianship_or_all)
new_table["Section"] = new_table["Temp"].apply(section_or_all)
new_table


# +
def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]


# +
new_table['DATAMARKER'].replace('*', 'less-than-three', inplace=True)

new_table.rename(columns={'OBS': 'Value'}, inplace=True)

new_table = new_table.replace({'Guardianship' : {
    '       Local Authority' : 'Local Authority',
    '       Other person' : 'Other Person'}})
new_table['Guardianship'] = new_table['Guardianship'].map(lambda x: pathify(x))

new_table = new_table.replace({'Status' : {
    'NEW CASES DURING THE YEAR' : 'Cases opened in year',
    'CASES CONTINUING AT THE END OF THE YEAR' : 'Cases continuing at the end of the year',
    'CASES CLOSED DURING THE YEAR' : 'Cases closed during the year'}})
new_table['Section'] = new_table['Section'].map(lambda x: pathify(x))

new_table['Status'] = new_table['Status'].map(lambda x: pathify(x))

new_table = new_table.replace({'Period' : {
    '2003-04*' : '2003-04', '2004-05*' : '2004-05', '2005-06*' : '2005-06', '2006-07*' : '2006-07',
    '2007-08*' : '2007-08', '2008-09*' : '2008-09', '2009-10*' : '2009-10', '2010-11*' : '2010-11', 
    '2011-12*' : '2011-12', '2012-13*' : '2012-13', '2013-14*' : '2013-14', '2014-15*' : '2014-15', 
    '2015-16*' : '2015-16'
    }})
new_table['Period'] = new_table['Period'].map(lambda x: 'government-year/' + left(x,4) +'-20' + right(x,2))
new_table = new_table.fillna('not-applicable')
# -

new_table = new_table.rename(columns={'DATAMARKER':'Marker'})
new_table = new_table.replace({'Marker' : {'-' : 'not-applicable'}})
new_table = new_table.drop(['Temp'], axis=1)

tidy = new_table[['Period', 'Status', 'Guardianship','Section', 'Value', 'Measure Type', 'Marker']]
tidy

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Cases of Guardianship under the Mental Health Act 1983 by year, Section and relationship of guardian, 2003-04 to 2017-18'
OBS_ID = pathify(TITLE)
GROUP_ID = 'NHS-guardianship-mental-health-act'

tidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)

# +
from gssutils.metadata import THEME
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(f'gss_data/disability/{GROUP_ID}/{OBS_ID}')
scraper.dataset.title = f'{TITLE}'
scraper.dataset.family = 'disability'

with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

schema = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')
