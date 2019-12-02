#!/usr/bin/env python
# coding: utf-8

# In[34]:


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


# In[35]:


distTables = scraper.distribution(title=lambda t: 'Tables' in t)

tabsTables = {tab.name: tab for tab in distTables.as_databaker()}


# In[36]:


tab = tabsTables['Table 9']

cell = tab.excel_ref('A5')
reason = cell.shift(RIGHT).expand(DOWN).is_not_whitespace().is_not_blank().shift(LEFT)
exclude = tab.excel_ref('A27').expand(DOWN).expand(RIGHT)
exclude2 = tab.excel_ref('N3').expand(RIGHT).expand(DOWN)
reason2 = reason - exclude
period = cell.shift(1,-2).expand(RIGHT).is_not_blank().is_not_whitespace() - exclude2
observations = cell.shift(RIGHT).expand(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().is_number() - exclude - exclude2

Dimensions = [
            HDim(reason2,'Reason(s) for homelessness application',DIRECTLY,LEFT),
            HDim(period,'Period',DIRECTLY,ABOVE),
            HDimConst('Measure Type','Count'),
            HDimConst('Unit','People')            
            ]
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
savepreviewhtml(c1, fname="Preview.html")


# NB:- Find if there is a replacement for 'filter' which can find partial matches rather than full cell matches and replace cell_ref

# In[37]:


new_table = c1.topandas()
import numpy as np
new_table['OBS'].replace('', np.nan, inplace=True)
new_table.dropna(subset=['OBS'], inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Period'] = new_table['Period'].map(
    lambda x: f'gregorian-interval/{left(x,2) + right(x,2)}-03-31T00:00:00/P1Y')
new_table = new_table[['Period','Reason(s) for homelessness application','Measure Type','Value','Unit']]
new_table['Reason(s) for homelessness application'] = new_table.apply(lambda x: pathify(x['Reason(s) for homelessness application']), axis = 1)
new_table


# In[38]:


destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TAB_NAME = 'Reason(s)-for-homelessness-application'

new_table.drop_duplicates().to_csv(destinationFolder / f'{TAB_NAME}.csv', index = False)
# +
from gssutils.metadata import THEME

scraper.dataset.family = 'health'
scraper.dataset.theme = THEME['health-social-care']
with open(destinationFolder / f'{TAB_NAME}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -

schema = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
schema.create(destinationFolder / f'{TAB_NAME}.csv', destinationFolder / f'{TAB_NAME}.csv-schema.json')

new_table


# In[39]:


tab = tabsTables['Table 10']

cell = tab.excel_ref('A5')
reason = cell.shift(RIGHT).expand(DOWN).is_not_whitespace().is_not_blank().shift(LEFT)
exclude = tab.excel_ref('A19').expand(DOWN).expand(RIGHT)
exclude2 = tab.excel_ref('N3').expand(RIGHT).expand(DOWN)
reason2 = reason - exclude
period = cell.shift(1,-2).expand(RIGHT).is_not_blank().is_not_whitespace() - exclude2
observations = cell.shift(RIGHT).expand(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().is_number() - exclude - exclude2

Dimensions = [
            HDim(reason2,'Reason(s) for failing to maintain accommodation',DIRECTLY,LEFT),
            HDim(period,'Period',DIRECTLY,ABOVE),
            HDimConst('Measure Type','Count'),
            HDimConst('Unit','People')            
            ]
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
savepreviewhtml(c1, fname="Preview.html")


# In[40]:


new_table = c1.topandas()
import numpy as np
new_table['OBS'].replace('', np.nan, inplace=True)
new_table.dropna(subset=['OBS'], inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Period'] = new_table['Period'].map(
    lambda x: f'gregorian-interval/{left(x,2) + right(x,2)}-03-31T00:00:00/P1Y')
new_table = new_table[['Period','Reason(s) for failing to maintain accommodation','Measure Type','Value','Unit']]
new_table['Reason(s) for failing to maintain accommodation'] = new_table.apply(lambda x: pathify(x['Reason(s) for failing to maintain accommodation']), axis = 1)
new_table


# In[41]:


destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TAB_NAME = 'Reasons-for-failing-to-maintain-accommodation-prior-to-application'

new_table.drop_duplicates().to_csv(destinationFolder / f'{TAB_NAME}.csv', index = False)
# +
from gssutils.metadata import THEME

scraper.dataset.family = 'health'
scraper.dataset.theme = THEME['health-social-care']
with open(destinationFolder / f'{TAB_NAME}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -

schema = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
schema.create(destinationFolder / f'{TAB_NAME}.csv', destinationFolder / f'{TAB_NAME}.csv-schema.json')

new_table


# In[42]:


tab = tabsTables['Table 15']

cell = tab.excel_ref('A4')
reason = cell.shift(RIGHT).expand(DOWN).is_not_whitespace().is_not_blank().shift(LEFT)
exclude = tab.excel_ref('A14').expand(DOWN).expand(RIGHT)
exclude2 = tab.excel_ref('N3').expand(RIGHT).expand(DOWN)
reason2 = reason - exclude
period = cell.shift(1,-1).expand(RIGHT).is_not_blank().is_not_whitespace() - exclude2
observations = cell.shift(RIGHT).expand(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().is_number() - exclude - exclude2

Dimensions = [
            HDim(reason2,'Identified Support Needs of Homeless Households',DIRECTLY,LEFT),
            HDim(period,'Period',DIRECTLY,ABOVE),
            HDimConst('Measure Type','Count'),
            HDimConst('Unit','People')            
            ]
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
savepreviewhtml(c1, fname="Preview.html")


# In[43]:


new_table = c1.topandas()
import numpy as np
new_table['OBS'].replace('', np.nan, inplace=True)
new_table.dropna(subset=['OBS'], inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Period'] = new_table['Period'].map(
    lambda x: f'gregorian-interval/{left(x,2) + right(x,2)}-03-31T00:00:00/P1Y')
new_table = new_table[['Period','Identified Support Needs of Homeless Households','Measure Type','Value','Unit']]
new_table['Identified Support Needs of Homeless Households'] = new_table.apply(lambda x: pathify(x['Identified Support Needs of Homeless Households']), axis = 1)
new_table


# In[44]:


destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TAB_NAME = 'Support-need-identified-for-those-homeless-2007-08-to-2018-19'

new_table.drop_duplicates().to_csv(destinationFolder / f'{TAB_NAME}.csv', index = False)
# +
from gssutils.metadata import THEME

scraper.dataset.family = 'health'
scraper.dataset.theme = THEME['health-social-care']
with open(destinationFolder / f'{TAB_NAME}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
# -

schema = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
schema.create(destinationFolder / f'{TAB_NAME}.csv', destinationFolder / f'{TAB_NAME}.csv-schema.json')

new_table

