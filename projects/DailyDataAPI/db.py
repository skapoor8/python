# db.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# for OYD Daily program

import sqlite3

# class Database: This class contains the SQL connection & cursor
class Database (object):
    """ Database object:
        Contains the SQL database Connection and Cursor"""

    def __init__(self):
        self.filename = None
        self.conn = None
        self.cursor = None

    def open_db (self, filename = 'oyd_daily.db'):
        """ Database Object: open_db method
            Opens the SQL database
            Parameters: database - default 'rooster.db'
            Returns: Connection, Cursor - for the SQL database"""

        self.filename = filename

        try:
            self.conn = sqlite3.connect(filename)
        except:
            print(f"ERROR: unable to open database: {filename}")
            exit(1)

        # get the cursor for the database
        self.cursor = self.conn.cursor()

        return 0

    def close_db (self):
        try:
            self.conn.close()
            self.conn = None
            self.cursor = None
            return 0
        except:
            return 1
