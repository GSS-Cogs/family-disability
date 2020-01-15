#!/usr/bin/env python
# coding: utf-8

# In[72]:


from gssutils import *
from databaker.framework import *
import pandas as pd
import numpy as np
from gssutils.metadata import THEME

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

scraper = Scraper('https://www.gov.uk/government/statistics/work-and-health-programme-statistics-to-august-2019')
scraper


# In[75]:


dist = scraper.distribution(title=lambda t: 'Tables' in t)
tabs = (t for t in dist.as_databaker())
tidy_tabs = {}

for tab in tabs:
    
    if tab.name in ['1_1']:
        
        tab_name = 'Number of Referrals, Individuals Referred and Starts by month of referral by Referral Group'
        
        cell = tab.filter("In month")
        
        remove = cell.fill(DOWN).filter('Total').expand(RIGHT)
    
        period = cell.shift(RIGHT).fill(DOWN).is_not_blank().shift(LEFT) - remove        

        referralGroup = cell.shift(1,-1).expand(RIGHT).is_not_blank()
        
        remove2 = referralGroup.filter('Total').expand(RIGHT).expand(DOWN)
        
        obsType = cell.fill(RIGHT)

        observations = period.shift(RIGHT).expand(RIGHT).is_not_blank() - remove2

        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT), 
                HDim(referralGroup, 'Referral Group', CLOSEST, LEFT),
                HDim(obsType, 'Observation Type', DIRECTLY, ABOVE),
                HDimConst('Gender', 'all'),
                HDimConst('Age Group', 'all'),
                HDimConst('Measure Type','Count'),
                HDimConst('Unit','People'),
                HDimConst('Region', 'England and Wales')
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets = []
        tidied_sheets.append(c1.topandas())
        
        new_table_1_1 = pd.concat(tidied_sheets, ignore_index = True, sort = True).fillna('')
        
        tidy_tabs[tab_name] = new_table_1_1
        
    elif tab.name in ['1_2']:
        
        tab_name = 'Number of Starts and Job Outcomes achieved within 6 and 12 months of starting, by Start month by Referral Group'
        
        cell = tab.filter("In month")
        
        remove = tab.filter("Percentage within 6 months").expand(RIGHT).expand(DOWN)
        
        period = cell.shift(2,0).fill(DOWN).is_not_blank().shift(-2,0) - remove

        referralGroup = cell.fill(RIGHT).is_not_blank()
        
        obsType = cell.shift(1,-1).fill(RIGHT).is_not_blank()

        observations = period.fill(RIGHT).is_not_blank() - remove

        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT), 
                HDim(referralGroup, 'Referral Group', DIRECTLY, ABOVE),
                HDim(obsType, 'Observation Type', CLOSEST, LEFT),
                HDimConst('Gender', 'all'),
                HDimConst('Age Group', 'all'),
                HDimConst('Measure Type','Count'),
                HDimConst('Unit','People'),
                HDimConst('Region', 'England and Wales')
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets = []
        tidied_sheets.append(c1.topandas())
        
        new_table_1_2 = pd.concat(tidied_sheets, ignore_index = True, sort = True).fillna('')
        
        tidy_tabs[tab_name] = new_table_1_2       
        
    elif tab.name in ['1_3']:
        
        tab_name = 'Number of Starts and Job Outcomes by Start month and Referral Group'
        
        cell = tab.filter("In month")
        
        remove = tab.filter("Percentage").expand(RIGHT).expand(DOWN)
        
        period = cell.shift(2,0).fill(DOWN).is_not_blank().shift(-2,0) - remove 

        referralGroup = cell.fill(RIGHT).is_not_blank()
        
        obsType = cell.shift(1,-1).fill(RIGHT).is_not_blank()

        observations = period.fill(RIGHT).is_not_blank() - remove

        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT), 
                HDim(referralGroup, 'Referral Group', DIRECTLY, ABOVE),
                HDim(obsType, 'Observation Type', CLOSEST, LEFT),
                HDimConst('Gender', 'all'),
                HDimConst('Age Group', 'all'),
                HDimConst('Measure Type','Count'),
                HDimConst('Unit','People'),
                HDimConst('Region', 'England and Wales')
            
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets = []
        tidied_sheets.append(c1.topandas())
        
        new_table_1_3 = pd.concat(tidied_sheets, ignore_index = True, sort = True).fillna('')
        
        tidy_tabs[tab_name] = new_table_1_3
        
    elif tab.name in ['1_4']:
        
        tab_name = 'Job Outcomes by Job Outcome month'
        
        cell = tab.filter("In month")
        
        remove = cell.expand(DOWN).filter("Total").expand(RIGHT).expand(DOWN)
        
        period = cell.shift(2,0).fill(DOWN).is_not_blank().shift(-2,0) - remove 

        referralGroup = cell.fill(RIGHT).is_not_blank()
        
        obsType = cell.shift(1,-1).fill(RIGHT).is_not_blank()

        observations = period.fill(RIGHT).is_not_blank() - remove

        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT), 
                HDim(referralGroup, 'Referral Group', DIRECTLY, ABOVE),
                HDim(obsType, 'Observation Type', CLOSEST, LEFT),
                HDimConst('Gender', 'all'),
                HDimConst('Age Group', 'all'),
                HDimConst('Measure Type','Count'),
                HDimConst('Unit','People'),
                HDimConst('Region', 'England and Wales'),
                HDimConst('DATAMARKER', '')
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets = []
        tidied_sheets.append(c1.topandas())
        
        new_table_1_4 = pd.concat(tidied_sheets, ignore_index = True, sort = True).fillna('')
        
        tidy_tabs[tab_name] = new_table_1_4
        
    elif tab.name in ['2_1']:
        
        tab_name = 'Number of Referrals, Individuals referred and Starts, by Contract Package Area, Local Government Partnership and Referral Group'
        
        cell = tab.filter("Disability1")
        
        remove = tab.filter("2.1").expand(DOWN).filter("Total").expand(RIGHT).expand(DOWN)
        
        referralGroup = cell.expand(RIGHT).is_not_blank()
        
        obsType = cell.shift(0,1).expand(RIGHT).is_not_blank()
        
        area = cell.shift(0,3).expand(DOWN).is_not_blank().shift(-2,0) - remove

        observations = obsType.fill(DOWN).is_not_blank() - remove

        dimensions = [
                HDimConst('Period', 'November 2017 to August 2019 inclusive'), 
                HDim(referralGroup, 'Referral Group', CLOSEST, LEFT),
                HDim(obsType, 'Observation Type', DIRECTLY, ABOVE),
                HDimConst('Gender', 'all'),
                HDimConst('Age Group', 'all'),
                HDimConst('Measure Type','Count'),
                HDimConst('Unit','People'),
                HDim(area, 'Region', DIRECTLY, LEFT),
                HDimConst('DATAMARKER', '')
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets = []
        tidied_sheets.append(c1.topandas())
        
        new_table_2_1 = pd.concat(tidied_sheets, ignore_index = True, sort = True).fillna('')
        
        tidy_tabs[tab_name] = new_table_2_1
        
    elif tab.name in ['2_2']:
        
        tab_name = 'Referrals, Individual Referrals and Starts, by Devolved Deal Area'
        
        cell = tab.filter("In Month")
        
        remove = cell.shift(LEFT).expand(DOWN).filter("1.0").expand(RIGHT).expand(DOWN)
        
        remove2 = cell.shift(2,0).expand(RIGHT).is_not_blank().filter('Total').expand(DOWN)
        
        period = cell.shift(2,0).expand(RIGHT).is_not_blank() - remove2
        
        obsType = cell.shift(0,2).expand(DOWN).is_not_blank() - remove
        
        area = cell.shift(1,2).expand(DOWN).is_not_blank() - remove

        observations = cell.shift(2,3).expand(RIGHT).is_not_blank().shift(UP).expand(DOWN).is_not_blank() - remove - remove2

        dimensions = [
                HDim(period, 'Period', DIRECTLY, ABOVE), 
                HDimConst('Referral Group', 'All'),
                HDim(obsType, 'Observation Type', CLOSEST, ABOVE),
                HDimConst('Gender', 'all'),
                HDimConst('Age Group', 'all'),
                HDimConst('Measure Type','Count'),
                HDimConst('Unit','People'),
                HDim(area, 'Region', DIRECTLY, LEFT)
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets = []
        tidied_sheets.append(c1.topandas())
        
        new_table_2_2 = pd.concat(tidied_sheets, ignore_index = True, sort = True).fillna('')
        
        tidy_tabs[tab_name] = new_table_2_2
        
    elif tab.name in ['3_1']:
        
        tab_name = 'Number of Starts, by age by gender'
        
        cell = tab.filter("3.1").shift(2,5)
        
        obsType = cell.expand(RIGHT).is_not_blank()
        
        gender = cell.shift(-2,2).expand(DOWN).is_not_blank()
        
        age = cell.shift(-1,2).expand(DOWN).is_not_blank()

        observations = cell.shift(0,1).expand(DOWN).is_not_blank()

        dimensions = [
                HDimConst('Period', 'November 2017 to August 2019 inclusive'), 
                HDimConst('Referral Group', 'All'),
                HDim(obsType, 'Observation Type', CLOSEST, ABOVE),
                HDim(gender, 'Gender', CLOSEST, ABOVE),
                HDim(age, 'Age Group', DIRECTLY, LEFT),
                HDimConst('Measure Type','Count'),
                HDimConst('Unit','People'),
                HDimConst('Region', 'England and Wales'),
                HDimConst('DATAMARKER', '')
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets = []
        tidied_sheets.append(c1.topandas())
        
        new_table_3_1 = pd.concat(tidied_sheets, ignore_index = True, sort = True).fillna('')
        
        tidy_tabs[tab_name] = new_table_3_1
        
    elif tab.name in ['3_2']:
        
        tab_name = 'Number of Starts, by Age and Contract Package Area, Local Government Partnership'
        
        cell = tab.filter("3.2").shift(2,5)
        
        remove = tab.filter("3.2").shift(LEFT).expand(DOWN).filter('1.0').expand(DOWN).expand(RIGHT)
        
        obsType = cell.expand(RIGHT).is_not_blank()
        
        age = cell.shift(0,1).expand(RIGHT).is_not_blank()
        
        area = cell.shift(-2,2).expand(DOWN) - remove

        observations = cell.shift(0,2).expand(DOWN).expand(RIGHT).is_not_blank()

        dimensions = [
                HDimConst('Period', 'November 2017 to August 2019 inclusive'), 
                HDimConst('Referral Group', 'All'),
                HDim(obsType, 'Observation Type', CLOSEST, RIGHT),
                HDimConst('Gender','all'),
                HDim(age, 'Age Group', DIRECTLY, ABOVE),
                HDimConst('Measure Type','Count'),
                HDimConst('Unit','People'),
                HDim(area, 'Region', DIRECTLY, LEFT),
                HDimConst('DATAMARKER', '')
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets = []
        tidied_sheets.append(c1.topandas())
        
        new_table_3_2 = pd.concat(tidied_sheets, ignore_index = True, sort = True).fillna('')
        
        tidy_tabs[tab_name] = new_table_3_2
        
    elif tab.name in ['3_3']:
        
        tab_name = 'Starts, by gender'
        
        cell = tab.filter("In month")
        
        period = cell.shift(1,2).expand(DOWN).is_not_blank().shift(LEFT)
        
        remove = period.filter('Total').expand(RIGHT)
        
        obsType = cell.shift(4,-1).expand(RIGHT).is_not_blank()
        
        gender = cell.shift(RIGHT).expand(RIGHT).is_not_blank()
        
        remove2 = gender.filter('Total').fill(DOWN)

        observations = cell.shift(1,2).expand(DOWN).expand(RIGHT).is_not_blank() - remove - remove2

        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT), 
                HDimConst('Referral Group', 'All'),
                HDim(obsType, 'Observation Type', CLOSEST, RIGHT),
                HDim(gender, 'Gender', DIRECTLY, ABOVE),
                HDimConst('Age Group', 'all'),
                HDimConst('Measure Type','Count'),
                HDimConst('Unit','People'),
                HDimConst('Region', 'England and Wales'),
                HDimConst('Tab', '3_3')
        ]
    
        c1 = ConversionSegment(observations, dimensions, processTIMEUNIT=True)
        savepreviewhtml(c1, fname="Preview.html")
        tidied_sheets = []
        tidied_sheets.append(c1.topandas())
        
        new_table_3_3 = pd.concat(tidied_sheets, ignore_index = True, sort = True).fillna('')
        
        tidy_tabs[tab_name] = new_table_3_3
        
    else:
        continue


# In[74]:


for i in tidy_tabs:
    new_table = tidy_tabs.get(i)
    
    new_table.rename(columns={'OBS': 'Value'}, inplace=True)
    new_table['Period'] = new_table['Period'].astype(str)

    new_table['Period'] = new_table['Period'].map(lambda x: 'gregorian-interval/2017-11-01T00:00:00/P22M' if 'inclusive' in x else 'gregorian-interval/' + left(x,4) + '-' + mid(x,5,2) + '-01T00:00:00/P1M')

    new_table['Age Group'] = new_table['Age Group'].map(lambda x: x.replace('Aged ', ''))
    new_table['Age Group'] = new_table['Age Group'].map(lambda x: x.replace('+', ' plus'))
    new_table['Region'] = new_table['Region'].map(lambda x: left(x, len(x) -1) if x.endswith('1') else x)
    new_table['Region'] = new_table['Region'].map(lambda x: left(x, len(x) -1) if x.endswith('3') else x) 
    
    tidy = new_table[['Period','Region','Age Group','Gender','Referral Group','Observation Type','Measure Type','Value','DATAMARKER','Unit']]
        
    tidy = tidy.replace({'Referral Group' : {
        'Disability1' : 'Disability', 
        'Early Access1' : 'Early Access', 
        'Long Term Unemployed2' : 'Long Term Unemployed',
        'Total' : 'all'}})
    tidy = tidy.replace({'Observation Type' : {
        'Individuals Referred 3' : 'Individuals Referred',
        'Individuals Referred4' : 'Individuals Referred',
        'Individual Referrals 1' : 'Individuals Referred',
        'Job Outcome 2' : 'Job Outcome',
        'total' : 'all'}})
    tidy = tidy.replace({'DATAMARKER' : {
        '-' : 'not-applicable', 
        '.' : 'negligible'}})
    tidy = tidy.replace({'Age Group' : {
        'Unknown Age' : 'unknown',
        'Total' : 'all'}})

    tidy.rename(columns={'DATAMARKER' : 'Marker',
                         'Region' : 'DWP Area',
                         'Gender' : 'Sex',
                         'Age Group' : 'DWP Age Group',
                         'Observation Type' : 'DWP Referral Type',
                         'Referral Group' : 'DWP Referral Group'}, inplace=True)

    tidy['DWP Referral Group'] = tidy['DWP Referral Group'].map(lambda x: pathify(x))
    tidy['DWP Referral Type'] = tidy['DWP Referral Type'].map(lambda x: pathify(x))
    tidy['DWP Area'] = tidy['DWP Area'].map(lambda x: pathify(x))
    tidy['Sex'] = tidy['Sex'].map(lambda x: pathify(x))
    tidy['DWP Age Group'] = tidy['DWP Age Group'].map(lambda x: pathify(x))
    #tidy = tidy.replace({'Area' : {'england-and-wales' : 'K04000001'}})

    tidy = tidy.replace({'Sex' : {
        'all' : 'T', 
        'female' : 'F', 
        'females' : 'F', 
        'male' : 'M', 
        'males' : 'M', 
        'unknown' : 'T'}})
    
    destinationFolder = Path('out')
    destinationFolder.mkdir(exist_ok=True, parents=True)

    TAB_NAME = pathify(i)
    
    tidy.drop_duplicates().to_csv(destinationFolder / f'{TAB_NAME}.csv', index = False)
    
    scraper.dataset.family = 'disability'
    #scraper.dataset.theme = THEME['health-social-care']
    with open(destinationFolder / 'observations.csv-metadata.trig', 'wb') as metadata:
        metadata.write(scraper.generate_trig())

    csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
    csvw.create(destinationFolder / f'{TAB_NAME}.csv', destinationFolder / f'{TAB_NAME}.csv-schema.json')


# In[ ]:




