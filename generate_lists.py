from database import create_database, Checklist


class ListItem:
    def __init__(self, checklist: Checklist):
        self.location = checklist.location
        self.county = checklist.county
        self.state = checklist.state
        self.date = checklist.date


def generate_list(start_date, end_date, list_type='first', regions=None):
    database = create_database(start_date, end_date, regions)
    species_list = {}
    for checklist in database.values():
        for species in checklist.species_list:
            if species not in species_list:
                species_list[species] = ListItem(checklist)
                continue
            if list_type == 'first':
                if checklist.date < species_list[species].date:
                    species_list[species] = ListItem(checklist)
            if list_type == 'last':
                if checklist.date > species_list[species].date:
                    species_list[species] = ListItem(checklist)
    return species_list
