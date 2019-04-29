import datetime


class Checklist:
    def __init__(self, sid, location, county, state, date):
        self.sid = sid
        self.location = location
        self.county = county
        self.state = state
        self.date = date
        self.species_list = dict()

    def add_species(self, species_name, count):
        self.species_list[species_name] = count


def create_database(min_date=datetime.datetime(1900, 1, 1), max_date=datetime.datetime.today(), regions=None):
    data = open('MyEBirdDataCleanup.csv')
    database = dict()
    data.readline()  # truncate header
    for raw_obs in data.readlines():
        obs = raw_obs.split(',')
        sid = obs[0]
        species = obs[1]
        tax_sort = obs[3]  # TODO: incorporate
        count = obs[4]
        state = obs[5]
        county = obs[6]
        # index date from back because some location names contain commas
        date_str = obs[len(obs) - 1].rstrip('\n').split('-')
        date = datetime.datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        # determine location
        location = ''
        for i in range(7, len(obs) - 1):
            location += obs[i]

        # check date filter
        if date < min_date or date > max_date:
            continue
        # check location filter
        if regions is not None and state not in regions:
            continue

        # check if checklist already exists
        if sid in database.keys():
            database[sid].add_species(species, count)
        else:
            database[sid] = Checklist(sid, location, county, state, date)

    return database
