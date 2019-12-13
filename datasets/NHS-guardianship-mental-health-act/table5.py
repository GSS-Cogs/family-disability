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


tabs = {tab.name: tab for tab in scraper.distribution(latest=True, mediaType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet').as_databaker()}

#Table 5a: Duration of closed cases of Guardianship under the Mental Health Act 1983 by local authority region, 2016-17
tab = tabs['Table 5']

#Number of cases by region - all cases - 2016-17
regionName = tab.excel_ref('B14').expand(DOWN).is_not_blank() - tab.excel_ref('B26').expand(DOWN) 
median = tab.excel_ref('M13').expand(DOWN).is_not_blank() - tab.excel_ref('M26').expand(DOWN) 
duration = tab.excel_ref('C13').expand(RIGHT).is_not_blank() - tab.excel_ref('M13').expand(RIGHT) 
observations_16_17_all = duration.fill(DOWN).is_not_blank() - tab.excel_ref('C26').expand(RIGHT).expand(DOWN)
#savepreviewhtml(observations)
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Section', 'all'),
    HDimConst('Period', 'government-year/2016-2017'),
    HDimConst('Status', 'cases-closed-during-year'),
    HDimConst('Guardianship', 'Local Authority'),
    HDim(duration, 'Duration of closed cases', DIRECTLY, ABOVE),
    HDim(regionName, 'Region name', DIRECTLY, LEFT),
    HDim(median, 'Median (months)', DIRECTLY, RIGHT),
]
c1 = ConversionSegment(observations_16_17_all, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c1, fname="Preview.html")
table_16_17_all = c1.topandas()

#Number of cases by region - all cases - 2017-18
regionName = tab.excel_ref('O14').expand(DOWN).is_not_blank() - tab.excel_ref('O26').expand(DOWN)
#totalCases = tab.excel_ref('P13').expand(DOWN).is_not_blank() - tab.excel_ref('P26').expand(DOWN) 
median = tab.excel_ref('Z13').expand(DOWN).is_not_blank() - tab.excel_ref('Z26').expand(DOWN) 
duration = tab.excel_ref('P13').expand(RIGHT).is_not_blank() - tab.excel_ref('Z13').expand(RIGHT) 
observations_17_18_all = duration.fill(DOWN).is_not_blank() - tab.excel_ref('P26').expand(RIGHT).expand(DOWN)
#savepreviewhtml(observations)
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Section', 'all'),
    HDimConst('Period', 'government-year/2017-2018'),
    HDimConst('Status', 'cases-closed-during-year'),
    HDimConst('Guardianship', 'Local Authority'),
    HDim(duration, 'Duration of closed cases', DIRECTLY, ABOVE),
    HDim(regionName, 'Region name', DIRECTLY, LEFT),
    #HDim(totalCases, 'Total Cases', DIRECTLY, LEFT),
    HDim(median, 'Median (months)', DIRECTLY, RIGHT),
]
c2 = ConversionSegment(observations_17_18_all, dimensions, processTIMEUNIT=True)
table_17_18_all = c2.topandas()

#Number of cases by region - Section 7 cases - 2016-17
tab = tabs['Table 5']
regionName = tab.excel_ref('B30').expand(DOWN).is_not_blank() - tab.excel_ref('B42').expand(DOWN)
#totalCases = tab.excel_ref('C29').expand(DOWN).is_not_blank() - tab.excel_ref('C42').expand(DOWN) 
median = tab.excel_ref('M29').expand(DOWN).is_not_blank() - tab.excel_ref('M42').expand(DOWN) 
duration = tab.excel_ref('C29').expand(RIGHT).is_not_blank() - tab.excel_ref('M29').expand(RIGHT) 
observations_16_17_section7 = duration.fill(DOWN).is_not_blank() - tab.excel_ref('C42').expand(RIGHT).expand(DOWN)
#savepreviewhtml(observations)
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Section', 'By Application (Section 7)'),
    HDimConst('Period', 'government-year/2016-2017'),
    HDimConst('Status', 'cases-closed-during-year'),
    HDimConst('Guardianship', 'Local Authority'),
    HDim(duration, 'Duration of closed cases', DIRECTLY, ABOVE),
    HDim(regionName, 'Region name', DIRECTLY, LEFT),
    #HDim(totalCases, 'Total Cases', DIRECTLY, LEFT),
    HDim(median, 'Median (months)', DIRECTLY, RIGHT),
]
c1 = ConversionSegment(observations_16_17_section7, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c1, fname="Preview.html")
table_16_17_section7 = c1.topandas()

