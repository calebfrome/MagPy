import datetime
from generate_lists import generate_list
import requests
import json
from ebird.api import get_observations

api_key = '411kkf61qc5d'
headers = {
    'X-eBirdApiToken': api_key
}
local_states = ['US-WI']


def main():
    generate_alert(local_states, 'ABA', 3)


def generate_alert(search_regions, list_regions, days_back):
    aba_list = generate_list(datetime.datetime(2019, 1, 1), datetime.datetime.today(), 'first', 'ABA')
    print(aba_list)
    recent_obs = get_most_recent_observations('US-WI-025', days_back)
    for obs in recent_obs:
        if obs['comName'] not in aba_list:
            all_recent_obs = get_all_recent_observations('US-WI-025', obs['speciesCode'], days_back)
            print(all_recent_obs[0]['comName'])
            for obs2 in all_recent_obs:
                print(obs2['locName'] + '\t\t' + obs2['obsDt'])


def get_most_recent_observations(search_region, days_back):
    url = 'https://api.ebird.org/v2/data/obs/' + search_region + '/recent?includeProvisional=true&cat=species&back=' + str(days_back)
    response = requests.request('GET', url, headers=headers, data={}, allow_redirects=False)
    return json.loads(response.text)


def get_all_recent_observations(search_region, speciesCode, days_back):
    url = 'https://api.ebird.org/v2/data/obs/' + search_region + '/recent/' + speciesCode + \
          '/?includeProvisional=true&cat=species&back=' + str(days_back)
    response = requests.request('GET', url, headers=headers, data={}, allow_redirects=False)
    return json.loads(response.text)


def lookup_county(lat, lon):
    return requests.request('GET', 'https://geo.fcc.gov/api/census/area?lat=' + lat + '&lon=' + lon + '&format=json').text


if __name__ == '__main__':
    main()
