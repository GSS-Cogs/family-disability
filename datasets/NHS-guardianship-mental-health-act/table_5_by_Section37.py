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

#Number of cases by region - Section 37 cases
tab = tabs['Table 5']
regionName = tab.excel_ref('B46').expand(DOWN).is_not_blank() - tab.excel_ref('B58').expand(DOWN)
totalCases = tab.excel_ref('C45').expand(DOWN).is_not_blank() - tab.excel_ref('C58').expand(DOWN) 
median = tab.excel_ref('M45').expand(DOWN).is_not_blank() - tab.excel_ref('M58').expand(DOWN) 
duration = tab.excel_ref('E45').expand(RIGHT).is_not_blank() - tab.excel_ref('M45').expand(RIGHT) 
observations_16_17 = duration.fill(DOWN).is_not_blank() - tab.excel_ref('E58').expand(RIGHT).expand(DOWN)
#savepreviewhtml(observations)
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Period', '2016-2017'),
    HDimConst('Status', 'closed cases'),
    HDimConst('Section', 'Section 37'),
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
regionName = tab.excel_ref('O46').expand(DOWN).is_not_blank() - tab.excel_ref('O58').expand(DOWN)
totalCases = tab.excel_ref('P45').expand(DOWN).is_not_blank() - tab.excel_ref('P58').expand(DOWN) 
median = tab.excel_ref('Z45').expand(DOWN).is_not_blank() - tab.excel_ref('Z58').expand(DOWN) 
duration = tab.excel_ref('R45').expand(RIGHT).is_not_blank() - tab.excel_ref('Z45').expand(RIGHT) 
observations_17_18 = duration.fill(DOWN).is_not_blank() - tab.excel_ref('R58').expand(RIGHT).expand(DOWN)
#savepreviewhtml(observations)
dimensions = [
    HDimConst('Unit', 'Number of Cases'),
    HDimConst('Period', '2017-2018'),
    HDimConst('Status', 'closed cases'),
    HDimConst('Section', 'Section 7'),
    HDimConst('Guardianship', 'Local Authority'),
    HDim(duration, 'Duration', DIRECTLY, ABOVE),
    HDim(regionName, 'Region Name', DIRECTLY, LEFT),
    HDim(totalCases, 'Total Cases', DIRECTLY, LEFT),
    HDim(median, 'Median1 Length Of Cases Closed (months)', DIRECTLY, RIGHT),
]
c2 = ConversionSegment(observations_17_18, dimensions, processTIMEUNIT=True)
#savepreviewhtml(c2, fname="Preview.html")
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
new_table['Section'] = new_table['Section'].map(
    lambda x: pathify(x))
#new_table
tidy = new_table[['Period','Guardianship', 'Status','Section','Region Name', 'Duration', 
                  'Value','DATAMARKER', 'Unit', 'Total Cases', 'Median1 Length Of Cases Closed (months)']]
tidy



