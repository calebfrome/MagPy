import os
import numpy as np

show_full_results = False
compare_routes = True

route = [
    # 'aransas_nwr_area',
    'bentsen_area',
    'estero_area',
    'goose_island_area',
    # 'hazel_pollywog_area',
    'king_ranch_norias_area',
    # 'laguna_atascosa_area',
    # 'old_port_isabel_rd_area',
    'port_aransas_area',
    # 'salineno_area',
    'santa_ana_area',
    'spi_area']

route_compare = [
    # 'aransas_nwr_area',
    'bentsen_area',
    'estero_area',
    'goose_island_area',
    # 'hazel_pollywog_area',
    #'king_ranch_norias_area',
    # 'laguna_atascosa_area',
    'old_port_isabel_rd_area',
    'port_aransas_area',
    #'salineno_area',
    'santa_ana_area',
    'spi_area']


def main():
    # week_index is 1-indexed
    week_index = 14

    # analyze first route
    expected_species = create_expectations(route, week_index)
    species_tuples = []
    for species in expected_species.keys():
        species_tuples.append((species, min(1.0, expected_species[species])))
    output(sorted(species_tuples, key=lambda x: x[1], reverse=True))

    if compare_routes:
        # analyze second route
        expected_species_2 = create_expectations(route_compare, week_index)
        species_tuples_2 = []
        compare_tuples = []
        for species in expected_species_2.keys():
            species_tuples_2.append((species, min(1.0, expected_species_2[species])))
            if species in expected_species.keys():
                compare_value = min(1.0, expected_species[species]) - min(1.0, expected_species_2[species])
            else:
                compare_value = - min(1.0, expected_species_2[species])
            compare_tuples.append((species, compare_value))

        for species in expected_species.keys():
            if species not in expected_species_2.keys():
                compare_tuples.append((species, min(1.0, expected_species[species])))

        output(sorted(species_tuples_2, key=lambda x: x[1], reverse=True))

        # compare routes
        for species in sorted(compare_tuples, key=lambda x:x[1], reverse=True):
            if species[1] != 0:
                print(species[0], '\t', species[1])


def create_expectations(route, week_index):
    expected_species = dict()
    for region in route:
        if show_full_results:
            print(region)
        for location in os.listdir('big_day_bar_charts/' + region):
            with open('big_day_bar_charts/' + region + '/' + location) as datafile:
                # discard first 14 lines
                for i in range(14):
                    datafile.readline()
                # get number of expected checklists from line 15
                expected_lists = max(np.ceil(float(datafile.readline().split('\t')[week_index]) / 70), 1.0)
                if show_full_results:
                    print('\t', location, expected_lists)
                # process species data
                for buffer in datafile.readlines():
                    species_data = buffer.rstrip().split('\t')
                    species_name = species_data[0]
                    parsed_name = parse_name(species_name)
                    if parsed_name == '':
                        continue
                    if parsed_name not in expected_species.keys():
                        expected_species[parsed_name] = expectation(float(species_data[week_index]), expected_lists)
                    else:
                        expected_species[parsed_name] += expectation(float(species_data[week_index]), expected_lists)

    return expected_species


def parse_name(species_name):
    parsed_name = species_name

    # ignore the entry if it's not a full species (spuh, hybrid)
    if '.' in species_name or 'hybrid' in species_name:
        return ''

    # ignore domestic types
    elif 'Domestic' in species_name:
        return ''

    # remove parenthesis suffices(denote subspecies)
    elif '(' in species_name:
        parsed_name = species_name[:species_name.index('(') - 1]

    # if the entry still contains a slash, it's not a full species
    if '/' in parsed_name:
        return ''

    return parsed_name


def expectation(frequency, expected_lists):
    return 1 - ((1 - frequency) ** expected_lists)


def output(exp_species):
    expected = 0
    counter = 1
    for species in exp_species:
        if species[1] == 0:
            break
        expected += species[1]
        if show_full_results:
            print(counter, '  \t', species[1], '  \t', species[0])
        counter += 1
    print('expected:', expected)


if __name__ == '__main__':
    main()
