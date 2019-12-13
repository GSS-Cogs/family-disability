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
# Duration of continuing cases as at 31 March 2007-08 to 2017-18
tab = tabs['Table 4']

#Table 4a: Duration of continuing cases of guardianship under the Mental Health Act 1983 by region and local authority, 2007-08
areaCode = tab.excel_ref('B14').expand(DOWN).is_not_blank() - tab.excel_ref('B180').expand(DOWN)
localAuthorityCode = tab.excel_ref('C14').expand(DOWN).is_not_blank()
localAuthorityName = tab.excel_ref('D14').expand(DOWN).is_not_blank()
regionName = tab.excel_ref('E14').expand(DOWN).is_not_blank()
medianOfContinuingCases = tab.excel_ref('G14').expand(DOWN).is_not_blank()
observations_08_09 = tab.excel_ref('F14').expand(DOWN).is_not_blank()
#savepreviewhtml(observations)
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Period', 'government-year/2007-2008'),
    HDimConst('Guardianship', 'Local Authority'),
    HDimConst('Status', 'Cases continuing at end of year'),
    HDim(areaCode, 'ONS area code', DIRECTLY, LEFT),
    HDim(localAuthorityCode, 'Local authority code', DIRECTLY, LEFT),
    HDim(localAuthorityName, 'Local authority name', DIRECTLY, LEFT),
    HDim(regionName, 'Region name', DIRECTLY, LEFT),
    HDim(medianOfContinuingCases, 'Median Length Of Continuing Cases (months)', DIRECTLY, RIGHT)
]
c1 = ConversionSegment(observations_08_09, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c1, fname="Preview.html")
table_07_08 = c1.topandas()

#Table 4b: Duration of continuing cases of guardianship under the Mental Health Act 1983 by region and local authority, 2017-18
areaCode = tab.excel_ref('I14').expand(DOWN).is_not_blank() - tab.excel_ref('I180').expand(DOWN)
localAuthorityCode = tab.excel_ref('J14').expand(DOWN).is_not_blank()
localAuthorityName = tab.excel_ref('K14').expand(DOWN).is_not_blank()
regionName = tab.excel_ref('L14').expand(DOWN).is_not_blank()
medianOfContinuingCases = tab.excel_ref('N14').expand(DOWN).is_not_blank()
observations_17_18 = tab.excel_ref('M14').expand(DOWN).is_not_blank()
#savepreviewhtml(observations)
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Period', 'government-year/2017-2018'),
    HDimConst('Guardianship', 'Local Authority'),
    HDimConst('Status', 'Cases continuing at end of year'),
    HDim(areaCode, 'ONS area code', DIRECTLY, LEFT),
    HDim(localAuthorityCode, 'Local authority code', DIRECTLY, LEFT),
    HDim(localAuthorityName, 'Local authority name', DIRECTLY, LEFT),
    HDim(regionName, 'Region name', DIRECTLY, LEFT),
    HDim(medianOfContinuingCases, 'Median Length Of Continuing Cases (months)', DIRECTLY, RIGHT)
]
c2 = ConversionSegment(observations_17_18, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c2, fname="Preview.html")
table_17_18 = c2.topandas()

new_table = pd.concat([table_07_08, table_17_18]).fillna('')

#Tidy up
new_table['DATAMARKER'].replace('*', 'Below-3', inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Unit'] = new_table['Unit'].map(
    lambda x: pathify(x))
new_table['Guardianship'] = new_table['Guardianship'].map(
    lambda x: pathify(x))
new_table['Region name'] = new_table['Region name'].map(
    lambda x: pathify(x))
new_table['Status'] = new_table['Status'].map(
    lambda x: pathify(x))
#new_table
tidy = new_table[['Period','Guardianship', 'Status','ONS area code','Local authority code','Local authority name'
                  ,'Region name','Value','DATAMARKER', 'Unit', 'Median Length Of Continuing Cases (months)']]
tidy

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Duration of continuing cases of guardianship under the Mental Health Act 1983 by region and local authority 2007-08 to 2017-18'
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
