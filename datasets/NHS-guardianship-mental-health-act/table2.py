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


#Table 2: Cases of Guardianship under the Mental Health Act 1983 by gender, Section, and relationship of guardian, 2016-17 and 2017-18 England
tabs = {tab.name: tab for tab in scraper.distribution(latest=True, mediaType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet').as_databaker()}
tab = tabs['Table 2']

# +
gender_type = ['Male', 'Female', 'Total']
section_type = ['By Application (Section 7)', 'Following conviction (Section 37)'] 
guardianship_type = ['Local Authority', 'Other Person']
status_type = ['NEW CASES DURING THE YEAR (1 April to 31 March)', 'CASES CONTINUING AT THE END OF THE YEAR', 'CASES CLOSED DURING THE YEAR (1 April to 31 March)']

reference_tab = tab.filter('England total')
year = tab.excel_ref('E12').expand(RIGHT).is_not_blank()
gender = reference_tab.expand(RIGHT).one_of(gender_type)
status = reference_tab.expand(DOWN).one_of(status_type)

section = reference_tab.expand(DOWN).one_of(section_type)
guardianship = reference_tab.expand(DOWN).one_of(guardianship_type)

observations = gender.fill(DOWN).is_not_blank() - section.expand(RIGHT) - guardianship.expand(RIGHT)
#savepreviewhtml(status)


# +
#by status
dimensions = [
               HDim(year, 'Period', CLOSEST, LEFT), 
               HDimConst('Period Duration', '1 April to 31 March'),
               HDim(gender, 'Sex', DIRECTLY, ABOVE),
               HDim(status, 'Status', CLOSEST, ABOVE),  
        ]
c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
status_table = c1.topandas()

#by section 
totals = gender.fill(DOWN).is_not_blank() - section.expand(RIGHT) - guardianship.expand(RIGHT)
section_observations = gender.fill(DOWN).is_not_blank() - totals - guardianship.expand(RIGHT)
dimensions = [
               HDim(year, 'Period', CLOSEST, LEFT), 
               HDimConst('Period Duration', '1 April to 31 March'),
               HDim(gender, 'Sex', DIRECTLY, ABOVE),
               HDim(section, 'Section', DIRECTLY, LEFT)
        ]
c2 = ConversionSegment(section_observations, dimensions, processTIMEUNIT=True)
section_table = c2.topandas()

#by guardianship
guardianship_observations = gender.fill(DOWN).is_not_blank() - totals - section_observations
dimensions = [
               HDim(year, 'Period', CLOSEST, LEFT), 
               HDimConst('Period Duration', '1 April to 31 March'),
               HDim(gender, 'Sex', DIRECTLY, ABOVE),
               HDim(guardianship, 'Guardianship', DIRECTLY, LEFT)
        ]
c3 = ConversionSegment(guardianship_observations, dimensions, processTIMEUNIT=True)
guardianship_table = c3.topandas()
# -

new_table = pd.concat([status_table, section_table, guardianship_table], sort=True)

# +
new_table['DATAMARKER'].replace('*', 'Below-3', inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Period Duration'] = new_table['Period Duration'].map(lambda x: pathify(x))

new_table = new_table.replace({'Guardianship' : {
    '      Local Authority' : 'Local Authority',
    '      Other Person' : 'Other Person'}})
new_table['Guardianship'] = new_table['Guardianship'].fillna('all').map(lambda x: pathify(x))

new_table = new_table.replace({'Status' : {
    'NEW CASES DURING THE YEAR (1 April to 31 March)' : 'New Cases',
    'CASES CONTINUING AT THE END OF THE YEAR' : 'Continuing Cases',
    'CASES CLOSED DURING THE YEAR (1 April to 31 March)' : 'Closed Cases'}})
new_table['Section'] = new_table['Section'].fillna('all').map(lambda x: pathify(x))

new_table['Status'] = new_table['Status'].fillna('all').map(lambda x: pathify(x))
new_table = new_table.replace({'Sex' : {'Male' : 'M',' Female' : 'F','Total' : 'T' }})
new_table = new_table.fillna('')

# -

tidy = new_table[['Period', 'Period Duration', 'Sex', 'Status', 'Guardianship','Section', 'Value', 'DATAMARKER']]
tidy

# +
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Cases of Guardianship under the Mental Health Act 1983 by gender, Section, and relationship of guardian'
OBS_ID = pathify(TITLE)
GROUP_ID = 'NHS-guardianship-mental-health-act'

tidy.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)