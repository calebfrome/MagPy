from database import create_database
import datetime


def main():
    database = create_database()
    day_lists = dict()

    for checklist in database.values():
        date = format_date(checklist.date)
        if date in day_lists.keys():
            day_lists[date] = set().union(*[day_lists[date], checklist.species_list])
        else:
            day_lists[date] = checklist.species_list

    for day in sorted(day_lists.keys()):
        print(day + '\t' + str(len(day_lists[day])))


def format_date(date):
    month = str(date.month)
    if len(month) == 1:
        month = '0' + month
    day = str(date.day)
    if len(day) == 1:
        day = '0' + day
    return month + '-' + day


if __name__ == '__main__':
    main()
