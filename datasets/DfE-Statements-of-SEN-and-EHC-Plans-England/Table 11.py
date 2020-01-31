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
scraper = Scraper('https://www.gov.uk/government/collections/statistics-special-educational-needs-sen')

scraper

scraper.select_dataset(title=lambda x: x.startswith('Statements of SEN and EHC Plans'), latest=True)

scraper

tabs = { tab.name: tab for tab in scraper.distributions[2].as_databaker() }

tab = tabs['Table 11']

# +
cell = tab.filter(contains_string('Table 11'))
cell.assert_one()
Year = tab.excel_ref('D6') | tab.excel_ref('H6')
plantype = Year.shift(0,1).expand(RIGHT).is_not_blank().is_not_whitespace()
age = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
observations = plantype.fill(DOWN).is_not_blank().is_not_whitespace() - tab.excel_ref('H26')
week = tab.filter(contains_string('38 to 51 weeks per year')) | tab.filter(contains_string('52 weeks per year'))
Dimensions = [
            HDimConst('Geography', 'all'),
            HDim(Year,'Year', CLOSEST,LEFT),
            HDim(week,'week', CLOSEST,ABOVE),
            HDim(age,'DfE Age Groups',DIRECTLY,LEFT),
            HDim(plantype,'Statements or EHC Plan Type',DIRECTLY, ABOVE),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDimConst('Statements of SEN or EHC Plan Description', 'Number of children and young people with statements or EHC plans placed in residential special schools or colleges by age')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
new_table['Year'] = 'Year/' + new_table['Year'].astype(str)
new_table['DfE Age Groups'] = new_table['DfE Age Groups'].map(
    lambda x: {
        'Total' : 'all ages'}.get(x, x))
new_table['Statements or EHC Plan Type'] = new_table['Statements or EHC Plan Type'].map(
    lambda x: {
        'Total' : 'all plans'}.get(x, x))
new_table['Statements or EHC Plan Type'] = new_table['Statements or EHC Plan Type'] + '-' + new_table['week']
new_table['Statements of SEN or EHC Plan Provider'] = 'all'
