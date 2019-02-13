import cleanup_data


def main():
    cleanup_data.main()

    tx_county_names = []
    tx_county_names_file = open('tx_county_names.txt')
    for line in tx_county_names_file.readlines():
        tx_county_names.append(line.strip())

    county_species_map = {}
    for county_name in tx_county_names:
        county_species_map[county_name] = []

    data_file = open('EBirdDataMod.csv')
    for line in data_file.readlines():
        line_elements = line.split(',')
        state = line_elements[4]
        if state == 'US-TX':
            species = line_elements[0]
            county = line_elements[5]
            if species not in county_species_map[county]:
                county_species_map[county].append(species)

    species_county_map = {}
    for county_name in tx_county_names:
        for species in county_species_map[county_name]:
            if species not in species_county_map.keys():
                species_county_map[species] = [county_name]
            else:
                species_county_map[species].append(county_name)

    unique_county_lists = {}
    for county_name in tx_county_names:
        unique_county_lists[county_name] = []

    for species in species_county_map.keys():
        if len(species_county_map[species]) == 1:
            unique_county_lists[species_county_map[species][0]].append(species)

    total_unique_counties = 0
    total_unique_species = 0
    for county in unique_county_lists.keys():
        num_unique = len(unique_county_lists[county])
        total_unique_species += num_unique
        if num_unique == 0:
            continue
        total_unique_counties += 1
        total_list = len(county_species_map[county])
        print(county, num_unique, '/', total_list, '=', 100*num_unique/total_list, '%')
        for species in unique_county_lists[county]:
            print('\t', species)

    print(total_unique_counties)
    print(total_unique_species)


if __name__ == '__main__':
    main()
