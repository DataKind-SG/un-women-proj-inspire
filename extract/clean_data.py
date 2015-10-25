__author__ = 'cq'

import openpyxl
import sqlite3 as db
import datetime


def create_table_sqlite(conn):
    cursor = conn.cursor()
    cursor.executescript('drop table if exists un_women;')
    create_table_query = 'create table un_women (year,application_id,project_name,institution,project_location_1,' \
                         'project_location_2, summary, project_details, name_1, name_2, project_team, dob1, email_1, ' \
                         'file_name, video_link_website, date_time, other_details)'
    cursor.execute(create_table_query)
    conn.commit()


def save_tosqlite(data,conn):
    cursor = conn.cursor()
    qmarks = ', '.join('?' * len(data))
    query = "insert into un_women (%s) values (%s)" % (qmarks, qmarks)
    cursor.execute(query, data.keys() + data.values())
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


def process_sheet_2011_2014(ws, conn):
    print 'Processing sheet: ' + ws.title
    highest_row = ws.get_highest_row()
    highest_col = ws.get_highest_column()
    print highest_col
    for row in range(2, highest_row + 1):

        data_dict = {}

        data_dict["year"] = ws['A' + str(row)].value
        data_dict["application_id"] = ws['B' + str(row)].value
        data_dict["project_name"] = ws['C' + str(row)].value
        data_dict["institution"] = ws['D' + str(row)].value
        data_dict["project_location_1"] = ws['E' + str(row)].value
        data_dict["project_location_2"] = ws['f' + str(row)].value
        data_dict["summary"] = ws['G' + str(row)].value
        data_dict["project_details"] = ws['H' + str(row)].value
        data_dict["name_1"] = ws['I' + str(row)].value
        data_dict["name_2"] = ws['J' + str(row)].value
        data_dict["project_team"] = ws['K' + str(row)].value
        data_dict["dob1"] = ws['L' + str(row)].value
        data_dict["email_1"] = ws['M' + str(row)].value
        data_dict["file_name"] = ws['N' + str(row)].value
        data_dict["video_link_website"] = ws['O' + str(row)].value
        data_dict["date_time"] = ws['P' + str(row)].value
        data_dict["other_details"] = process_other_details(ws, row, openpyxl.utils.get_column_letter(highest_col))
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