#Number of cases by region - Section 7 cases - 2017-18
regionName = tab.excel_ref('O30').expand(DOWN).is_not_blank() - tab.excel_ref('O42').expand(DOWN)
#totalCases = tab.excel_ref('P29').expand(DOWN).is_not_blank() - tab.excel_ref('P42').expand(DOWN) 
median = tab.excel_ref('Z29').expand(DOWN).is_not_blank() - tab.excel_ref('Z42').expand(DOWN) 
duration = tab.excel_ref('P29').expand(RIGHT).is_not_blank() - tab.excel_ref('Z29').expand(RIGHT) 
observations_17_18_section7 = duration.fill(DOWN).is_not_blank() - tab.excel_ref('P42').expand(RIGHT).expand(DOWN)
#savepreviewhtml(observations)
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Section', 'By Application (Section 7)'),
    HDimConst('Period', 'government-year/2017-2018'),
    HDimConst('Status', 'cases-closed-during-year'),
    HDimConst('Guardianship', 'Local Authority'),
    HDim(duration, 'Duration of closed cases', DIRECTLY, ABOVE),
    HDim(regionName, 'Region name', DIRECTLY, LEFT),
    #HDim(totalCases, 'Total Cases', DIRECTLY, LEFT),
    HDim(median, 'Median (months)', DIRECTLY, RIGHT),
]
c2 = ConversionSegment(observations_17_18_section7, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c2, fname="Preview.html")
table_17_18_section7 = c2.topandas()

#Number of cases by region - Section 37 cases - 2016-17
regionName = tab.excel_ref('B46').expand(DOWN).is_not_blank() - tab.excel_ref('B58').expand(DOWN)
#totalCases = tab.excel_ref('C45').expand(DOWN).is_not_blank() - tab.excel_ref('C58').expand(DOWN) 
median = tab.excel_ref('M45').expand(DOWN).is_not_blank() - tab.excel_ref('M58').expand(DOWN) 
duration = tab.excel_ref('C45').expand(RIGHT).is_not_blank() - tab.excel_ref('M45').expand(RIGHT) 
observations_16_17_section37 = duration.fill(DOWN).is_not_blank() - tab.excel_ref('C58').expand(RIGHT).expand(DOWN)
#savepreviewhtml(observations)
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Period', 'government-year/2016-2017'),
    HDimConst('Status', 'cases-closed-during-year'),
    HDimConst('Section', 'following-conviction-section-37'),
    HDimConst('Guardianship', 'Local Authority'),
    HDim(duration, 'Duration of closed cases', DIRECTLY, ABOVE),
    HDim(regionName, 'Region name', DIRECTLY, LEFT),
    #HDim(totalCases, 'Total Cases', DIRECTLY, LEFT),
    HDim(median, 'Median (months)', DIRECTLY, RIGHT),
]
c1 = ConversionSegment(observations_16_17_section37, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c1, fname="Preview.html")
table_16_17_section37 = c1.topandas()

#Number of cases by region - Section 37 cases - 2016-17
regionName = tab.excel_ref('O46').expand(DOWN).is_not_blank() - tab.excel_ref('O58').expand(DOWN)
#totalCases = tab.excel_ref('P45').expand(DOWN).is_not_blank() - tab.excel_ref('P58').expand(DOWN) 
median = tab.excel_ref('Z45').expand(DOWN).is_not_blank() - tab.excel_ref('Z58').expand(DOWN) 
duration = tab.excel_ref('P45').expand(RIGHT).is_not_blank() - tab.excel_ref('Z45').expand(RIGHT) 
observations_17_18_section37 = duration.fill(DOWN).is_not_blank() - tab.excel_ref('P58').expand(RIGHT).expand(DOWN)
#savepreviewhtml(observations)
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Period', 'government-year/2016-2017'),
    HDimConst('Status', 'cases-closed-during-year'),
    HDimConst('Section', 'following-conviction-section-37'),
    HDimConst('Guardianship', 'Local Authority'),
    HDim(duration, 'Duration of closed cases', DIRECTLY, ABOVE),
    HDim(regionName, 'Region name', DIRECTLY, LEFT),
   # HDim(totalCases, 'Total Cases', DIRECTLY, LEFT),
    HDim(median, 'Median (months)', DIRECTLY, RIGHT),
]
c2 = ConversionSegment(observations_17_18_section37, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c2, fname="Preview.html")
table_17_18_section37 = c2.topandas()

new_table = pd.concat([table_16_17_all, table_17_18_all, table_16_17_section7, table_17_18_section7, 
                      table_16_17_section37, table_17_18_section37], sort=True)

#Tidy up
new_table['DATAMARKER'].replace('*', 'Below-3', inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Unit'] = new_table['Unit'].map(lambda x: pathify(x))
new_table['Guardianship'] = new_table['Guardianship'].map(lambda x: pathify(x))
new_table['Duration of closed cases'] = new_table['Duration of closed cases'].map(lambda x: pathify(x))
new_table['Region name'] = new_table['Region name'].map(lambda x: pathify(x))
new_table['Status'] = new_table['Status'].map(lambda x: pathify(x))
new_table['Section'] = new_table['Section'].map(lambda x: pathify(x))
new_table = new_table.fillna('')


new_table = new_table.rename(columns={'DATAMARKER':'Estimated values'})

tidy = new_table[['Period','Guardianship', 'Status','Region name', 'Section',
                  'Duration of closed cases','Value','Estimated values', 'Unit', 'Median (months)']]
tidy

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Duration of closed cases of Guardianship under the Mental Health Act 1983 by local authority region'
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
