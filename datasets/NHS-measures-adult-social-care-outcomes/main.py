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

# %%
table.rename(columns={
    'Geographical Code': 'NHS Geography',
    'ONS Area Code': 'ONS Geography'
}, inplace=True)
table.drop(columns=['Geographical Description', 'Geographical Level'], inplace=True)
table

# %%
for col in table:
    if col not in 'Measure Value':
        table[col] = table[col].astype('category')
        display(col)
        display(table[col].cat.categories)

# %%
out = Path('out')
out.mkdir(exist_ok=True, parents=True)
table.to_csv(out / 'observations.csv', index = False)


# %%
scraper.dataset.family = 'health'
scraper.dataset.theme = THEME['health-social-care']
with open(out / 'dataset.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())


# %%
csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')

# %%
