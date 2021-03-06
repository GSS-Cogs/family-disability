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


# %%
distTables = scraper.distribution(title=lambda t: 'Tables' in t)

tabsTables = {tab.name: tab for tab in distTables.as_databaker()}


# %%
tab = tabsTables['Table 9']

cell = tab.excel_ref('A5')
reason = cell.shift(RIGHT).expand(DOWN).is_not_whitespace().is_not_blank().shift(LEFT)
exclude = tab.excel_ref('A27').expand(DOWN).expand(RIGHT)
exclude2 = tab.excel_ref('N3').expand(RIGHT).expand(DOWN)
reason2 = reason - exclude
period = cell.shift(1,-2).expand(RIGHT).is_not_blank().is_not_whitespace() - exclude2
observations = cell.shift(RIGHT).expand(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().is_number() - exclude - exclude2

Dimensions = [
            HDim(reason2,'Reasons for homelessness application',DIRECTLY,LEFT),
            HDim(period,'Period',DIRECTLY,ABOVE),
            HDimConst('Measure Type','Count'),
            HDimConst('Unit','People')            
            ]
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
savepreviewhtml(c1)


# NB:- Find if there is a replacement for 'filter' which can find partial matches rather than full cell matches and replace cell_ref

# %%
new_table = c1.topandas()
import numpy as np
new_table['OBS'].replace('', np.nan, inplace=True)
new_table.dropna(subset=['OBS'], inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Period'] = new_table['Period'].map(
    lambda x: f'gregorian-interval/{left(x,2) + right(x,2)}-03-31T00:00:00/P1Y')
new_table = new_table[['Period','Reasons for homelessness application','Measure Type','Value','Unit']]
new_table['Reasons for homelessness application'] = new_table.apply(lambda x: pathify(x['Reasons for homelessness application']), axis = 1)
new_table['Reasons for homelessness application'] = new_table.apply(lambda x: x['Reasons for homelessness application'].replace('/', 'or'), axis = 1)
new_table


# %%
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Homelessness in Scotland: Applications: Main reason for making an application for homelenessness to a Local Authority'
OBS_ID = pathify(TITLE)
GROUP_ID = 'sg-homelessness-in-scotland-annual-publication'

new_table.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)
# +
from gssutils.metadata import THEME
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(f'gss_data/disability/{GROUP_ID}/{OBS_ID}')
scraper.dataset.title = TITLE

scraper.dataset.family = 'disability'
#scraper.dataset.theme = THEME['health-social-care']
with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -

schema = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')

new_table


# %%
tab = tabsTables['Table 10']

cell = tab.excel_ref('A5')
reason = cell.shift(RIGHT).expand(DOWN).is_not_whitespace().is_not_blank().shift(LEFT)
exclude = tab.excel_ref('A19').expand(DOWN).expand(RIGHT)
exclude2 = tab.excel_ref('N3').expand(RIGHT).expand(DOWN)
reason2 = reason - exclude
period = cell.shift(1,-2).expand(RIGHT).is_not_blank().is_not_whitespace() - exclude2
observations = cell.shift(RIGHT).expand(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().is_number() - exclude - exclude2

Dimensions = [
            HDim(reason2,'Reasons for failing to maintain accommodation',DIRECTLY,LEFT),
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
new_table = new_table[['Period','Reasons for failing to maintain accommodation','Measure Type','Value','Unit']]
new_table['Reasons for failing to maintain accommodation'] = new_table.apply(lambda x: pathify(x['Reasons for failing to maintain accommodation']), axis = 1)
new_table['Reasons for failing to maintain accommodation'] = new_table.apply(lambda x: x['Reasons for failing to maintain accommodation'].replace('/', '-or'), axis = 1)
new_table = new_table.replace({'Reasons for failing to maintain accommodation' : {
    'not-to-do-with-applicant-household-e-g-landlord-selling-property-fire-circumstances-of-other-persons-sharing-previous-property-harassment-by-others-etc' : 'not-to-do-with-applicant-household', }})                                                                             
new_table


# %%
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Homelessness in Scotland: Applications: Reasons for failing to maintain accommodation prior to application'
OBS_ID = pathify(TITLE)

new_table.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)
# +
from gssutils.metadata import THEME
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(f'gss_data/disability/{GROUP_ID}/{OBS_ID}')
scraper.dataset.title = TITLE

scraper.dataset.family = 'disability'
#scraper.dataset.theme = THEME['health-social-care']
with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -

schema = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')

new_table


# %%
tab = tabsTables['Table 15']

cell = tab.excel_ref('A4')
reason = cell.shift(RIGHT).expand(DOWN).is_not_whitespace().is_not_blank().shift(LEFT)
exclude = tab.excel_ref('A14').expand(DOWN).expand(RIGHT)
exclude2 = tab.excel_ref('N3').expand(RIGHT).expand(DOWN)
reason2 = reason - exclude
period = cell.shift(1,-1).expand(RIGHT).is_not_blank().is_not_whitespace() - exclude2
observations = cell.shift(RIGHT).expand(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().is_number() - exclude - exclude2

Dimensions = [
            HDim(reason2,'Identified support needs of homeless households',DIRECTLY,LEFT),
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
new_table['Identified support needs of homeless households'] = new_table.apply(lambda x: pathify(x['Identified support needs of homeless households'].replace('/', 'or')), axis = 1)
new_table


# %%
destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TITLE = 'Homelessness in Scotland: Applications: Support need identified for those homeless (or threatened with homelessness) households'
OBS_ID = pathify(TITLE)

new_table.drop_duplicates().to_csv(destinationFolder / f'{OBS_ID}.csv', index = False)
# +
from gssutils.metadata import THEME
scraper.set_base_uri('http://gss-data.org.uk')
scraper.set_dataset_id(f'gss_data/disability/{GROUP_ID}/'+ f'{OBS_ID}')
scraper.dataset.title = TITLE

scraper.dataset.family = 'disability'
scraper.dataset.theme = THEME['health-social-care']
with open(destinationFolder / f'{OBS_ID}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -

schema = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
schema.create(destinationFolder / f'{OBS_ID}.csv', destinationFolder / f'{OBS_ID}.csv-schema.json')

new_table

