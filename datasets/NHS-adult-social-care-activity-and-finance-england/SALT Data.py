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

saltdata['Period'] = 'gregorian-interval/' + (saltdata['FY_Ending']-1).astype(str) + '-04-01T00:00:00/P1Y'

saltdata.drop(
['GEOGRAPHY_LEVEL',
'SHEET',
'TABLE',
'ADDITIONAL_CELLS',
'DATA_LEVEL',
'FY_Ending',
'UUID',
'GEOGRAPHY_CODE',
'DH_GEOGRAPHY_NAME',
'REGION_GO_CODE',
'GEOGRAPHY_NAME',
'AgeAtAssessment_Key',
'AgeAtTransition_Key',
'DataType_Key',
'DischargeStatus_Key'
], axis = 1, inplace = True)

saltdata[saltdata.columns.difference(['ITEMVALUE'])] = saltdata[saltdata.columns.difference(['ITEMVALUE'])].fillna('all')

saltdata[saltdata.columns.difference(['ITEMVALUE'])] = saltdata[saltdata.columns.difference(['ITEMVALUE'])]\
                                                            .replace('99','Total')        

saltdata[saltdata.columns.difference(['ITEMVALUE'])] = saltdata[saltdata.columns.difference(['ITEMVALUE'])]\
                                                            .replace(99.0,'Total')        


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

saltdata.rename(columns= {
'CASSR_CODE':'NHS Geography',
'ItemValue':'Value',
'AgeBand_Key':'Age',
'CarerAgeBand_Key':'Carer Age Band',
'CarerSupport_Key':'Carer Support',
'CarerType_Key':'Carer Type',
'ChangeInSetting_Key':'Change In Setting',
'ClientCount_Key':'Client Count',
'ClientType_Key':'Client Type',
'CommunitySupport_Key':'Community Support',
'EmploymentStatusDesc_Key':'Employment Status',
'EmploymentStatusType_Key':'Employment Status Type',
'EthnicityDesc_Key':'Ethnicity',
'EthnicityGrouping_Key':'Ethnicity Group',
'Gender_Key':'Sex',
'LivingStatusDesc_Key':'Living Status',
'LivingStatusType_Key':'Living Status',
'LongTermPeriod_Key':'Long Term Period',
'LongTermSupportSetting_Key':'Long Term Support Setting',
'MethodOfAssessment_Key':'Method Of Assessment',
'NoChangeInSetting_Key':'No Change In Setting',
'NoServicesProvided_Key':'No Services Provided',
'PrimarySupportReason_Key':'Primary Support Reason',
'PrimarySupportReasonDesc_Key':'Primary Support Reason',
'PrisonSupport_Key':'Prison Support',
'ReportedHealthCondDesc_Key':'Reported Health Condition',
'ReportedHealthCondGroup_Key':'Reported Health Conditon Group',
'ReviewType_Key':'Review Type',
'RouteOfAccess_Key':'Route Of Access',
'RouteOfTransitionDesc_Key':'Route Of Transition',
'RouteOfTransitionType_Key': 'Route Of Transition Type',
'SequelToReviewType_Key': 'Sequel To Review Type',
'SequelToSTMax_Key':'Sequel To STMax',
'SequelToSupportRequest_Key': 'Sequel To Support Request',
'ShortTermPeriod_Key':'Short Term Period',
'ShortTermPurpose_Key':'Short Term Purpose',
'SignificantEvent_Key':'Significant Event',
'StatusOfCaredForPerson_Key':'Status Of Cared For Person',
'SupportToCarerDesc_Key':'Support To Carer',
'SupportToCarerType_Key':'Support To Carer Type',
'TableType_Key':'Table Type'}, inplace = True)

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
# -


