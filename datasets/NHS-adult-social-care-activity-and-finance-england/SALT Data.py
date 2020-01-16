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

saltdata = csvfiles[1]

list(saltdata)

saltdata.drop(
['GEOGRAPHY_LEVEL',
 'FY_Ending',
 'SHEET',
 'TABLE',
 'ADDITIONAL_CELLS',
 'DATA_LEVEL',
 'GEOGRAPHY_CODE',
 'DH_GEOGRAPHY_NAME',
 'REGION_GO_CODE',
 'GEOGRAPHY_NAME',
 'RouteOfAccess_Key',
 'SequelToSTMax_Key',
 'NoServicesProvided_Key',
 'PrimarySupportReason_Key',
 'ShortTermPeriod_Key',
 'Gender_Key',
 'DischargeStatus_Key',
 'LongTermPeriod_Key',
 'CommunitySupport_Key',
 'EthnicityGrouping_Key',
  'RouteOfTransitionDesc_Key',
 'CarerType_Key',
  'SupportToCarerType_Key',
  'SupportToCarerDesc_Key',
  'AgeAtAssessment_Key',
 'AgeAtTransition_Key',
 'ReportedHealthCondGroup_Key',
 'ReportedHealthCondDesc_Key',
 'ReviewType_Key',
  'SignificantEvent_Key',
  'MethodOfAssessment_Key',
  'SignificantEvent_Key',
 'ClientCount_Key',
 'CarerAgeBand_Key',
 'StatusOfCaredForPerson_Key',
  'EmploymentStatusDesc_Key',
 'LivingStatusType_Key',
 'LivingStatusDesc_Key'
], axis = 1, inplace = True)

saltdata['Period'] = 'gregorian-interval/2018-04-01T00:00:00/P1Y'


# +
def f(x):
    if x == ':':
        return 'Data not submitted'
    elif x == '*':
        return 'Data suppressed'
    else :
        return ''

saltdata['NHS Marker'] = saltdata.apply(lambda row: f(row['ITEMVALUE']), axis = 1)
# -

saltdata['ITEMVALUE'] = pd.to_numeric(saltdata['ITEMVALUE'], errors = 'coerce')

saltdata.rename(columns= {'UUID':'SALT UUID',
 'CASSR_CODE': 'NHS Geography',
 'ITEMVALUE': 'Value',
 'DataType_Key': 'Data Type',
 'ClientType_Key': 'Client Type',
 'TableType_Key': 'Table Type',
 'AgeBand_Key': 'Age',
 'SequelToSupportRequest_Key': 'Sequel To Support Request',
 'LongTermSupportSetting_Key': 'Long Term Support Setting',
 'ShortTermPurpose_Key': 'Short Term Purpose',
 'RouteOfTransitionType_Key': 'Route Of Transition Type',
 'PrimarySupportReasonDesc_Key': 'Primary Support Reason',
 'CarerSupport_Key': 'Carer Support',
 'PrisonSupport_Key': 'Prison Support',
 'EthnicityDesc_Key': 'Ethnicity',
 'SequelToReviewType_Key': 'Sequel To ReviewType',
 'ChangeInSetting_Key': 'Change In Setting',
 'EmploymentStatusType_Key': 'Employment Status Type'}, inplace = True)

# +
# from pathlib import Path
# out = Path('out')
# out.mkdir(exist_ok=True)
# saltdata.drop_duplicates().to_csv(out / 'salt-observations.csv', index = False)

# +
# scraper.dataset.family = 'disability'
# with open(out / 'salt-observations.csv-metadata.trig', 'wb') as metadata:
#     metadata.write(scraper.generate_trig())

# +
# csvw = CSVWMetadata('https://gss-cogs.github.io/family-disability/reference/')
# csvw.create(out / 'salt-observations.csv', out / 'salt-observations.csv-schema.json')
