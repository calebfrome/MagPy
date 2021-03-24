import sys, os
import datetime
import requests
import json
import configparser

api_key = '411kkf61qc5d'
headers = {
    'X-eBirdApiToken': api_key
}


def main():
    config = configparser.ConfigParser()
    config.read(resource_path('config.ini'))
    lat = config.getfloat('circle', 'latitude')
    lon = config.getfloat('circle', 'longitude')
    radius = config.getfloat('circle', 'radius_km')
    days_back = config.getint('settings', 'days')
    max_obs = config.getint('settings', 'max')
    generate_alert(lat, lon, radius, days_back, max_obs)


def generate_alert(lat, lon, radius_km, days_back, max_obs):
    file = start_alert()
    species_list_file = open(resource_path('species_list.txt'))
    species_list = species_list_file.readlines()
    species_list = [s.strip() for s in species_list]
    recent_obs = get_recent_obs(lat, lon, radius_km, days_back)
    for obs in recent_obs:
        if obs['comName'] not in species_list:
            species_obs = get_recent_species_obs(obs['speciesCode'], lat, lon, radius_km, days_back)
            add_alert(file, species_obs, lat, lon, max_obs)
    end_alert(file)


def get_recent_obs(lat, lon, radius_km, days_back):
    url = 'https://api.ebird.org/v2/data/obs/geo/recent?lat=' + str(lat) + '&lng=' + str(lon) + '&dist=' + \
          str(radius_km) + '&includeProvisional=true&cat=species&sort=species&back=' + str(days_back)
    response = requests.request('GET', url, headers=headers, data={}, allow_redirects=False)
    return json.loads(response.text)


def get_recent_species_obs(species, lat, lon, radius_km, days_back):
    url = 'https://api.ebird.org/v2/data/obs/geo/recent/' + species + '?lat=' + str(lat) + '&lng=' + str(lon) + \
          '&dist=' + str(radius_km) + '&includeProvisional=true&cat=species&sort=species&back=' + str(days_back)
    response = requests.request('GET', url, headers=headers, data={}, allow_redirects=False)
    return json.loads(response.text)


def start_alert():
    file = open(resource_path('needs_alert.html'), 'w')
    file.write('<html><head><link rel="stylesheet" href="needs_alert.css"><title>YardSquad Needs Alerts</title></head>'
               '<body>')
    file.write('<h3>YardSquad Needs Alerts for ' + datetime.datetime.today().strftime('%B %d') + '</h3>')
    file.write('<p><em>The following are species still needed for your YardSquad circle that have been reported '
               'recently. Birds reported in the past 24 hours are shown with red dates. Click the species names '
               'to view sightings on the eBird map. Click the location names to see the checklists.</em></p>')
    file.write('<ul>')
    return file


def add_alert(file, obs_list, lat, lon, max_obs):
    file.write('<li>' + '<a class="bold" href=' + ebird_map_url(obs_list[0]['speciesCode'], lat, lon) + '>'
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


def ebird_map_url(species_code, lat, lon):
    url = 'https://ebird.org/map/{species}?env.minX={minX}&env.minY={minY}&env.maxX={maxX}&env.maxY={maxY}&gp=true' \
          '&yr=cur&mr=on&bmo=3&emo=5'
    offset = 0.1
    return url.format(species=species_code, minX=lon-offset, minY=lat-offset, maxX=lon+offset, maxY=lat+offset)


def ebird_checklist_url(checklist_id):
    return 'https://ebird.org/checklist/' + checklist_id


def end_alert(file):
    file.write('</ul></body></html>')


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
