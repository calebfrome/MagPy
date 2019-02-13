""" Trim bird names to full species only """
import re


def main():
    raw_file = open('MyEBirdData.csv')
    clean_file = open('EBirdDataMod.csv', 'w')
    
    raw_file.readline()
    header = 'Common Name,Scientific Name,Taxonomic Order,Count,State/Province,County,Location,Date\n'
    clean_file.write(header)
    
    for line in raw_file.readlines():
        raw_tokens = line.replace('"', '').split(',')
        final_tokens = fix_tokens(raw_tokens)
    
        # format species name
        species_name = final_tokens[0]
        
        # ignore the entry if it's not a full species (spuh, slash, hybrid)
        if '.' in species_name or '/' in species_name or 'hybrid' in species_name:
            continue

        # ignore domestic types
        elif 'Domestic' in final_tokens[1]:
            continue

        # remove parenthesis suffices(denote subspecies)
        elif '(' in species_name:
            species_name = species_name[:species_name.index('(') - 1]

        final_tokens[0] = species_name
    
        # output all 8 fields from final_tokens
        buffer = ''
        for i in range(8):
            buffer += final_tokens[i]
            if i < 7:
                buffer += ','
            else:
                buffer += '\n'

        clean_file.write(buffer)


def fix_tokens(raw_fields):
    # raw_fields contains some unknown number of fields, depending on:
    #  - the number of commas in the location name
    #  - whether the last few fields contained data in the original document

    input_fields = len(raw_fields)
    date_found = False
    temp_index = input_fields - 1
    loc_start = 7  # the index of the first part of the location field
    date = ''
    location_name = ''
    fixed_fields = []

    # copy fields 1 to 6 to start of fixed_fields (common name to county) - eliminating SID
    for i in range(1, 7):
        fixed_fields.append(raw_fields[i])

    # find the date
    fields_tested = 0
    while not date_found:
        temp = raw_fields[temp_index]
        if fields_tested > 3 and re.search('.(.?)-.(.?)-....', temp):
            date = temp
            date_found = True

        else:
            temp_index -= 1

        fields_tested += 1

    # the last part of the location is three fields ahead of the date
    loc_end = temp_index - 3  # the index of the last part of the location field

    # combine all location parts
    for i in range(loc_start, loc_end + 1):
        location_name += raw_fields[i]

    # add location and date to fixed_fields array
    fixed_fields.append(location_name)
    fixed_fields.append(date)

    return fixed_fields


if __name__ == '__main__':
    main()
