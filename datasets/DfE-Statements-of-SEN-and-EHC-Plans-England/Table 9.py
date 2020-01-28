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

tab = tabs['Table 9']

cell = tab.filter('LA code')
cell.assert_one()
geo = cell.fill(DOWN).is_not_blank().is_not_whitespace()
Year = cell.shift(0,2).fill(RIGHT).is_not_blank().is_not_whitespace()
plantype = cell.fill(RIGHT).is_not_blank().is_not_whitespace() 
per = tab.filter(contains_string('Percentage'))
observations = geo.shift(2,0).fill(RIGHT).is_not_blank().is_not_whitespace() - per.fill(DOWN)
Dimensions = [
            HDim(geo,'Geography',DIRECTLY,LEFT),
            HDim(Year,'Year', DIRECTLY, ABOVE),
            HDim(plantype,'Statements or EHC Plan Type',CLOSEST,LEFT),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDimConst('Statements of SEN or EHC Plan Description', \
                      'New EHC plans issued within 20 weeks by local authority')
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'NHS Marker'}, inplace=True)
new_table['Year'] = 'Year/' + new_table['Year'].astype(str).str[-6:]
new_table['Statements or EHC Plan Type'] = new_table['Statements or EHC Plan Type'].str.lower()
new_table['Statements or EHC Plan Type'] = new_table['Statements or EHC Plan Type'].str.rstrip('3:')
new_table['Statements or EHC Plan Type'] = 'Number of new EHC plans issued ' + new_table['Statements or EHC Plan Type']
new_table['DfE Age Groups'] = 'all ages'
