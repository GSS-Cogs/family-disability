# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/collections/statistics-special-educational-needs-sen')
scraper.select_dataset(title=lambda x: x.startswith('Statements of SEN and EHC Plans'), latest=True)

next_table = pd.DataFrame()

# +
# %%capture

# %run "Table 1.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 2.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 3.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 4.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 5.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 6.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 7.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 8.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 9.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 10.py"
next_table = pd.concat([next_table, new_table])
# %run "Table 11.py"
next_table = pd.concat([next_table, new_table])
# -

next_table['DfE Age Groups'] = next_table['DfE Age Groups'].map(
    lambda x: {
        'Under 5 years of age' : 'under-5', 
        'all ages' : 'all',
        'Aged 5-10': 'age-5-to-10' ,
        'Aged 11-15': 'age-11-to-15',
        'Aged 16-19' : 'age-16-to-19',
        'Aged 20-25' : 'age-20-to-25'}.get(x, x))

next_table['DfE Statements or EHC Plan Type'] = next_table['Statements or EHC Plan Type'].apply(pathify)

next_table['DfE Statements or EHC Plan Type'] = next_table['DfE Statements or EHC Plan Type'].str.rstrip('()1324569')

next_table['DfE Statements or EHC Plan Type'] = next_table['DfE Statements or EHC Plan Type'].map(
    lambda x: {
        'total' : 'all-plans', 
        'ehc-plan' : 'ehc-plans',
        'ehc-plans3-38-to-51-weeks-per-year': 'ehc-plans-38-to-51-weeks-per-year' ,
        'ehc-plans3-52-weeks-per-year': 'ehc-plans-52-weeks-per-year',
        }.get(x, x))

next_table['DfE Statements of SEN or EHC Plan Provider'] = next_table['Statements of SEN or EHC Plan Provider'].str.rstrip('132478,0569')
next_table['DfE Statements of SEN or EHC Plan Provider'] = next_table['DfE Statements of SEN or EHC Plan Provider'].str.lstrip()
next_table['DfE Statements of SEN or EHC Plan Provider'] = next_table['DfE Statements of SEN or EHC Plan Provider'].str.rstrip()

next_table['DfE Statements of SEN or EHC Plan Provider'] = next_table['DfE Statements of SEN or EHC Plan Provider'].apply(pathify) 

next_table['DfE Statements of SEN or EHC Plan Provider'] = next_table['DfE Statements of SEN or EHC Plan Provider'].map(
    lambda x: {
        'academy/free' : 'academy-free', 
        'general-fe-and-tertiary-colleges/he' : 'general-fe-and-tertiary-colleges-he',
        'special-school-academy/free': 'special-school-academy-free' ,
        'alternative-provision-ap-/pupil-referral-unit-pru-la-maintained': 'alternative-provision-ap-pupil-referral-unit-pru-la-maintained',
        'ap/pru-academy' : 'ap-pru-academy',
        'ap/pru-free-school' : 'ap-pru-free-school'
        
        }.get(x, x))

next_table['DfE Statements of SEN or EHC Plan Description'] = next_table['Statements of SEN or EHC Plan Description'].str.rstrip('132478,0569:')
next_table['DfE Statements of SEN or EHC Plan Description'] = next_table['DfE Statements of SEN or EHC Plan Description'].str.lstrip()
next_table['DfE Statements of SEN or EHC Plan Description'] = next_table['DfE Statements of SEN or EHC Plan Description'].str.rstrip()

next_table['DfE Statements of SEN or EHC Plan Description'] = next_table['DfE Statements of SEN or EHC Plan Description'].apply(pathify)

next_table['DfE Marker'] = next_table['Marker'].map(
    lambda x: {
        '.' : 'not-applicable', 
        '..' : 'not-available'}.get(x, x))
next_table['DfE Marker'] = next_table['DfE Marker'].fillna('no-marker')

next_table.rename(columns={'Geography': 'DfE Geography'}, inplace=True)

next_table['Period'] = next_table['Year'].str.replace('\.0', '')
next_table['Period'] = next_table['Period'].str.lower()

next_table['Period'] = next_table['Period'].str.lower()

next_table = next_table[['Period','DfE Geography','DfE Statements of SEN or EHC Plan Description','DfE Statements or EHC Plan Type','DfE Statements of SEN or EHC Plan Provider','DfE Age Groups','Unit','Value','Measure Type', 'DfE Marker']]

from pathlib import Path
out = Path('out')
out.mkdir(exist_ok=True)
next_table.drop_duplicates().to_csv(out / 'observations.csv', index = False)

scraper.dataset.family = 'disability'
with open(out / 'observations.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')
