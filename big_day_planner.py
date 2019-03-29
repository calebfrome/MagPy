locations = ['aransas_nwr_area',
             'bentsen_area',
             'estero_area',
            # 'goose_island_area',
            # 'hazel_pollywog_area',
             'laguna_atascosa_area',
             'port_aransas_area',
            # 'salineno_area',
             'santa_ana_area',
             'spi_area']


def main():
    # week_index is 1-indexed!
    week_index = 13  # first week in April
    species_freqs = dict()
    for loc in locations:
        print(loc)
        with open('big_day_bar_charts/' + loc + '.txt') as datafile:
            # discard first 16 lines
            for i in range(16):
                datafile.readline()
            for buffer in datafile.readlines():
                species_data = buffer.rstrip().split('\t')
                species_name = species_data[0]
                parsed_name = parse_name(species_name)
                if parsed_name == '':
                    continue
                # if parsed_name == 'House Sparrow':
                #    print('debug')
                # print(parsed_name)
                if parsed_name not in species_freqs.keys():
                    species_freqs[parsed_name] = [species_data[week_index]]
                else:
                    species_freqs[parsed_name].append(species_data[week_index])

    species_odds = []
    for species in species_freqs.keys():
        species_odds.append((species, combine_probabilities(species_freqs[species])))
    output(sorted(species_odds, key=lambda x: x[1], reverse=True))


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


def combine_probabilities(probs_list):
    prob_not = 1
    for prob in probs_list:
        prob_not *= (1 - float(prob))
    return 1 - prob_not


def output(species_odds):
    expected = 0
    counter = 1
    for species in species_odds:
        if species[1] == 0:
            break
        expected += species[1]
        print(counter, '  \t', species[1], '  \t', species[0])
        counter += 1
    print('expected:', expected)


if __name__ == '__main__':
    main()
