# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# Adult Social Care Activity and Finance Report, England

from gssutils import *
from gssutils.metadata import THEME
scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-activity-and-finance-report')
scraper

scraper.select_dataset(latest=True)
scraper

data_pack = scraper.distribution(title=lambda x: 'CSV DATA PACK' in x, mediaType='application/zip')
data_pack

with data_pack.open() as data_stream:
    buffered_data = BytesIO(data_stream.read())
    with ZipFile(buffered_data) as zip_file:
        for name in zip_file.namelist():
            display(name)
            if name.startswith('ASC') and name.endswith('.csv'):
                with zip_file.open(name, 'r') as csv_file:
                    observations = pd.read_csv(TextIOWrapper(csv_file, encoding='utf-8'))
observations

# +
from IPython.core.display import HTML

for col in observations:
    if col not in ['ITEMVALUE', 'CASSR', 'UUID']:
        observations[col] = observations[col].astype('category')
        display(HTML(f'<h2>{col}</h2>'))
        display(observations[col].cat.categories)
