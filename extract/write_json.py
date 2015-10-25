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
    with sqlite3.connect('../data/early.db') as conn:
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute('SELECT * FROM stocks WHERE project_year=?', y)
        data = c.fetchall()
    return data


def transform_data(input):
    output = list()
    for row in input:
        output.append(row)

    return output

def 


def main():
    iso_map = import_iso_map()
    for year in range(2011, 2015):
        raw_data = get_year_data(year)
        transformed_data = transform_data(raw_data)
        write_data(raw_data)




if __name__ == '__main__':
    main()
