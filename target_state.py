import datetime
import numpy as np
import cleanup_data
from amw import retrieve_aba_data
from database import create_database
import os


class Species:
    def __init__(self, species, aba_code, exotic, checklist):
        self.species = species
        self.num_obs = 1
        self.aba_code = int(aba_code)
        self.first_date = checklist.date
        self.last_date = checklist.date
        self.years_since = 0
        self.exotic = int(exotic)
        self.value = 0

    def add_data(self, checklist):

        # update first and last dates
        self.first_date = min(self.first_date, checklist.date)
        self.last_date = max(self.last_date, checklist.date)

        # increment num_obs
        self.num_obs += 1

    def compute_years_since(self):
        self.years_since = np.divide((datetime.datetime.today() - self.last_date).days, 365)
        return self.years_since

    def compute_value(self):
        self.value = np.divide(np.multiply(self.years_since, self.aba_code),
                               np.multiply(self.num_obs, (self.exotic + 1)))


def main():
    cleanup_data.main()
    aba_data = retrieve_aba_data()
    species_values, max_years_since = compute_species_values(aba_data)
    print('max years since:', max_years_since)
    state_values = compute_state_values(aba_data, species_values, max_years_since)
    for state in state_values.keys():
        print(state, state_values[state])


def compute_species_values(aba_data):
    database = create_database()
    species_values = dict()
    max_years_since = 0
    # aggregate data
    for checklist in database.values():
        for species in checklist.species_list:
            if species not in species_values:
                if species not in aba_data.keys():
                    continue
                aba_species_data = aba_data[species]
                species_values[species] = Species(species, aba_species_data['aba_code'], aba_species_data['exotic'], checklist)
            else:
                species_values[species].add_data(checklist)
    # compute years since
    for species in species_values.values():
        max_years_since = max(max_years_since, species.compute_years_since())
    for species in species_values.values():
        species.compute_value()
    return species_values, max_years_since


def compute_state_values(aba_data, species_values, max_years_since):
    state_values = dict()
    species_list = species_values.keys()
    for state in os.listdir('state_freqs'):
        if state == 'hi.txt':
            continue
        state_name = state[:-4]
        f = open(os.path.join('state_freqs', state))
        state_values[state_name] = 0
        for raw_line in f.readlines():
            line = raw_line.split('\t')
            species = line[0]
            freq = float(line[1].rstrip())
            if species in species_list:
                species_value = species_values[species].value
            else:
                if species not in aba_data.keys():
                    continue
                aba_species_data = aba_data[species]
                species_value = np.divide(np.multiply(max_years_since, int(aba_species_data['aba_code'])),
                                          (int(aba_species_data['exotic']) + 1))
            state_species_value = np.multiply(freq, species_value)
            if state_species_value >= 0.1:
                print(state_name, species, species_value, freq, state_species_value)
            state_values[state_name] += state_species_value

    return state_values


if __name__ == '__main__':
    main()
