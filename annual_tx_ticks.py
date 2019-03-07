import cleanup_data
import datetime


class Observation:
    def __init__(self, species, date):
        self.species = species
        self.date = date


def main():
    cleanup_data.main()

    tx_county_names = []
    tx_county_names_file = open('tx_county_names.txt')
    for line in tx_county_names_file.readlines():
        tx_county_names.append(line.strip())

    tx_county_lists = {}
    for county_name in tx_county_names:
        tx_county_lists[county_name] = []

    min_date = datetime.datetime.today()
    max_date = datetime.datetime(2000, 1, 1)

    data_file = open('MyEBirdDataCleanup.csv')
    for line in data_file.readlines():
        line_elements = line.split(',')
        state = line_elements[4]
        if state == 'US-TX':
            species = line_elements[0]
            county = line_elements[5]
            # index date from back because some location names contain commas
            date_s = line_elements[len(line_elements) - 1].split('-')
            date = datetime.datetime(int(date_s[2]), int(date_s[0]), int(date_s[1]))
            if date < min_date:
                min_date = date
            if date > max_date:
                max_date = date
            tx_county_lists[county].append((species, date))

    annual_ticks = {}
    for year in range(min_date.year, max_date.year + 1, 1):
        total_year_ticks = 0
        for county in tx_county_lists.values():
            county_year_list = []
            for observation in county:
                if int(observation[1].year) == year and observation[0] not in county_year_list:
                    county_year_list.append(observation[0])

            total_year_ticks += len(county_year_list)
        annual_ticks[str(year)] = total_year_ticks

    for key in annual_ticks.keys():
        print(key, annual_ticks[key])


if __name__ == '__main__':
    main()
