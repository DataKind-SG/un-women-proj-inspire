__author__ = 'cq'

import openpyxl
import sqlite3 as db
import datetime


def create_table_sqlite(conn):
    cursor = conn.cursor()
    cursor.executescript('drop table if exists un_women;')
    create_table_query = 'create table un_women (year text,application_id text,project_name text,institution text,' \
                         'project_location_1 text, project_location_2 text, summary text, ' \
                         'project_details text, name_1 text, name_2 text, project_team text, dob1 text,' \
                         ' email_1 text, file_name text, video_link_website text, date_time text, other_details text)'
    cursor.execute(create_table_query)
    conn.commit()


def save_tosqlite(data,conn):
    cursor = conn.cursor()
    qmarks = ', '.join('?' * len(data))
    columns = ', '.join(data.keys())
    query = ('insert into un_women ({}) VALUES ({})'.format(columns, qmarks)).encode('utf-8')

    cursor.execute(query, data.values())
    conn.commit()


def read_file_return_workbook(filename):
    wb = openpyxl.load_workbook(filename)
    return wb


def process_other_details(ws, row, max_letter):
    current_letter = 'Q'
    other_details = ''
    while current_letter != max_letter:
        temp_details = ws[current_letter + str(row)].value
        if temp_details is not None:
            if isinstance(temp_details, datetime.datetime):
                temp_details = str(temp_details)
            other_details += '\n' + temp_details.encode('utf-8')
        current_letter = chr(ord(current_letter) + 1)

    return other_details


def clean_field(value):
    ret_value = value if value is not None else ''
    if isinstance(ret_value,str):
        ret_value = unicode(ret_value, "utf-8")
    return ret_value


def process_sheet_2011_2014(ws, conn):
    print 'Processing sheet: ' + ws.title
    highest_row = ws.get_highest_row()
    highest_col = ws.get_highest_column()
    print highest_col
    for row in range(2, highest_row + 1):

        data_dict = {"year": clean_field(ws['A' + str(row)].value),
                     "application_id": clean_field(ws['B' + str(row)].value),
                     "project_name": clean_field(ws['C' + str(row)].value),
                     "institution": clean_field(ws['D' + str(row)].value),
                     "project_location_1": clean_field(ws['E' + str(row)].value),
                     "project_location_2": clean_field(ws['f' + str(row)].value),
                     "summary": clean_field(ws['G' + str(row)].value),
                     "project_details": clean_field(ws['H' + str(row)].value),
                     "name_1": clean_field(ws['I' + str(row)].value), "name_2": clean_field(ws['J' + str(row)].value),
                     "project_team": clean_field(ws['K' + str(row)].value),
                     "dob1": clean_field(ws['L' + str(row)].value), "email_1": clean_field(ws['M' + str(row)].value),
                     "file_name": clean_field(ws['N' + str(row)].value),
                     "video_link_website": clean_field(ws['O' + str(row)].value),
                     "date_time": clean_field(ws['P' + str(row)].value),
                     "other_details": clean_field(process_other_details(ws, row, openpyxl.utils.get_column_letter(
                         highest_col)))}

        save_tosqlite(data_dict, conn)


if __name__ == '__main__':
    file_name = "/Users/cq/Dev/Personal/DataKindSG/un_women/project_inspire_2011_2015.xlsx"

    wb = read_file_return_workbook(file_name)
    sheet_names = wb.get_sheet_names()
    del sheet_names[0]
    print sheet_names

    conn = db.connect('un_women_data.sqlite')
    create_table_sqlite(conn)

    for sheet in sheet_names:
        process_sheet_2011_2014(wb.get_sheet_by_name(sheet), conn)
