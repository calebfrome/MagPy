import datetime
import numpy as np
from database import create_database


class AMWSpecies:
    def __init__(self, species, aba_code, exotic, checklist):
        self.species = species
        self.num_obs = 1
        self.aba_code = aba_code
        self.loc_code = lookup_loc_code(checklist.county, checklist.state)
        self.first_date = checklist.date
        self.last_date = checklist.date
        self.years_since = 0
        self.exotic = exotic
        self.amw = 0

    def add_data(self, checklist):
        # update location code
        new_loc_code = lookup_loc_code(checklist.county, checklist.state)
        if new_loc_code < self.loc_code:
            self.loc_code = new_loc_code

        # update first and last dates
        self.first_date = min(self.first_date, checklist.date)
        self.last_date = max(self.last_date, checklist.date)

        # increment num_obs
        self.num_obs += 1

    def final_calc(self):
        # years since
        self.years_since = 1 + np.floor_divide((datetime.datetime.today() - self.last_date).days, 365)

        # AMW
        self.amw = self.num_obs * (1 + int(self.exotic)) / (int(self.years_since) * (1 + int(self.aba_code) + int(self.loc_code)))


def main():
    # setup
    aba_data = retrieve_aba_data()
    database = create_database()
    amw = dict()
    # compute
    for checklist in database.values():
        for species in checklist.species_list:
            if species not in amw:
                if species not in aba_data.keys():
                    continue
                aba_species_data = aba_data[species]
                amw[species] = AMWSpecies(species, aba_species_data['aba_code'], aba_species_data['exotic'], checklist)
            else:
                amw[species].add_data(checklist)
    for species in amw.values():
        species.final_calc()

    # output
    # amw_sorted = amw  # todo
    amw_out = open('amw.csv', 'w')
    amw_out.write('Species,AMW,ABA Code,Observations,First Seen,Last Seen,Years Since,Loc Code\n')
    for a in amw.values():
        amw_row = a.species + ',' + str(a.amw) + ',' + str(a.aba_code) + ',' + str(a.num_obs) + ',' + str(a.first_date)\
                  + ',' + str(a.last_date) + ',' + str(a.years_since) + ',' + str(a.loc_code) + '\n'
        amw_out.write(amw_row)


def retrieve_aba_data():
    aba_data = dict()
    aba_file = open('aba_checklist.csv', 'r')
    for line in aba_file.readlines():
        raw_data = line.split(',')
        aba_data[raw_data[0]] = {'aba_code': raw_data[1], 'exotic': raw_data[2]}
    return aba_data


def lookup_loc_code(county, state):
    # counties lived in
    if county == 'Collin' and state == 'US-TX':
        return 1
    elif county == 'Cleveland' and state == 'US-OK':
        return 1
    elif county == 'Dane' and state == 'US-WI':
        return 1
    # states lived in
    elif state in ['US-TX', 'US-OK', 'US-WI']:
        return 2
    # states within a day's drive / often visited
    elif state in ['US-NM', 'US-CO', 'US-AZ', 'US-ND', 'US-SD', 'US-NE', 'US-MO', 'US-KS', 'US-IA', 'US-MN',
                   'US-MI', 'US-IL', 'US-IN', 'US-KY', 'US-OH', 'US-MS', 'US-TN', 'US-AR', 'US-LA']:
        return 3
    # Alaska, Hawaii, Canada
    elif state in ['US-AK', 'US-HI'] or state[:2] == 'CA':
        return 5
    # international
    elif state[:2] not in ['US', 'CA']:
        return 6
    # all other US states (long drive / infrequent visits)
    else:
        return 4


if __name__ == '__main__':
    main()
