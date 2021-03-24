import datetime
from generate_lists import generate_list
import requests
import json
import sys, os
from ebird.api import get_observations

api_key = '411kkf61qc5d'
headers = {
    'X-eBirdApiToken': api_key
}
lifer_states = ['US-WI']
midwest_states = ['US-MN', 'US-WI', 'US-MI', 'US-OH', 'US-IN', 'US-IL', 'US-IA', 'US-MO']


def main():
    # ABA lifers (since 2019) seen in the last 7 days
    # species_list = generate_list(datetime.datetime(2019, 1, 1), datetime.datetime.today(), 'first', 'ABA')
    # generate_alert(lifer_states, 7, species_list)

    # Fantasy Birding alerts for the Midwest game from the last 3 days
    species_list = [line.split(',')[2] for line in open('needs_alerts\midwest_species_list.csv').readlines()][1:]
    generate_alert(midwest_states, 3, species_list)


def generate_alert(search_regions, days_back, species_list):
    alert_obs = {}
    for region in search_regions:
        recent_obs = get_most_recent_observations(region, days_back)
        for obs in recent_obs:
            species = obs['comName']
            if species not in species_list:
                if species not in alert_obs.keys():
                    alert_obs[species] = []
                alert_obs[species].extend(get_all_recent_observations(region, obs['speciesCode'], days_back))
    file = start_alert()
    for species in alert_obs.keys():
        add_alert(file, alert_obs[species])
    end_alert(file)


def get_most_recent_observations(search_region, days_back):
    url = 'https://api.ebird.org/v2/data/obs/' + search_region + '/recent?includeProvisional=true&cat=species&back=' + str(days_back)
    response = requests.request('GET', url, headers=headers, data={}, allow_redirects=False)
    return json.loads(response.text)


def get_all_recent_observations(search_region, species_code, days_back):
    url = 'https://api.ebird.org/v2/data/obs/' + search_region + '/recent/' + species_code + \
          '/?includeProvisional=true&cat=species&back=' + str(days_back)
    response = requests.request('GET', url, headers=headers, data={}, allow_redirects=False)
    return json.loads(response.text)


def start_alert():
    file = open('needs_alerts\\needs_alert.html', 'w')
    file.write('<html><head><link rel="stylesheet" href="needs_alert.css"><title>Custom Needs Alerts</title></head>'
               '<body>')
    file.write('<h3>Needs Alerts for ' + datetime.datetime.today().strftime('%B %d') + '</h3>')
    file.write('<p><em>The following are species still needed for your list that have been reported recently.'
               'Birds reported in the past 24 hours are shown with red dates. Click the species names '
               'to view sightings on the eBird map. Click the location names to see the checklists.</em></p>')
    file.write('<ul>')
    return file


def add_alert(file, obs_list, max_obs=10):
    file.write('<li>' + '<a class="bold" href=' + ebird_map_url(obs_list[0]['speciesCode']) + '>'
               + obs_list[0]['comName'] + '</a><ul>')
    count = 0
    for obs in obs_list:
        count += 1
        if count > max_obs:
            break
        date_time_obj = try_parsing_date(obs['obsDt'])
        file.write('<li><span')
        timedelta = datetime.datetime.now() - date_time_obj
        if timedelta.total_seconds() < 86400:
            file.write(' style="color:red;"')
        else:
            file.write(' style="color:#36316b;"')
        file.write('>' + date_time_obj.strftime('%b %d') + '</span>: <a href=' + ebird_checklist_url(obs['subId']) + '>'
                   + obs['locName'] + '</a></li>')
    file.write('</ul></li>')


def end_alert(file):
    file.write('</ul></body></html>')
    file.close()


def ebird_map_url(species_code):
    url = 'https://ebird.org/map/{species}?env.minX=-97.8&env.minY=36.2&env.maxX=-80&env.maxY=49.3&gp=true' \
          '&yr=cur&mr=on&bmo=3&emo=5'
    return url.format(species=species_code)


def ebird_checklist_url(checklist_id):
    return 'https://ebird.org/checklist/' + checklist_id


def lookup_county(lat, lon):
    return requests.request('GET', 'https://geo.fcc.gov/api/census/area?lat=' + lat + '&lon=' + lon + '&format=json').text


def try_parsing_date(text):
    for fmt in ('%Y-%m-%d %H:%M', '%Y-%m-%d'):
        try:
            return datetime.datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if __name__ == '__main__':
    main()
