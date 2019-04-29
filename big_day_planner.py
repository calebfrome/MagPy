import os
import numpy as np

scale_factor = 4/3
show_full_results = False
compare_routes = True


route_ctx_ctc_rgv = [
    'mitchell_lake_area',
    'port_aransas_area',
    'king_ranch_norias_area',
    'estero_area',
    # 'old_port_isabel_rd_area',
    'santa_ana_area',
    'spi_area',
]

route_ctx_utc = [
    'anahuac_area',
    'high_island_area',
    'bolivar_flats_area',
    'mitchell_lake_area',
    'south_llano_area'
]

route_ctx_ctc_utc = [
    'anahuac_area',
    'high_island_area',
    # 'bolivar_flats_area',
    # 'hazel_pollywog_area',
    'mitchell_lake_area',
    'south_llano_area'
]

route_utc = [
    'anahuac_area',
    'high_island_area',
    'rollover_pass_area',
    'bolivar_flats_area',
    'galveston_island_area',
    'brazoria_area',
    'quintana_area',
    'san_bernard_area'
]

route_compare_rgv_ctc_v1 = [
    # 'aransas_nwr_area',
    'bentsen_area',
    'estero_area',
    'goose_island_area',
    # 'hazel_pollywog_area',
    'king_ranch_norias_area',
    # 'laguna_atascosa_area',
    # 'old_port_isabel_rd_area',
    'port_aransas_area',
    'santa_ana_area',
    'spi_area']

route_rgv_ctc_v2 = [
    'aransas_nwr_area',
    'bentsen_area',
    'estero_area',
    'goose_island_area',
    'hazel_pollywog_area',
    # 'king_ranch_norias_area',
    # 'laguna_atascosa_area',
    # 'old_port_isabel_rd_area',
    # 'port_aransas_area',
    'santa_ana_area',
    'spi_area']


def main():
    route = route_ctx_ctc_rgv
    route_compare = route_ctx_utc

    # week_index is 1-indexed
    week_index = 13

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
    expected_species_values = dict()
    for region in route:
        if show_full_results:
            print(region)
        for location in os.listdir('big_day_bar_charts/' + region):
            with open('big_day_bar_charts/' + region + '/' + location) as datafile:
                # discard first 15 lines
                for i in range(15):
                    datafile.readline()
                # process species data
                for buffer in datafile.readlines():
                    species_data = buffer.rstrip().split('\t')
                    species_name = species_data[0]
                    parsed_name = parse_name(species_name)
                    if parsed_name == '':
                        continue
                    if parsed_name not in expected_species_values.keys():
                        expected_species_values[parsed_name] = [float(species_data[week_index])]
                    else:
                        expected_species_values[parsed_name].append(float(species_data[week_index]))
                        
    expected_species = dict()
    for species in expected_species_values.keys():
        expected_species[species] = expectation(expected_species_values[species])

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


def expectation(frequency_values):
    x = 1
    for freq in frequency_values:
        x *= (1 - freq)
    return (1 - x) * scale_factor


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
