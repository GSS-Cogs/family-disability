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
section_type = ['By application (Section 7)', 'Following conviction (Section 37)'] 
guardianship_type = ['Local Authority', 'Other person', 'No. of non-responding LAs']
status_type = ['NEW CASES DURING THE YEAR', 'CASES CONTINUING AT THE END OF THE YEAR', 'CASES CLOSED DURING THE YEAR']


year = tab.excel_ref('B12').expand(RIGHT).is_not_blank()
status = tab.excel_ref('B12').expand(DOWN).one_of(status_type)
section = tab.excel_ref('B12').expand(DOWN).one_of(section_type)
guardianship = tab.excel_ref('B12').expand(DOWN).one_of(guardianship_type)
percentage = tab.excel_ref('B42').expand(RIGHT)

observations = year.fill(DOWN).is_not_blank() - percentage
totals = year.fill(DOWN).is_not_blank() - section.expand(RIGHT) - guardianship.expand(RIGHT)
#savepreviewhtml(totals)


# +
#by status
dimensions = [
               HDim(year, 'Period', CLOSEST, LEFT), 
               HDim(status, 'Status', CLOSEST, ABOVE),
               HDimConst('Guardianship', 'all'),
               HDimConst('Section', 'all')
        ]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
status_table = c1.topandas()

#by section 
section_observations = year.fill(DOWN).is_not_blank() - totals - guardianship.expand(RIGHT)
dimensions = [
               HDim(year, 'Period', CLOSEST, LEFT), 
               HDim(section, 'Section', DIRECTLY, LEFT),
               HDimConst('Guardianship', 'all'),
               HDimConst('Status', 'all')
        ]
c2 = ConversionSegment(section_observations, dimensions, processTIMEUNIT=True)
section_table = c2.topandas()

#by guardianship
guardianship_observations = year.fill(DOWN).is_not_blank() - totals - section_observations
dimensions = [
               HDim(year, 'Period', CLOSEST, LEFT), 
               HDim(guardianship, 'Guardianship', DIRECTLY, LEFT),
               HDimConst('Section', 'all'),
               HDimConst('Status', 'all')
        ]
c3 = ConversionSegment(guardianship_observations, dimensions, processTIMEUNIT=True)
guardianship_table = c3.topandas()
# -

new_table = pd.concat([status_table, section_table, guardianship_table], sort=True)


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
    'CASES CONTINUING AT THE END OF THE YEAR' : 'Cases continuing at end of year',
    'CASES CLOSED DURING THE YEAR' : 'Cases closed during year'}})
new_table['Section'] = new_table['Section'].map(lambda x: pathify(x))

new_table['Status'] = new_table['Status'].map(lambda x: pathify(x))

new_table = new_table.replace({'Period' : {
    '2003-04*' : '2003-04', '2004-05*' : '2004-05', '2005-06*' : '2005-06', '2006-07*' : '2006-07',
    '2007-08*' : '2007-08', '2008-09*' : '2008-09', '2009-10*' : '2009-10', '2010-11*' : '2010-11', 
    '2011-12*' : '2011-12', '2012-13*' : '2012-13', '2013-14*' : '2013-14', '2014-15*' : '2014-15', 
    '2015-16*' : '2015-16'
    }})
new_table['Period'] = new_table['Period'].map(lambda x: 'government-year/' + left(x,4) +'-20' + right(x,2))

new_table = new_table.fillna('')
# -

new_table = new_table.rename(columns={'DATAMARKER':'Marker'})

tidy = new_table[['Period', 'Status', 'Guardianship','Section', 'Value', 'Marker']]
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
