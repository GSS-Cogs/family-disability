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

tab = tabs['Table 10']

plantype = tab.excel_ref('B6:N9').is_not_blank().is_not_whitespace()

# +
cell = tab.filter('LA code')
cell.assert_one()
geo = cell.fill(DOWN).is_not_blank().is_not_whitespace()
Year = tab.filter(contains_string('Year'))
plantype = tab.excel_ref('B6:N9').is_not_blank().is_not_whitespace() 
observations = geo.shift(2,0).fill(RIGHT).is_not_blank().is_not_whitespace() \
                        - tab.excel_ref('O11').expand(DOWN).expand(RIGHT)
Dimensions = [
            HDim(geo,'Geography',DIRECTLY,LEFT),
            HDim(Year,'Year', CLOSEST, ABOVE),
            HDim(plantype,'Statements or EHC Plan Type',DIRECTLY,ABOVE),
            HDimConst('Unit','children'),  
            HDimConst('Measure Type','Count'),
            HDimConst('Statements of SEN or EHC Plan Description', \
                      'EHC plans with personal budgets, mediation and tribunal cases by local authority')
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'NHS Marker'}, inplace=True)
new_table['Year'] = 'Year/' + new_table['Year'].astype(str).str[-5:]
def user_perc(x):    
    if ((str(x) ==  'Education') | (str(x) ==  'Social care') | (str(x) ==  'Health ')) :
        return 'Number of personal budgets taken up for EHC plans issued or reviewed with direct payments for '+ x
    elif str(x) == 'Number' :
        return 'Mediation cases held which were followed by appeals to tribunal'
    else:
        return x        
    
new_table['Statements or EHC Plan Type'] = new_table.apply(lambda row: user_perc(row['Statements or EHC Plan Type']), axis = 1)
new_table['DfE Age Groups'] = 'all ages'
new_table['Statements of SEN or EHC Plan Provider'] = 'all'
# -


