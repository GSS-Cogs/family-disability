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
tab = tabs['Table 3']

#Table 3a: Cases of Guardianship under the Mental Health Act 1983 by local authority region, 2016-17
region = tab.excel_ref('B14').expand(DOWN).is_not_blank() - tab.excel_ref('B25').expand(DOWN).is_not_blank()
removePercentage1 = tab.excel_ref('E12')
removePercentage2 = tab.excel_ref('I12')
caseStstus = tab.excel_ref('B12').expand(RIGHT).is_not_blank() - tab.excel_ref('M12').expand(RIGHT)
caseStstus = caseStstus - removePercentage1 - removePercentage2
observations = caseStstus.fill(DOWN).is_not_blank()
dimensions = [
    HDimConst('Period', 'government-year/2016-2017'),
    HDimConst('Guardianship', 'Local Authority'),
    HDimConst('Period Duration', '1 April to 31 March'),
    HDim(region, 'Region', DIRECTLY, LEFT),
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
    HDimConst('Period', 'government-year/2017-2018'),
    HDimConst('Guardianship', 'Local Authority'),
    HDimConst('Period Duration', '1 April to 31 March'),
    HDim(region, 'Region', DIRECTLY, LEFT),
    HDim(caseStstus, 'Status', DIRECTLY, ABOVE) 
]
c2 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
table_17_18 = c2.topandas()

new_table = pd.concat([table_16_17, table_17_18])

# +
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Guardianship'] = new_table['Guardianship'].map(
    lambda x: pathify(x))
new_table['Region'] = new_table['Region'].map(
    lambda x: pathify(x))
new_table['Case Status'] = new_table['Status'].map(
    lambda x: pathify(x))
new_table

tidy = new_table[['Period', 'Period Duration', 'Guardianship', 'Region', 'Case Status', 'Value']]
tidy

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Cases of Guardianship under the Mental Health Act 1983 by local authority region'
OBS_ID = pathify(TITLE)
GROUP_ID = 'NHS-guardianship-mental-health-act'

tidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)
