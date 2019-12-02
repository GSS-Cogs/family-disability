#!/usr/bin/env python
# coding: utf-8

# In[37]:


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

# In[38]:


distCharts = scraper.distribution(title=lambda t: 'Charts' in t)
#distTables = scraper.distribution(title=lambda t: 'Tables' in t)

tabsCharts = {tab.name: tab for tab in distCharts.as_databaker()}


# In[39]:


tab = tabsCharts['Data6']

cell = tab.filter('Refused')
reason = cell.shift(1,-1).expand(DOWN).is_not_whitespace().shift(LEFT).is_not_blank()
period = cell.shift(1,-1).expand(RIGHT).is_not_blank().is_not_whitespace()
observations = cell.shift(RIGHT).expand(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().is_number()

Dimensions = [
            HDim(reason,'Reason(s) for failing to maintain accommodation',DIRECTLY,LEFT),
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
    lambda x: f'gregorian-interval/{right(x,4)}-03-31T00:00:00/P1Y')
new_table = new_table[['Period','Reason(s) for failing to maintain accommodation','Measure Type','Value','Unit']]
new_table['Reason(s) for failing to maintain accommodation'] = new_table.apply(lambda x: pathify(x['Reason(s) for failing to maintain accommodation']), axis = 1)
new_table


# In[41]:


destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TAB_NAME = 'Reason(s)-for-failing-to-maintain-accommodation'

new_table.drop_duplicates().to_csv(destinationFolder / f'{TAB_NAME}.csv', index = False)


# In[42]:


destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TAB_NAME = 'Reason(s)-for-failing-to-maintain-accommodation'

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


# In[43]:


tab = tabsCharts['Data9']

cell = tab.filter('Learning disability')
support = cell.shift(1,-1).expand(DOWN).is_not_whitespace().shift(LEFT).is_not_blank()
period = cell.shift(1,-1)
observations = cell.shift(RIGHT).expand(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().is_number()

Dimensions = [
            HDim(support,'Identified Support Needs of Homeless Households',DIRECTLY,LEFT),
            HDim(period,'Period',DIRECTLY,ABOVE),
            HDimConst('Measure Type','Count'),
            HDimConst('Unit','People')            
            ]
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
savepreviewhtml(c1, fname="Preview.html")


# In[47]:


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


# In[45]:


destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TAB_NAME = 'Identified-Support-Needs-of-Homeless-Households-2018-19'

new_table.drop_duplicates().to_csv(destinationFolder / f'{TAB_NAME}.csv', index = False)


# In[46]:


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


# In[ ]:




