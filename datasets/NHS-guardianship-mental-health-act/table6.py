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
tab = tabs['Table 6']

# +
#Table 6a: Cases of guardianship under the Mental Health Act 1983 by region and local authority, 2016-17 (including duration of closed cases)
areaCode = tab.excel_ref('B13').expand(DOWN).is_not_blank() - tab.excel_ref('B178').expand(DOWN)
localAuthorityCode = tab.excel_ref('C13').expand(DOWN).is_not_blank()
localAuthorityName = tab.excel_ref('D13').expand(DOWN).is_not_blank()
regionName = tab.excel_ref('E13').expand(DOWN).is_not_blank()
caseStatus = tab.excel_ref('F12').expand(RIGHT).is_not_blank() - tab.excel_ref('H12').expand(RIGHT)
case_observations_16_17 = caseStatus.fill(DOWN).is_not_blank()
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Period', 'government-year/2016-2017'),
    HDimConst('Guardianship', 'Local Authority'),
    HDimConst('Measure Type', 'rounded-to-the-nearest-multiple-of-5'), 
    HDim(caseStatus, 'Status', DIRECTLY, ABOVE),
    HDimConst('Duration of closed cases', ' '),
    HDim(areaCode, 'ONS area code', DIRECTLY, LEFT),
    HDim(localAuthorityCode, 'Local authority code', DIRECTLY, LEFT),
    HDim(localAuthorityName, 'Local authority name', DIRECTLY, LEFT),
    HDim(regionName, 'Region name', DIRECTLY, LEFT),
]
c1 = ConversionSegment(case_observations_16_17, dimensions, processTIMEUNIT=True)
table_16_17_Status = c1.topandas()

duration = tab.excel_ref('I12').expand(RIGHT).is_not_blank() - tab.excel_ref('Q12').expand(RIGHT) 
duration_observations_16_17 = duration.fill(DOWN).is_not_blank()
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Period', 'government-year/2016-2017'),
    HDimConst('Guardianship', 'Local Authority'),
    HDimConst('Measure Type', 'rounded-to-the-nearest-multiple-of-5'),
    HDimConst('Status', 'Cases closed in  year'),
    HDim(duration, 'Duration of closed cases', DIRECTLY, ABOVE),
    HDim(areaCode, 'ONS area code', DIRECTLY, LEFT),
    HDim(localAuthorityCode, 'Local authority code', DIRECTLY, LEFT),
    HDim(localAuthorityName, 'Local authority name', DIRECTLY, LEFT),
    HDim(regionName, 'Region name', DIRECTLY, LEFT),
]
c2 = ConversionSegment(duration_observations_16_17, dimensions, processTIMEUNIT=True)
table_16_17_Duration = c2.topandas()

# +
#Table 6b: Cases of guardianship under the Mental Health Act 1983 by region and local authority, 2017-18 (including duration of closed cases)
areaCode = tab.excel_ref('R13').expand(DOWN).is_not_blank() - tab.excel_ref('R178').expand(DOWN)
localAuthorityCode = tab.excel_ref('S13').expand(DOWN).is_not_blank()
localAuthorityName = tab.excel_ref('T13').expand(DOWN).is_not_blank()
regionName = tab.excel_ref('U13').expand(DOWN).is_not_blank()
caseStatus = tab.excel_ref('V12').expand(RIGHT).is_not_blank() - tab.excel_ref('X12').expand(RIGHT)
case_observations_17_18 = caseStatus.fill(DOWN).is_not_blank()
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Period', 'government-year/2017-2018'),
    HDimConst('Guardianship', 'Local Authority'),
    HDimConst('Measure Type', 'rounded-to-the-nearest-multiple-of-5'),
    HDim(caseStatus, 'Status', DIRECTLY, ABOVE),
    HDimConst('Duration of closed cases', ' '),
    HDim(areaCode, 'ONS area code', DIRECTLY, LEFT),
    HDim(localAuthorityCode, 'Local authority code', DIRECTLY, LEFT),
    HDim(localAuthorityName, 'Local authority name', DIRECTLY, LEFT),
    HDim(regionName, 'Region name', DIRECTLY, LEFT),
]
c3 = ConversionSegment(case_observations_17_18, dimensions, processTIMEUNIT=True)
table_17_18_Status = c3.topandas()

duration = tab.excel_ref('Y12').expand(RIGHT).is_not_blank() 
duration_observations_17_18 = duration.fill(DOWN).is_not_blank()
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Period', 'government-year/2017-2018'),
    HDimConst('Measure Type', 'rounded-to-the-nearest-multiple-of-5'),
    HDimConst('Guardianship', 'Local Authority'),
    HDimConst('Status', 'Cases closed in  year'),
    HDim(duration, 'Duration of closed cases', DIRECTLY, ABOVE),
    HDim(areaCode, 'ONS area code', DIRECTLY, LEFT),
    HDim(localAuthorityCode, 'Local authority code', DIRECTLY, LEFT),
    HDim(localAuthorityName, 'Local authority name', DIRECTLY, LEFT),
    HDim(regionName, 'Region name', DIRECTLY, LEFT),
]
c4 = ConversionSegment(duration_observations_17_18, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c4, fname="Preview.html")
table_17_18_Duration = c4.topandas()
# -

new_table = pd.concat([table_16_17_Status, table_16_17_Duration, table_17_18_Status, table_17_18_Duration], sort=True)

#Tidy up
new_table['DATAMARKER'].replace('*', 'Below-3', inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Unit'] = new_table['Unit'].map(lambda x: pathify(x))
new_table['Guardianship'] = new_table['Guardianship'].map(lambda x: pathify(x))
new_table['Region name'] = new_table['Region name'].map(lambda x: pathify(x))
new_table['Status'] = new_table['Status'].map(lambda x: pathify(x))
new_table = new_table.replace({'Duration of closed cases' : {' ' : 'does-not-apply',}})
new_table = new_table.fillna('')
new_table


tidy = new_table[['Period','Guardianship', 'Status', 'Duration of closed cases', 
                  'ONS area code','Local authority code','Local authority name',
                  'Region name','Value','DATAMARKER', 'Unit', 'Measure Type']]
tidy

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Cases of guardianship under the Mental Health Act 1983 by region and local authority (including duration of closed cases)'

OBS_ID = pathify(TITLE)
GROUP_ID = 'NHS-guardianship-mental-health-act'

tidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)

