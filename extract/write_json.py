import sqlite3
import csv
import json


def import_iso_map():
    iso_map = dict()
    with open('../data/ISO_mapping.csv', 'rt') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            iso_map[row['Name']] = row['Code']

    return iso_map


def dict_factory(cursor, row):
    d = dict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_year_data(year):
    y = (year,)
    with sqlite3.connect('../source_data/early.db') as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute('SELECT * FROM table WHERE project_year=?', y)
        data = c.fetchall()
    return data


def get_test_data(year):
    data = [{'project_year': year, 'title': 'asdf', 'country': 'Singapore'},
            {'project_year': year, 'title': 'qwer', 'country': 'Malaysia'},
            {'project_year': year, 'title': 'zxcv', 'country': 'Indonesia'}]
    return data


def transform_data(input, iso_map):
    output = list()
    for row in input:
        out_row = dict()
        out_row['project_year'] = row['project_year']
        out_row['title'] = row['title']
        out_row['country'] = row['country']
        out_row['country_code'] = iso_map[row['country']]
        output.append(out_row)

    return output


def write_data(data, year):
    with open('../data/cleaned_applications_{}.json'.format(year), 'wt') as w:
        json.dump(data, w)


def main():
    iso_map = import_iso_map()
    for year in range(2011, 2015):
        # raw_data = get_year_data(year)
        raw_data = get_test_data(year)

        transformed_data = transform_data(raw_data, iso_map)
        write_data(transformed_data, year)


if __name__ == '__main__':
    main()
