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

tab = tabs['Table 1']

# +
cell = tab.filter(contains_string('Table 1'))
cell.assert_one()
Year = tab.excel_ref('D6').expand(RIGHT).is_not_blank().is_not_whitespace() 
plantype = Year.shift(0,1).expand(RIGHT).is_not_blank().is_not_whitespace()
age = tab.excel_ref('C10:C15')
observations = plantype.fill(DOWN).is_not_blank().is_not_whitespace() - tab.excel_ref('Z65')
description = tab.excel_ref('B9').expand(DOWN).is_not_blank().is_not_whitespace()
provider = tab.excel_ref('C18').expand(DOWN).is_not_blank().is_not_whitespace() | tab.excel_ref('B9')
Dimensions = [
            HDimConst('Geography', 'all'),
            HDim(Year,'Year', CLOSEST,LEFT),
            HDim(age,'DfE Age Groups',CLOSEST,ABOVE),
            HDim(plantype,'Statements or EHC Plan Type',DIRECTLY, ABOVE),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDim(description,'Statements of SEN or EHC Plan Description',CLOSEST,ABOVE),
            HDim(provider, 'Statements of SEN or EHC Plan Provider',CLOSEST,ABOVE)
    
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
new_table['Statements of SEN or EHC Plan Provider'] = new_table['Statements of SEN or EHC Plan Provider'].map(
    lambda x: {
        'Number of children and young people with statements or EHC plans4:' : 'all',
        ' LA maintained (including foundation schools)' : 'Main stream LA maintained schools',
        ' Academy' : 'Mainstream Academy',
         ' Free school' : 'Mainstream Free School',
         'LA maintained': 'LA maintained AP or PRU'}.get(x, x))
# -


