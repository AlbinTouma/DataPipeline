import requests
import json
import pandas as pd
from datetime import date
import xml.sax


base_url = 'http://data.niassembly.gov.uk/'
return_format = 'members_json.ashx?m='


def api_call(query):

    headers = {'Content-Type': 'application/json; charset=utf-8'}
    response = requests.get(
        f'{base_url}{return_format}{query}', headers=headers)
    dictionary = response.json()

    return dictionary


allMLA = api_call('GetAllMembers')
onlyServingMLA = api_call('GetAllCurrentMembers')
contactDetails = api_call('GetAllMemberContactDetails')
allMembersRoles = api_call('GetAllMemberRoles')

# We need to flatten the nested JSONs
# Example DataFrames
allMLA = pd.json_normalize(allMLA['AllMembersList']['Member'])
onlyServingMLA = pd.json_normalize(onlyServingMLA['AllMembersList']['Member'])
onlyServingMLA['Status'] = 'Active'
contactDetails = pd.json_normalize(contactDetails['AllMembersList']['Member'])
allMembersRoles = pd.json_normalize(allMembersRoles['AllMembersRoles']['Role'])


merged = pd.merge(allMLA, onlyServingMLA, on=['PersonId', 'MemberName', 'MemberLastName', 'MemberFirstName', 'MemberFullDisplayName',
                  'MemberSortName', 'MemberTitle', 'PartyName', 'PartyOrganisationId', 'ConstituencyName', 'ConstituencyId', 'MemberImgUrl', 'MemberPrefix'], how='outer')
merged = pd.merge(merged, contactDetails, on='PersonId', how='outer')
merged = pd.merge(merged, allMembersRoles, on=[
                  'PersonId', 'MemberFullDisplayName'], how='outer')
merged = merged.groupby('PersonId').apply(
    lambda x: x.to_dict(orient='records')).tolist()

print(merged)


quit()
# result_dict = merged.groupby('PersonId').apply(lambda x: x.to_dict(orient='records')).tolist()

# merged = pd.merge(merged, allMembersRoles, on=merge_on, how='outer')
# grouped = merged.groupby('PersonId').apply(lambda x: x.to_dict(orient='records')).reset_index(drop=True)

# Group by 'PersonId' and convert roles to arrays

# Convert the grouped data to a dictionary


# Save the dictionary as a JSON file

with open('./Northern Ireland Assembly/MLA.json', 'w') as f:
    json.dump(result_dict, f, indent=4)

# allMLA = pd.DataFrame(allMLA)

# print(json.dumps(onlyServingMLA, indent=5))

"""
There is no way to distinguish between previous and present in response.
We'll ave to merge current members with historical members. 
We can merge contact details on personID and MemberName


The reason we get duplicate entries is because Member Role creates new entries when it should be array. 

Keys for incHistoricalMLA: 
    "PersonID:              int =>  unique id,
    MemberName:            str =>  first_name, last_name,
    MemberLastName          str =>  last name, 
    MemberFirstName"       str =>  first_name,
    MemberFullDisplayName   str =>  Prefix first_name last name,
    MemberSortName          str =>  LastNameFirstName
    MemberTitle             str =>  MLA - constituency_name
    PartyName               str =>  Name of party Sinn F\u00009ein                ! utf is not supported
    PartyOrganisationID     int =>  id representation of party
    ConstituencyName        str =>  constituency_name
    ConstituencyID          int =>  id representation of constituency
    MemberImgURL            url =>  'https://aims.niassembly.gov.uk/images/mla/2_s.jpg

Keys for CurrentMLA:
    PersonID                int =>  Unique id
    AffiliationId           int =>  Unique id of affiliation ?
    MemberLastName          str =>  Surname
    MemberFirstName         str =>  First name
    MemberFullDisplayName   str =>  prefix first name surname
    MemberSortName          str =>  SurnameFirstName
    MemberTitle             str =>  MLA Upper Bann
    PartyName               str =>  Name of Party
    PartyOrganisationID     str =>  Id of organisation
    ConstituencyName        str =>  Name of constituency
    ConstituencyID          int =>  id of constituency
    MemberImgUrl            url =>  Image of MLA
    MemberPrefix            str =>  Mr, Mrs, Miss


Keys for contactDetails
    AddressID               int =>  identifies address
    PersonID                int =>  identifies MLA
    AddressType             str =>  type of address ie NIA Constituency Address
    Townland                str =>  Municipality ? Not sure Ballynainch
    TownCity                str =>  City where located
    Postcode                str =>  Post code
    TelephoneNumber         int =>  Phone number
    EmaiAddress            str =>  email address (key is missing l in email)
    Latitude:               str =>  latitude
    Longitude               str =>  Longitude
    locTypeID               int =>  unique identifier of address

Keys for AllMemberRoles
    PersonID                int =>   unique identifyer of person
    AffiliationID           int =>   unique identifyer of affilation. Not sure what this is
    MemberFullDisplayNmae   str =>   Prefix and Full Name
    Role                    str =>   ie MLA
    OrganisationId          int =>   unique id of organisation ie Northern Ireland Assembly
    Organisation            str =>   Name of Organisation ie Northern Ireland Assembly
    AffiliationStart        date =>  Date when started  2022-05-05T18:40:00+00:00
    AffiliationTitle        str =>   Title ie MLA - Mid Ulster
    """
