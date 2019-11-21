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
