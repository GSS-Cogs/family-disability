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
#Number of cases by region - all cases
tab = tabs['Table 5']
regionName = tab.excel_ref('B14').expand(DOWN).is_not_blank() - tab.excel_ref('B26').expand(DOWN)
totalCases = tab.excel_ref('C13').expand(DOWN).is_not_blank() - tab.excel_ref('C26').expand(DOWN) 
median = tab.excel_ref('M13').expand(DOWN).is_not_blank() - tab.excel_ref('M26').expand(DOWN) 
duration = tab.excel_ref('E13').expand(RIGHT).is_not_blank() - tab.excel_ref('M13').expand(RIGHT) 
observations_16_17 = duration.fill(DOWN).is_not_blank() - tab.excel_ref('E26').expand(RIGHT).expand(DOWN)
#savepreviewhtml(observations)
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Period', '2016-2017'),
    HDimConst('Status', 'closed cases'),
    HDimConst('Guardianship', 'Local Authority'),
    HDim(duration, 'Duration', DIRECTLY, ABOVE),
    HDim(regionName, 'Region Name', DIRECTLY, LEFT),
    HDim(totalCases, 'Total Cases', DIRECTLY, LEFT),
    HDim(median, 'Median1 Length Of Cases Closed (months)', DIRECTLY, RIGHT),
]
c1 = ConversionSegment(observations_16_17, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c1, fname="Preview.html")
table_16_17 = c1.topandas()

#Table 5b: Duration of closed cases of Guardianship under the Mental Health Act 1983 by local authority region, 2017-18
Number of cases by region - all cases
regionName = tab.excel_ref('O14').expand(DOWN).is_not_blank() - tab.excel_ref('O26').expand(DOWN)
totalCases = tab.excel_ref('P13').expand(DOWN).is_not_blank() - tab.excel_ref('P26').expand(DOWN) 
median = tab.excel_ref('Z13').expand(DOWN).is_not_blank() - tab.excel_ref('Z26').expand(DOWN) 
duration = tab.excel_ref('R13').expand(RIGHT).is_not_blank() - tab.excel_ref('Z13').expand(RIGHT) 
observations_17_18 = duration.fill(DOWN).is_not_blank() - tab.excel_ref('R26').expand(RIGHT).expand(DOWN)
#savepreviewhtml(observations)
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Period', '2017-2018'),
    HDimConst('Status', 'closed cases'),
    HDimConst('Guardianship', 'Local Authority'),
    HDim(duration, 'Duration', DIRECTLY, ABOVE),
    HDim(regionName, 'Region Name', DIRECTLY, LEFT),
    HDim(totalCases, 'Total Cases', DIRECTLY, LEFT),
    HDim(median, 'Median1 Length Of Cases Closed (months)', DIRECTLY, RIGHT),
]
c2 = ConversionSegment(observations_17_18, dimensions, processTIMEUNIT=True)
table_17_18 = c2.topandas()

new_table = pd.concat([table_16_17, table_17_18])

#Tidy up
new_table['DATAMARKER'].replace('*', 'Below-3', inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Unit'] = new_table['Unit'].map(
    lambda x: pathify(x))
new_table['Guardianship'] = new_table['Guardianship'].map(
    lambda x: pathify(x))
new_table['Duration'] = new_table['Duration'].map(
    lambda x: pathify(x))
new_table['Region Name'] = new_table['Region Name'].map(
    lambda x: pathify(x))
new_table['Status'] = new_table['Status'].map(
    lambda x: pathify(x))
#new_table
tidy = new_table[['Period','Guardianship', 'Status','Region Name', 'Duration', 
                  'Value','DATAMARKER', 'Unit', 'Total Cases', 'Median1 Length Of Cases Closed (months)']]
tidy



