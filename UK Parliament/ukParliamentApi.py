import requests
import json
import pandas as pd

base_url = 'https://members-api.parliament.uk/api/Members/Search'
skip = 0
take = 20
total_entries = 1400
all_members = []


while skip < total_entries:
    # Make a request to the API with the current skip value
    url = f'{base_url}?skip={skip}&take={take}'
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            members = data['items']

            # Append the retrieved members to the list
            all_members.extend(members)

            # Update the skip value for the next request
            skip += take
        except (json.JSONDecodeError, KeyError) as e:
            print("Error parsing JSON:", str(e))
            break
    else:
        print("Error fetching data. Status code:", response.status_code)
        break

# Creating empty lists to store the extracted data
id = []
names = []
parties = []
memberships = []
start_dates = []
end_dates = []
statuses = []
status_description = []
house = []  # Commons or Lords

# Extracting data for each member
for member in all_members:
    try:
        id.append(member['value']['id'])
    except:
        id.append('')
    try:
        names.append(member['value']['nameDisplayAs'])
    except:
        names.append('')
    try:
        parties.append(member['value']['latestParty']['name'])
    except:
        parties.append('')
    try:
        memberships.append(
            member['value']['latestHouseMembership']['membershipFrom'])
    except:
        memberships.append('')
    try:
        start_dates.append(
            member['value']['latestHouseMembership']['membershipStartDate'])
    except:
        start_dates.append('')
    try:
        end_dates.append(
            member['value']['latestHouseMembership']['membershipEndDate'])
    except:
        end_dates.append('')
    try:
        statuses.append(member['value']['latestHouseMembership']
                        ['membershipStatus']['statusIsActive'])
    except:
        statuses.append('')

    try:
        status_description.append(
            member['value']['latestHouseMembership']['membershipStatus']['statusDescription'])
    except:
        status_description.append('')

    try:
        house.append(member['value']['latestHouseMembership']['house'])
    except:
        house.append('')

# Creating a DataFrame using the extracted data
df = pd.DataFrame({
    'entity_id': id,
    "Name": names,
    "Party": parties,
    "Membership": memberships,
    "start_date": start_dates,
    "end_date": end_dates,
    "active": statuses,
    'status_description': status_description,
    'house': house

})


df.to_csv('./UK Parliament/parliamentarians.csv')

print(df)
