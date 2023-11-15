
import requests
import json
import pandas as pd

def fetch_members(url):
    limit = 20
    skip = 0
    total_members = 660
    names_list = []

    while skip < total_members:
        response = requests.get(url + f"&skip={skip}&take={limit}")
        if response.status_code != 200:
            print("Error: Could not retrieve names from API")
        else:
            names = response.json()
            for item in names.get('items', []):
                names_list.append(item.get('value', {}).get ('nameFullTitle'))
        skip += limit
    return names_list


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
                members_list.append(member)
        skip += limit
    member_details = pd.DataFrame(members_list)
    return member_details

members_url = 'https://members-api.parliament.uk/api/Members/Search?House=1&IsCurrentMember=true'

all_details = fetch_all_details(members_url)
print(all_details)


