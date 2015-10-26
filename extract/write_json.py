import sqlite3
import csv
import json


def import_iso_to_name_maps():
    iso_map = import_name_to_iso_map_from_file('../data/ISO_mapping.csv')
    additional_map = import_name_to_iso_map_from_file('../data/additional_countries.csv')
    iso_map.update(additional_map)
    return iso_map


def import_iso_to_name_map_from_file(filename):
    this_map = dict()
    with open(filename, 'rt') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            this_map[row['Code']] = row['Name']

    return this_map


def import_name_to_iso_map_from_file(filename):
    this_map = dict()
    with open(filename, 'rt') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            this_map[row['Name']] = row['Code']

    return this_map


def import_iso_changes_from_file(filename):
    change_map = dict()
    with open(filename, 'rt') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            change_map[(row['Year'], row['ID'])] = (row['Application_Code'], row['Impact_Code'])

    return change_map


def import_deletes(filename):
    delete_set = set()
    with open(filename, 'rt') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            delete_set.add((row['Year'], row['ID']))

    return delete_set


def dict_factory(cursor, row):
    d = dict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_year_data(year):
    y = (year,)
    with sqlite3.connect('../source_data/un_women_data.sqlite') as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute('SELECT * FROM un_women WHERE year=?', y)
        data = c.fetchall()
    return data


def get_country_code(country_name, iso_map):
    try:
        country_code = iso_map[country_name]
    except KeyError:
        print('Unknown country name: {}'.format(country_name))
        country_code = ''

    return country_code


def get_country_name(country_code, name_map):
    try:
        country_name = name_map[country_code]
    except KeyError:
        country_name = ''

    return country_name



def transform_data(input_data, iso_map, name_map, delete_set):
    output = list()
    for row in input_data:
        out_row = dict()
        out_row['project_details_other'] = row['other_details']
        out_row['project_id'] = row['application_id']
        out_row['project_summary'] = row['summary']
        out_row['project_name'] = row['project_name']
        out_row['sectors'] = row['sector'].replace(', ', ',').split(',')

        country_name = row['project_location_2'].strip()
        country_code = get_country_code(country_name, iso_map)
        if country_code:
            clean_country_name = name_map[country_code]
        else:
            clean_country_name = country_name

        out_row['country_application_name'] = clean_country_name
        out_row['country_impact_name'] = clean_country_name
        out_row['country_application'] = country_code
        out_row['country_impact'] = country_code
        out_row['project_details'] = row['project_details']
        out_row['project_year'] = row['year']

        if (out_row['project_year'], out_row['project_id']) not in delete_set:
            output.append(out_row)
        else:
            with open('../data/out.log', 'at') as a:
                a.write('(Year, ID) = ({}, {}) has been excluded.\n'
                        .format(out_row['project_year'], out_row['project_id']))

    return output


def change_data(data, change_mapping, name_map):
    wrote_header = False

    for row in data:
        project_tuple = (row['project_year'], row['project_id'])
        if project_tuple in change_mapping:
            old_countries_string = get_countries_string(row)

            new_countries = change_mapping[project_tuple]
            row['country_application'] = new_countries[0]
            row['country_application_name'] = get_country_name(new_countries[0], name_map)

            row['country_impact'] = new_countries[1]
            row['country_impact_name'] = get_country_name(new_countries[1], name_map)

            new_countries_string = get_countries_string(row)

            with open('../data/out.log', 'at') as a:
                if not wrote_header:
                    a.write('\n\nChanges in {}, format = (Appl Country, Appl Code, Impact Country, Impact Code)\n'
                            .format(row['project_year']))
                    a.write('*************************************************************************************\n')
                    wrote_header = True
                a.write('(Year, ID) = {} has been changed from: ({}) to: ({}).\n'
                        .format(str(project_tuple), old_countries_string, new_countries_string))


def get_countries_string(row):
    return '{}, {}, {}, {}'.format(
        row['country_application_name'],
        row['country_application'],
        row['country_impact_name'],
        row['country_impact']
    )


def write_data(data, year):
    with open('../data/cleaned_applications_{}.json'.format(year), 'wt') as w:
        json.dump(data, w)


def main():
    iso_map = import_iso_to_name_maps()
    name_map = import_iso_to_name_map_from_file('../data/ISO_mapping.csv')
    delete_set = import_deletes('../data/delete_records.csv')
    change_map = import_iso_changes_from_file('../data/change_country_mapping.csv')
    for year in range(2011, 2016):
        raw_data = get_year_data(year)

        transformed_data = transform_data(raw_data, iso_map, name_map, delete_set)
        change_data(transformed_data, change_map, name_map)
        write_data(transformed_data, year)


if __name__ == '__main__':
    main()
