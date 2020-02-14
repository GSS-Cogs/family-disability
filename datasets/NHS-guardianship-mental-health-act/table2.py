# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
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


#Table 2: Cases of Guardianship under the Mental Health Act 1983 by gender, Section, and relationship of guardian, 2016-17 and 2017-18 England
tabs = {tab.name: tab for tab in scraper.distribution(latest=True, mediaType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet').as_databaker()}
tab = tabs['Table 2']

# +
status_type = ['NEW CASES DURING THE YEAR (1 April to 31 March)', 'CASES CONTINUING AT THE END OF THE YEAR' ] 
#Commented out from now 
#, 'CASES CLOSED DURING THE YEAR (1 April to 31 March)']
section_guardianship_type = ['By Application (Section 7)', 'Following conviction (Section 37)','Local Authority', 'Other Person', 'Total Number of Cases ']
gender_type = ['Male', 'Female', 'Total']

reference_tab = tab.filter('England total')
year = tab.excel_ref('E12').expand(RIGHT).is_not_blank()
gender = reference_tab.expand(RIGHT).one_of(gender_type)
status = reference_tab.expand(DOWN).one_of(status_type)
section_guardianship = reference_tab.expand(DOWN).one_of(section_guardianship_type)
totals = gender.fill(DOWN).is_not_blank() - section_guardianship.expand(RIGHT)
observations = gender.fill(DOWN).is_not_blank() - totals
#savepreviewhtml(observations)
# -

dimensions = [
    HDimConst('Measure Type', 'Count'),
    HDim(year, 'Period', CLOSEST, LEFT),
    HDim(status, 'Status', CLOSEST, ABOVE),
    HDim(gender, 'Sex', DIRECTLY, ABOVE),
    HDim(section_guardianship, 'Temp', DIRECTLY, LEFT)
]
#TODO, maybe extract totals and percentage the same way ? 
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c1, fname="Preview.html")
new_table = c1.topandas()

new_table

guardanship_values = ['      Local Authority', '      Other Person', 'No. of non-responding LAs']
section_values = ['By Application (Section 7)', 'Following conviction (Section 37)']
total_values =['Total Number of Cases ']
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
new_table['DATAMARKER'].replace('*', 'nhs-guardianship/less-than-three', inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)

new_table = new_table.replace({'Guardianship' : {
    '      Local Authority' : 'Local Authority',
    '      Other Person' : 'Other Person'}})
new_table['Guardianship'] = new_table['Guardianship'].fillna('all').map(lambda x: pathify(x))

new_table = new_table.replace({'Status' : {
    'NEW CASES DURING THE YEAR (1 April to 31 March)' : 'Cases opened in year',
    'CASES CONTINUING AT THE END OF THE YEAR' : 'Cases continuing at the end of the year',
    #'CASES CLOSED DURING THE YEAR (1 April to 31 March)' : 'Cases closed during year'
}})

new_table['Section'] = new_table['Section'].fillna('all').map(lambda x: pathify(x))

new_table['Status'] = new_table['Status'].map(lambda x: pathify(x))
new_table = new_table.replace({'Sex' : {'Male' : 'M',' Female' : 'F','Total' : 'T' }})

new_table['Period'] = new_table['Period'].map(lambda x: 'government-year/' + left(x,4) +'-20' + right(x,2))
new_table = new_table.fillna('not-applicable')
# -

new_table = new_table.rename(columns={'DATAMARKER':'Marker'})
new_table = new_table.replace({'Marker' : {'-' : 'not-applicable'}})
new_table = new_table.drop(['Temp'], axis=1)

tidy = new_table[['Period', 'Sex', 'Guardianship', 'Status', 'Section', 'Value', 'Measure Type', 'Marker']]
tidy

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Cases of Guardianship under the Mental Health Act 1983 by gender, Section, and relationship of guardian'
OBS_ID = pathify(TITLE)

tidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)

# +
from gssutils.metadata import THEME
from os import environ
scraper.set_dataset_id(f'{pathify(environ.get("JOB_NAME", ""))}/{OBS_ID}')
scraper.dataset.title = f'{TITLE}'
scraper.dataset.family = 'disability'

with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

schema = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')
