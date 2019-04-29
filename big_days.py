import datetime
from database import create_database
import cleanup_data


def main():
    cleanup_data.main()
    database = create_database()
    threshold = 100
    start_date = datetime.datetime(1900, 1, 1)
    end_date = datetime.datetime.today()
    date = start_date
    while date < end_date:
        day_list = []
        for sid in database.keys():
            checklist = database[sid]
            if checklist.date == date:
                for species in checklist.species_list:
                    if species not in day_list:
                        day_list.append(species)

        if len(day_list) >= threshold:
            # TODO: fix format
            print(date, len(day_list))

        date += datetime.timedelta(days=1)


if __name__ == '__main__':
    main()