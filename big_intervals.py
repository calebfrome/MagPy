import datetime
from database import create_database
import cleanup_data
# import matplotlib.pyplot as plt


# TODO: use queue
# TODO: plot trends
def main():
    cleanup_data.main()
    database = create_database()
    threshold = 550
    interval = 365
    start_date = datetime.datetime(2013, 1, 1)
    end_date = datetime.datetime.today() - datetime.timedelta(days=interval)
    date = start_date
    while date < end_date:
        interval_list = []
        for sid in database.keys():
            checklist = database[sid]
            if checklist.state[:2] != 'US' and checklist.state[:2] != 'CA':
                continue
            if date <= checklist.date < (date + datetime.timedelta(days=interval)):
                for species in checklist.species_list:
                    if species not in interval_list:
                        interval_list.append(species)

        if len(interval_list) >= threshold:
            print(date, len(interval_list))

        date += datetime.timedelta(days=1)


if __name__ == '__main__':
    main()
