import requests
import json
import pandas as pd

def fetch_all_details(url):
    limit = 20
    skip = 0
    total_members = 660
    members_list = []

    while skip < total_members:
        response = requests.get(url + f"&skip={skip}&take={limit}")
        if response.status_code != 200:
            print("Error: Could not retrieve members from API")
        else:
            members = response.json()
            for member in members.get('items', []):
                member_details = {
                    'id': member.get('value', {}).get('id'),
                    'name': member.get('value', {}).get('nameFullTitle'),
                    'party': member.get('value', {}).get('latestParty', {}).get('name'),
                    'constituency': member.get('value', {}).get('latestHouseMembership', {}).get('membershipFrom'),
                    'start_date': member.get('value', {}).get('latestHouseMembership', {}).get('membershipStartDate', {})
                }
                members_list.append(member_details)
        skip += limit
    member_details = pd.DataFrame(members_list)
    return member_details

members_url = 'https://members-api.parliament.uk/api/Members/Search?House=1&IsCurrentMember=true'

all_details = fetch_all_details(members_url)
all_details['start_date'] = pd.to_datetime(all_details['start_date'])
all_details.to_csv('all_details.csv')