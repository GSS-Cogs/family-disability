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


tabs = {tab.name: tab for tab in scraper.distribution(latest=True, mediaType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet').as_databaker()}
tab = tabs['Table 3']

#Table 3a: Cases of Guardianship under the Mental Health Act 1983 by local authority region, 2016-17
region = tab.excel_ref('B14').expand(DOWN).is_not_blank() - tab.excel_ref('B25').expand(DOWN).is_not_blank()
removePercentage1 = tab.excel_ref('E12')
removePercentage2 = tab.excel_ref('I12')
caseStstus = tab.excel_ref('B12').expand(RIGHT).is_not_blank() - tab.excel_ref('M12').expand(RIGHT)
caseStstus = caseStstus - removePercentage1 - removePercentage2
observations = caseStstus.fill(DOWN).is_not_blank()
dimensions = [
    HDimConst('Measure Type', 'Count'),
    HDimConst('Period', 'government-year/2016-2017'),
    HDimConst('Guardianship', 'Local Authority'),
    HDim(region, 'Region name', DIRECTLY, LEFT),
    HDim(caseStstus, 'Status', DIRECTLY, ABOVE) 
]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_16_17 = c1.topandas()

#Table 3b: Cases of Guardianship under the Mental Health Act 1983 by local authority region, 2017-18
region = tab.excel_ref('W14').expand(DOWN).is_not_blank() - tab.excel_ref('W25').expand(DOWN).is_not_blank()
removePercentage1 = tab.excel_ref('Z12')
removePercentage2 = tab.excel_ref('AD12')
caseStstus = tab.excel_ref('W12').expand(RIGHT).is_not_blank() - tab.excel_ref('AH12').expand(RIGHT)
caseStstus = caseStstus - removePercentage1 - removePercentage2
observations = caseStstus.fill(DOWN).is_not_blank()
dimensions = [
    HDimConst('Measure Type', 'Count'),
    HDimConst('Period', 'government-year/2017-2018'),
    HDimConst('Guardianship', 'Local Authority'),
    HDim(region, 'Region name', DIRECTLY, LEFT),
    HDim(caseStstus, 'Status', DIRECTLY, ABOVE) 
]
c2 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_17_18 = c2.topandas()

new_table = pd.concat([table_16_17, table_17_18])

# +
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Guardianship'] = new_table['Guardianship'].map(
    lambda x: pathify(x))
new_table['Region name'] = new_table['Region name'].map(
    lambda x: pathify(x))

new_table = new_table.replace({'Status' : {
    'Cases continuing at end of year' : 'Cases continuing at the end of the year',
    'Cases closed during year' : 'Cases closed during the year'
}})

new_table['Status'] = new_table['Status'].map(
    lambda x: pathify(x))
new_table = new_table.fillna('')

tidy = new_table[['Period', 'Guardianship', 'Region name', 'Status', 'Value', 'Measure Type']]
tidy

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Cases of Guardianship under the Mental Health Act 1983 by local authority region'
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
