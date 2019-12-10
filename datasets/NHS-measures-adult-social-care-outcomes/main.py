#!/usr/bin/env python
# coding: utf-8
# %%
from gssutils import *

scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-outcomes-framework-ascof')
scraper


# %%
scraper.select_dataset(latest=True)
scraper


# %%
dist = scraper.distribution(latest=True, mediaType='text/csv')
dist


# %%
table = dist.as_pandas(encoding='Windows-1252')
table

# %% [markdown]
#  'Geographical Description', 'Geographical Level' removed as those covered by 'Geographical Code'
#  'ONS Area Code' removed as data set relevant code kept in tidy data, and also based on 
#  https://files.digital.nhs.uk/19/C45DF7/meas-from-asc-of-eng-1819-Appendices.pdf due to variation in both geographical codes, only `Geographical Code` in tidy data 

# %%
table.rename(columns={
    'Geographical Code': 'NHS Geography'    
}, inplace=True)
table.drop(columns=['Geographical Description', 'Geographical Level','ONS Area Code', 
                    'Measure Group Description'], inplace=True)

# %% [markdown]
# Here ideal Tidy data should look like this with dimensions
# `NHS Geography,	ASCOF Measure Code,	Measure Group Description, Measure Type, Value, CI, Count`
# But data have various missing values for ASCOF Codes, not all Outcome have Margin Of Error , 
# Here ASCOF codes were more than observations, Outcome are 17868 and Margin Of Error are only 10126, so significant amount of data missing.

# %%
nt1 = table[table['Measure Type'] == 'Outcome']

# %%
nt1.columns = ['Value' if x=='Measure Value' else x for x in table.columns]

# %%
nt2 = table[table['Measure Type'] == 'Margin Of Error']

# %%
nt2.columns = ['CI' if x=='Measure Value' else x for x in table.columns]

# %%
nt2.drop(columns=['Measure Type', 'Disaggregation Level','Measure Group'], inplace=True)

# %%
Final_table = pd.merge(nt1, nt2, how = 'outer', on = ['NHS Geography','ASCOF Measure Code'])

# %%
Final_table = Final_table[Final_table['Value'].isnull() == False]

# %% [markdown]
# 'c' not defined in source data

# %%
Final_table = Final_table[Final_table['Value'] != 'c' ]

# %%
Final_table['Disaggregation Level'] = Final_table['Disaggregation Level'].map(
                        lambda x: {
                            'Female' : 'F', 'Total' : 'T', '65 and over': '65-plus', 'Male' :'M', 
                            '64 and under':'under-64', '85 and over' : '85-plus'}.get(x, x))

# %%
Final_table = Final_table[['NHS Geography','ASCOF Measure Code','Disaggregation Level','Measure Group','Measure Type','Value','CI']]

# %%
out = Path('out')
out.mkdir(exist_ok=True, parents=True)
Final_table.to_csv(out / 'observations.csv', index = False)


# %%
scraper.dataset.family = 'health'
scraper.dataset.theme = THEME['health-social-care']
with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())


# %%
csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')
