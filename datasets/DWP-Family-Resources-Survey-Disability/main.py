#!/usr/bin/env python
# coding: utf-8

# In[92]:


from gssutils import *
from databaker.framework import *
import pandas as pd
from gssutils.metadata import THEME

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

scraper = Scraper('https://www.gov.uk/government/statistics/family-resources-survey-financial-year-201718')


# In[93]:


dist = scraper.distribution(title=lambda t: 'Disability data tables (XLS)' in t)
tabs = (t for t in dist.as_databaker())
tidied_sheets = []

for tab in tabs:
    
    if tab.name in ['4_1']:
        cell = tab.filter("Year")
    
        year = cell.shift(RIGHT).expand(DOWN).is_not_blank().shift(LEFT)

        remove = tab.filter("Sample size").expand(DOWN)

        age = cell.shift(RIGHT).expand(RIGHT).is_not_blank() - remove

        observations = year.shift(RIGHT).expand(RIGHT).is_not_blank() - remove

        dimensions = [
                #HDimConst('Dimension Name', 'Variable'),
                HDimConst('Disability','Disabled'),
                HDimConst('Gender','All'),
                HDim(year, 'Period', DIRECTLY, LEFT), 
                HDim(age, 'Age Group', DIRECTLY, ABOVE),
                HDimConst('Measure type','Percentage'),
                HDimConst('Unit','Percent'),
                HDimConst('Region', 'United Kingdom')
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets.append(c1.topandas())
    
    elif tab.name in ['4_2']:
        
        cell = tab.excel_ref("B9")

        remove = tab.filter('Percentage of people').expand(RIGHT).expand(LEFT).expand(DOWN)
    
        year = cell.shift(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().shift(LEFT) - remove

        gender = cell.shift(1,0).expand(RIGHT).is_not_blank().is_not_whitespace()

        observations = gender.fill(DOWN).is_not_blank().is_not_whitespace() - remove

        dimensions = [
                HDim(gender, 'Disability', DIRECTLY, ABOVE),
                HDim(year, 'Period', DIRECTLY, LEFT), 
                HDim(gender, 'Gender', DIRECTLY, ABOVE), 
                HDimConst('Age Group', 'All people'),
                HDimConst('Measure type','Count'),
                HDimConst('Unit','people-millions') ,
                HDimConst('Region', 'United Kingdom')
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets.append(c1.topandas())
        
    elif tab.name in ['4_3']:
        
        cell = tab.excel_ref("B9")

        remove = tab.filter('Percentage of people').expand(RIGHT).expand(DOWN).expand(LEFT)
    
        age = cell.shift(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().shift(LEFT) - remove

        gender = tab.excel_ref("C9").expand(RIGHT).is_not_blank().is_not_whitespace() - remove

        observations = gender.shift(0,5).fill(DOWN).is_not_blank().is_not_whitespace() - remove

        dimensions = [
                HDim(gender,'Disability', DIRECTLY, ABOVE),
                HDim(age, 'Age Group', DIRECTLY, LEFT), 
                HDimConst('Region', 'United Kingdom'), 
                HDimConst('Period', '2015-18'),
                HDim(gender, 'Gender', DIRECTLY, ABOVE),
                HDimConst('Measure type','Count'),
                HDimConst('Unit','people-millions')
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets.append(c1.topandas())
    
    elif tab.name in ['4_4']:
        
        cell = tab.excel_ref("B7")

        remove = tab.filter('Percentage of people').expand(RIGHT).expand(DOWN)
    
        #age = cell.shift(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().shift(LEFT) - remove

        region = cell.expand(DOWN).is_not_blank().is_not_whitespace()

        observations = region.fill(RIGHT).is_not_blank().is_not_whitespace() - remove

        dimensions = [
                HDimConst('Disability','Disabled'),
                HDimConst('Age Group', 'All people'), 
                HDim(region, 'Region', DIRECTLY, LEFT), 
                HDimConst('Period', '2017/18'),
                HDimConst('Gender', 'All people'),
                HDimConst('Measure type','Count'),
                HDimConst('Unit','people-millions')
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets.append(c1.topandas())
        
    elif tab.name in ['4_5']:
        
        cell = tab.excel_ref("B9")

        remove = tab.filter('Sample size').expand(RIGHT).expand(LEFT).expand(DOWN)
    
        disability = cell.fill(DOWN).is_not_blank().is_not_whitespace() - remove

        year = cell.shift(1,0).expand(RIGHT).is_not_blank().is_not_whitespace()

        observations = year.fill(DOWN).is_not_blank().is_not_whitespace() - remove

        dimensions = [
                HDim(disability, 'Disability', DIRECTLY, LEFT),
                HDimConst('Age Group', 'All people'), 
                HDimConst('Gender', 'All people'), 
                HDim(year, 'Period', DIRECTLY, ABOVE),
                HDimConst('Measure type','Count'),
                HDimConst('Unit','people-millions'),
                HDimConst('Region', 'United Kingdom') 
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets.append(c1.topandas())
        
    elif tab.name in ['4_6']:
        
        cell = tab.excel_ref("B8")

        remove = tab.filter('Sample size').expand(RIGHT).expand(LEFT).expand(DOWN)
    
        disability = cell.fill(DOWN).is_not_blank().is_not_whitespace() - remove

        age = cell.shift(1,0).expand(RIGHT).is_not_blank().is_not_whitespace()

        observations = age.fill(DOWN).is_not_blank().is_not_whitespace() - remove
        
        over = {'All disabled people': 'All people'}

        dimensions = [
                HDim(disability, 'Disability', DIRECTLY, LEFT),
                HDim(age, 'Age Group', DIRECTLY, ABOVE, cellvalueoverride = over), 
                HDimConst('Gender', 'All people'), 
                HDimConst('Period', '2017/18'),
                HDimConst('Measure type','Percentage'),
                HDimConst('Unit','Percent'),
                HDimConst('Region', 'United Kingdom')
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets.append(c1.topandas())
        
    #4_7,8,9 need looking into - doesn't look like something easily represented - also only percentages
           
    else:
        continue
    


# In[94]:


new_table = pd.concat(tidied_sheets, ignore_index = True, sort = True).fillna('')
import numpy as np
new_table['OBS'].replace('', np.nan, inplace=True)
new_table.dropna(subset=['OBS'], inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Period'] = new_table['Period'].map(
    lambda x: 'government-year/' + left(x,4) +'-20' + right(x,2))
new_table['Age Group'] = new_table['Age Group'].map(
    lambda x: left(x, len(x) - 1) if x.endswith('1') else x)
new_table['Age Group'] = new_table['Age Group'].map(
    lambda x: x.replace('2', '') if '2' in x else x)
new_table['Age Group'] = new_table['Age Group'].map(
    lambda x: pathify(x))
new_table['Region'] = new_table['Region'].map(
    lambda x: pathify(x))
tidy = new_table[['Period','Region','Disability','Gender','Age Group','Measure type','Value','Unit']]


# In[95]:


tidy = tidy.replace({'Disability' : {
    'All disabled people' : 'Any Disability', 
    'All not disabled people' : 'No Disability', 
    'All people' : 'All',
    'Female, disabled' : 'Any Disability', 
    'Female, not disabled' : 'No Disability', 
    'Females' : 'Any Disability', 
    'Male, disabled' : 'Any Disability',
    'Male, not disabled' : 'No Disability', 
    'Males' : 'Any Disability',
    'Stamina/\nbreathing/\nfatigue' : 'Stamina/breathing/fatigue'}})
tidy = tidy.replace({'Gender' : {
    'All' : 'T',
    'All disabled people' : 'T', 
    'All not disabled people' : 'T', 
    'All people' : 'T',
    'Female, disabled' : 'F', 
    'Female, not disabled' : 'F', 
    'Females' : 'F', 
    'Male, disabled' : 'M',
    'Male, not disabled' : 'M', 
    'Males' : 'M'}}) 
tidy = tidy.replace({'Age Group' : { 
    'All people' : 'All'}})
tidy = tidy.replace({'Region' : { 
    'east' : 'E12000006', 
    'east-midlands' : 'E12000004', 
    'england' : 'E92000001',
    'great-britain' : 'K03000001',
    'inner-london' : 'E13000001',
    'london' : 'E12000007',
    'north-east' : 'E12000001',
    'north-west' : 'E12000002',
    'northern-ireland' : 'N07000001',
    'outer-london' : 'E13000002',
    'scotland' : 'S04000001',
    'south-east' : 'E12000008',
    'south-west' : 'E12000009',
    'united-kingdom' : 'K02000001',
    'wales' : 'W08000001',
    'west-midlands' : 'E12000005',
    'yorkshire-and-the-humber' : 'E12000003',}})


# In[96]:


tidy['Disability'] = tidy['Disability'].map(
    lambda x: pathify(x))

tidy.rename(columns={'Disability':'DWP Disability'}, 
                 inplace=True)

from IPython.core.display import HTML
for col in tidy:
    if col not in ['Value']:
        tidy[col] = tidy[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(tidy[col].cat.categories)       


# In[97]:


pd.set_option('display.float_format', lambda x: '%.0f' % x)

tidy.rename(columns={'Gender':'Sex',
                   'Region':'Area',
                   'Age Group':'DWP Age Group',
                   'Measure type':'Measure Type'}, 
          inplace=True)


# In[98]:


destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TAB_NAME = 'observations'

tidy.drop_duplicates().to_csv(destinationFolder / f'{TAB_NAME}.csv', index = False)
tidy


# In[99]:


scraper.dataset.family = 'disability'
#scraper.dataset.theme = THEME['health-social-care']
with open(destinationFolder / 'observations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
csvw.create(destinationFolder / 'observations.csv', destinationFolder / 'observations.csv-schema.json')

