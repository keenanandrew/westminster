import requests
import json
import pandas as pd
import datetime

# A function that fetches basic data about MPs from the API
# and exports it to a CSV file
# which is then added to the repo, with today's date, by a GitHub Action

def fetch_all_details(url):
    limit = 20 # because the API limits requests to 20 MPs at a time
    skip = 0
    total_members = 660 # closest multiple of 20 that is greater than the total number of MPs
    members_list = []

    while skip < total_members:
        response = requests.get(url + f"&skip={skip}&take={limit}")
        if response.status_code != 200:
            print("Error: Could not retrieve members from API")
        else:
            members = response.json()
            for member in members.get('items', []):
                member_details = {
                    'id': member.get('value', {}).get('id'),  # extracts ID of the MP
                    'name': member.get('value', {}).get('nameFullTitle'),   # extracts full name & title of the MP
                    'party': member.get('value', {}).get('latestParty', {}).get('name'), # extracts MP's current party
                    'constituency': member.get('value', {}).get('latestHouseMembership', {}).get('membershipFrom'), # extracts MP's current constituency
                    'start_date': member.get('value', {}).get('latestHouseMembership', {}).get('membershipStartDate', {}) # extracts date they started in Parliament
                }
                members_list.append(member_details)
        skip += limit
    member_details = pd.DataFrame(members_list)
    return member_details

members_url = 'https://members-api.parliament.uk/api/Members/Search?House=1&IsCurrentMember=true'

# the actual function call
all_details = fetch_all_details(members_url)

# converts the date to a datetime object - may be undone by the csv write
all_details['start_date'] = pd.to_datetime(all_details['start_date'])

today = datetime.datetime.now().strftime("%Y-%m-%d")

# exports the df as a CSV with today's date
all_details.to_csv(f'all_details_{today}.csv')
