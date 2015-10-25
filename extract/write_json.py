import sqlite3
import csv
import json


def import_iso_map():
    iso_map = import_map_from_file('../data/ISO_mapping.csv')
    additional_map = import_map_from_file('../data/additional_countries.csv')
    iso_map.update(additional_map)
    return iso_map


def import_map_from_file(filename):
    this_map = dict()
    with open(filename, 'rt') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            this_map[row['Name']] = row['Code']

    return this_map


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


def get_test_data(year):
    data = [{'project_year': year, 'title': 'asdf', 'country': 'Singapore'},
            {'project_year': year, 'title': 'qwer', 'country': 'Malaysia'},
            {'project_year': year, 'title': 'zxcv', 'country': 'Indonesia'}]
    return data


def get_country_code(country_name, iso_map):
    try:
        country_code = iso_map[country_name]
    except KeyError:
        print('Unknown country name: {}'.format(country_name))
        country_code = ''

    return country_code

def transform_data(input, iso_map):
    output = list()
    for row in input:
        out_row = dict()
        out_row['project_details_other'] = row['other_details']
        out_row['project_id'] = row['application_id']
        out_row['project_summary'] = row['summary']
        out_row['project_name'] = row['project_name']
        out_row['sectors'] = ''

        country_name = row['project_location_2'].strip()
        country_code = get_country_code(country_name, iso_map)

        out_row['country_application_name'] = country_name
        out_row['country_impact_name'] = country_name # needs modification
        out_row['country_application'] = country_code
        out_row['country_impact'] = country_code # needs modification
        out_row['project_details'] = row['project_details']
        out_row['project_year'] = row['year']
        output.append(out_row)

    return output


def write_data(data, year):
    with open('../data/cleaned_applications_{}.json'.format(year), 'wt') as w:
        json.dump(data, w)


def main():
    iso_map = import_iso_map()
    for year in range(2011, 2015):
        raw_data = get_year_data(year)

        transformed_data = transform_data(raw_data, iso_map)
        write_data(transformed_data, year)


if __name__ == '__main__':
    main()
