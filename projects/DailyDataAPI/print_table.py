# print_table.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# for OYD Daily program

# Given a Database, table name and a title, print the table with title
def print_table(db, table, title):
    """ print_table function
        Prints a SQLite3 Table given a Database, Table Name and a Title for the
        Table"""

    # print title and divider the same length as the title
    print(f"Table: {table} | {title}")
    print('-' * (len(title) + len(table) + 10))

    # get the table data
    db.cursor.execute('SELECT * FROM ' + table)

    # print the Column Names
    # would have gotten these from sqlite3.row.keys() but the Row
    # returns as a tuple and not as the class, so no method keys()
    col_names = '| '
    for i in db.cursor.description:
        col_names = col_names + i[0] + ' | '
    print(col_names)

    # print all rows
    # this coould be done with c.fetchall() but memory is a consideration
    row = db.cursor.fetchone()
    while row:
        print(row)
        row = db.cursor.fetchone()

    # follow table with a blank line
    print('')
# ----------------------------------------------------------------------------
