#!/usr/bin/env python
# coding: utf-8

# In[192]:


from gssutils import *
from databaker.framework import *
import pandas as pd
import datetime

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

year = right(str(datetime.datetime.now().year),2)

scraper = Scraper('https://www.gov.uk/government/statistics/family-resources-survey-financial-year-201718')


# In[193]:


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
                HDimConst('Unit','People (Millions)') ,
                HDimConst('Region', 'United Kingdom')   
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets.append(c1.topandas())
        
    elif tab.name in ['4_3']:
        
        cell = tab.excel_ref("B9")

        remove = tab.filter('Percentage of people').expand(RIGHT).expand(LEFT).expand(DOWN)
    
        age = cell.shift(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace().shift(LEFT) - remove

        gender = cell.shift(1,0).expand(RIGHT).is_not_blank().is_not_whitespace()

        observations = gender.fill(DOWN).is_not_blank().is_not_whitespace() - remove

        dimensions = [
                HDim(gender, 'Disability', DIRECTLY, ABOVE),
                HDim(age, 'Age Group', DIRECTLY, LEFT), 
                HDim(gender, 'Gender', DIRECTLY, ABOVE), 
                HDimConst('Period', '2015-18'),
                HDimConst('Measure type','Count'),
                HDimConst('Unit','People (Millions)'),
                HDimConst('Region', 'United Kingdom')    
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
                HDimConst('Unit','People (Millions)')    
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
                HDimConst('Unit','People (Millions)'),
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
                HDimConst('Measure type','Count'),
                HDimConst('Unit','People (Millions)'),
                HDimConst('Region', 'United Kingdom')    
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets.append(c1.topandas())
        
    #4_7,8,9 need looking into - doesn't look like something easily represented - also only percentages
        
    else:
        continue


# In[194]:


new_table = pd.concat(tidied_sheets, ignore_index = True, sort = True).fillna('')
import numpy as np
new_table['OBS'].replace('', np.nan, inplace=True)
new_table.dropna(subset=['OBS'], inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
#new_table['Period'] = new_table['Period'].map(
    #lambda x: f'gregorian-interval/{left(x,2) + right(x,2)}-03-31T00:00:00/P1Y')
new_table['Age Group'] = new_table['Age Group'].map(
    lambda x: left(x, len(x) - 1) if x.endswith('1') else x)
new_table['Age Group'] = new_table['Age Group'].map(
    lambda x: x.replace('2', '') if '2' in x else x)
tidy = new_table[['Period','Region','Disability','Gender','Age Group','Measure type','Value','Unit']]


# In[195]:


tidy = tidy.replace({'Disability' : {
    'All disabled people' : 'Disabled', 
    'All not disabled people' : 'Not Disabled', 
    'All people' : 'All',
    'Female, disabled' : 'Disabled', 
    'Female, not disabled' : 'Not Disabled', 
    'Females' : 'Disabled', 
    'Male, disabled' : 'Disabled',
    'Male, not disabled' : 'Not Disabled', 
    'Males' : 'Disabled',
    'Stamina/\nbreathing/\nfatigue' : 'Stamina/breathing/fatigue'}})
tidy = tidy.replace({'Gender' : {
    'All disabled people' : 'All', 
    'All not disabled people' : 'All', 
    'All people' : 'All',
    'Female, disabled' : 'Female', 
    'Female, not disabled' : 'Female', 
    'Females' : 'Female', 
    'Male, disabled' : 'Male',
    'Male, not disabled' : 'Male', 
    'Males' : 'Male'}}) 
tidy = tidy.replace({'Age Group' : { 
    'All people' : 'All'}})


# In[196]:


from IPython.core.display import HTML
for col in tidy:
    if col not in ['Value']:
        tidy[col] = tidy[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(tidy[col].cat.categories)


# In[197]:


destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)

TAB_NAME = 'observations'

tidy.drop_duplicates().to_csv(destinationFolder / f'{TAB_NAME}.csv', index = False)
tidy


# In[ ]:





# In[ ]:




