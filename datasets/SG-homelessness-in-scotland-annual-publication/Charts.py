#!/usr/bin/env python
# coding: utf-8
# %%
from gssutils import *
from databaker.framework import *

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

scraper = Scraper('https://www2.gov.scot/Topics/Statistics/Browse/Housing-Regeneration/RefTables/homelessness1819tablescharts')
scraper


# NB:- Scraper needed to be directed to specific 2018/19 page rather than the landing page
#   :- Also need to update the below to use a more standard pivot point ('cell') rather than the first entry in the column as this most likely won't be standard moving forward.

# %%
distCharts = scraper.distribution(title=lambda t: 'Charts' in t)
#distTables = scraper.distribution(title=lambda t: 'Tables' in t)

tabsCharts = {tab.name: tab for tab in distCharts.as_databaker()}


# %%
tab = tabsCharts['Data6']

cell = tab.filter('Refused')
reason = cell.shift(1,-1).expand(DOWN).is_not_whitespace().shift(LEFT).is_not_blank()
period = cell.shift(1,-1).expand(RIGHT).is_not_blank().is_not_whitespace()
observations = cell.shift(RIGHT).expand(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().is_number()

Dimensions = [
            HDim(reason,'Reasons for failing to maintain accommodation',DIRECTLY,LEFT),
            HDim(period,'Period',DIRECTLY,ABOVE),
            HDimConst('Measure Type','Count'),
            HDimConst('Unit','People')            
            ]
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
savepreviewhtml(c1)


# %%
new_table = c1.topandas()
import numpy as np
new_table['OBS'].replace('', np.nan, inplace=True)
new_table.dropna(subset=['OBS'], inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Period'] = new_table['Period'].map(
    lambda x: f'gregorian-interval/{right(x,4)}-03-31T00:00:00/P1Y')
new_table = new_table[['Period','Reasons for failing to maintain accommodation','Measure Type','Value','Unit']]
new_table['Reasons for failing to maintain accommodation'] = new_table.apply(lambda x: pathify(x['Reasons for failing to maintain accommodation']), axis = 1)
new_table['Reasons for failing to maintain accommodation'] = new_table.apply(lambda x: x['Reasons for failing to maintain accommodation'].replace('/', '-or'), axis = 1)
new_table = new_table.replace({'Reasons for failing to maintain accommodation' : {
    'not-to-do-with-applicant-household-e-g-landlord-selling-property-fire-circumstances-of-other-persons-sharing-previous-property-harassment-by-others-etc' : 'not-to-do-with-applicant-household', }})
new_table


# %%
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Homelessness in Scotland: Reason(s) for failing to maintain accommodation'
OBS_ID = pathify(TITLE.replace('(s)', ''))

new_table.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)


# %%
GROUP_ID = 'sg-homelessness-in-scotland-annual-publication'

from gssutils.metadata import THEME
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(f'disability/{GROUP_ID}/{OBS_ID}')
scraper.dataset.title = f'{TITLE}'

scraper.dataset.family = 'disability'
#scraper.dataset.theme = THEME['health-social-care']
with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -

schema = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')

new_table


# %%
tab = tabsCharts['Data9']

cell = tab.filter('Learning disability')
support = cell.shift(1,-1).expand(DOWN).is_not_whitespace().shift(LEFT).is_not_blank()
period = cell.shift(1,-1)
observations = cell.shift(RIGHT).expand(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().is_number()

Dimensions = [
            HDim(support,'Identified support needs of homeless households',DIRECTLY,LEFT),
            HDim(period,'Period',DIRECTLY,ABOVE),
            HDimConst('Measure Type','Count'),
            HDimConst('Unit','People')            
            ]
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
savepreviewhtml(c1)


# %%
new_table = c1.topandas()
import numpy as np
new_table['OBS'].replace('', np.nan, inplace=True)
new_table.dropna(subset=['OBS'], inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Period'] = new_table['Period'].map(
    lambda x: f'gregorian-interval/{left(x,2) + right(x,2)}-03-31T00:00:00/P1Y')
new_table = new_table[['Period','Identified support needs of homeless households','Measure Type','Value','Unit']]
new_table['Identified support needs of homeless households'] = new_table.apply(lambda x: pathify(x['Identified support needs of homeless households']), axis = 1)
new_table['Identified support needs of homeless households'] = new_table.apply(lambda x: x['Identified support needs of homeless households'].replace('/', 'or'), axis = 1)
new_table


# %%
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Homelessness in Scotland: Identified Support Needs of Homeless Households'
OBS_ID = pathify(TITLE.replace('(s)', ''))

new_table.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)


# %%
# +
from gssutils.metadata import THEME
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(f'disability/{GROUP_ID}/{OBS_ID}')
scraper.dataset.title = f'{TITLE}'
scraper.dataset.family = 'disability'

#scraper.dataset.theme = THEME['health-social-care']
with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -

schema = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')

new_table

