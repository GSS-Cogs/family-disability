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

# Adult Social Care Activity and Finance Report, England 2018-19: CSV DATA PACK

from gssutils import *
from gssutils.metadata import THEME
scraper = Scraper('https://digital.nhs.uk/data-and-information/publications/statistical/adult-social-care-activity-and-finance-report')
scraper.select_dataset(latest=True)

scraper

for dist in scraper.distributions:
    print(dist.downloadURL)

from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO, TextIOWrapper

csvfiles = []
with ZipFile(BytesIO(scraper.session.get(scraper.distributions[3].downloadURL).content)) as File:
    for name in File.namelist():
        print(name)
        if '.csv' in name:
            if not os.path.isdir(name):
                with File.open(name) as f:
                    print(type(f))
                    csvfile = pd.read_csv(f, encoding='utf-8')
                    csvfiles.append(csvfile)

list(csvfiles[0])

ascfrdata = csvfiles[0]

ascfrdata.drop(['GEOGRAPHY_LEVEL',
 'DATA_LEVEL',
'FY_ENDING',
 'GEOGRAPHY_CODE',
 'DH_GEOGRAPHY_NAME',
 'REGION_GO_CODE',
 'GEOGRAPHY_NAME',
 'DataType_Key',
 'ComparativeTotals_Key',
 'DataSource_Key',
 'ValueType_Key',
  'CarerSupportType_Key' ], axis = 1, inplace = True)

ascfrdata['Period'] = 'gregorian-interval/2018-04-01T00:00:00/P1Y'


# +
def f(x):
    if x == ':':
        return 'Data not submitted'
    elif x == '*':
        return 'Data suppressed'
    else :
        return ''

ascfrdata['NHS Marker'] = ascfrdata.apply(lambda row: f(row['ITEMVALUE']), axis = 1)
ascfrdata['ITEMVALUE'] = pd.to_numeric(ascfrdata['ITEMVALUE'], errors = 'coerce')
# -

ascfrdata.rename(columns= {'CASSR':'NHS Geography',
                           'UUID' : 'ASC-FR UUID',
                           'DimensionGroup' : 'ASC-FR Group',
                           'CareType_Key' : 'Care Type',
                           'FinanceType_Key' : 'Finance Type',
                           'FinanceDescription_Key': 'Finance Description',
                           'AgeBand_Key' : 'Age',
                           'PrimarySupportReason_Key' : 'Primary Support Reason',
                           'SupportSetting_Key' : 'Support Setting',
                           'Purpose_Key' : 'Purpose',
                           'ActivityProvision_Key': 'Activity Provision',
                           'ITEMVALUE':'Value'
                          }, inplace = True)

# +
# from pathlib import Path
# out = Path('out')
# out.mkdir(exist_ok=True)
# ascfrdata.drop_duplicates().to_csv(out / 'ascfrdata-observations.csv', index = False)

# +
# scraper.dataset.family = 'disability'
# with open(out / 'ascfrdata-observations.csv-metadata.trig', 'wb') as metadata:
#     metadata.write(scraper.generate_trig())

# +
# csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
# csvw.create(out / 'ascfrdata-observations.csv', out / 'ascfrdata-observations.csv-schema.json')
