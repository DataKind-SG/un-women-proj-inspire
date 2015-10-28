import sqlite3
import csv


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
            change_map[(row['Year'], row['ID'])] = (row['Application_Code'], row['Impact_Code'],
                                                    row['Comments'])

    return change_map


def import_deletes(filename):
    delete_set = dict()
    with open(filename, 'rt') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            delete_set[(row['Year'], row['ID'])] = row['Comment']

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


def transform_data(input_data, iso_map, name_map):
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

        out_row['orig_country_application_name'] = clean_country_name
        out_row['orig_country_impact_name'] = clean_country_name
        out_row['orig_country_application'] = country_code
        out_row['orig_country_impact'] = country_code
        out_row['project_details'] = row['project_details']
        out_row['project_year'] = row['year']

        out_row['project_location_2'] = row['project_location_2']
        out_row['institution'] = row['institution']
        out_row['project_location_1'] = row['project_location_1']

        output.append(out_row)

    return output


def change_row(row, name_map, change_map, delete_map):
    project_tuple = (row['project_year'], row['project_id'])
    if project_tuple in change_map:
        new_countries = change_map[project_tuple]
        row['country_application'] = new_countries[0]
        row['country_application_name'] = get_country_name(new_countries[0], name_map)
        row['country_impact'] = new_countries[1]
        row['country_impact_name'] = get_country_name(new_countries[1], name_map)
        row['change_comment'] = new_countries[2]
    else:
        row['country_application_name'] = row['orig_country_application_name']
        row['country_impact_name'] = row['orig_country_impact_name']
        row['country_application'] = row['orig_country_application']
        row['country_impact'] = row['orig_country_impact']
        row['change_comment'] = ''

    if project_tuple in delete_map:
        row['is_deleted'] = '1'
        row['delete_comment'] = delete_map[project_tuple]
    else:
        row['is_deleted'] = '0'
        row['delete_comment'] = ''

    return row


def write_data(data, year, name_map, change_map, delete_map):
    fieldnames = ['project_year', 'project_id', 'country_application', 'country_application_name',
                  'country_impact', 'country_impact_name',
                  'orig_country_application', 'orig_country_application_name',
                  'orig_country_impact', 'orig_country_impact_name', 'change_comment',
                  'project_name', 'institution', 'project_location_1', 'project_location_2',
                  'is_deleted', 'delete_comment',
                  'sectors', 'project_summary', 'project_details', 'project_details_other',]

    with open('../data/cleaned_applications_{}.csv'.format(year), 'wt') as csvfile:
        w = csv.DictWriter(csvfile, fieldnames=fieldnames)
        w.writeheader()
        for row in data:
            changed_row = change_row(row, name_map, change_map, delete_map)
            w.writerow(changed_row)


def main():
    iso_map = import_iso_to_name_maps()
    name_map = import_iso_to_name_map_from_file('../data/ISO_mapping.csv')
    delete_map = import_deletes('../data/delete_records.csv')
    change_map = import_iso_changes_from_file('../data/change_country_mapping.csv')
    for year in range(2011, 2016):
        raw_data = get_year_data(year)
        transformed_data = transform_data(raw_data, iso_map, name_map)
        write_data(transformed_data, year, name_map, change_map, delete_map)


if __name__ == '__main__':
    main()
