
def main():
    total_time = 0
    checklists_counted = []
    data_file = open('MyEBirdData.csv')
    data_file.readline()  # truncate header
    for line in data_file.readlines():
        line_elements = line.split(',')
        if line_elements[0] not in checklists_counted:
            # find protocol column
            column = 12
            while line_elements[column][0:5] != 'eBird':
                column += 1

            checklists_counted.append(line_elements[0])
            if line_elements[column + 1] != '':
                total_time += int(line_elements[column + 1])

    print(total_time, 'minutes =', total_time/60, 'hours')
    print(len(checklists_counted), 'checklists')


if __name__ == '__main__':
    main()
