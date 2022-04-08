# refreshuserdb.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# Refreshes the User Table in the OYD Daily Program Database for Testing

import sqlite3
from db import *
from user import *
from print_table import *
from werkzeug import generate_password_hash, check_password_hash

class Users_Table_Management (object):
    """ User_Table_Management object
        Management functions for 'users' Table """

    def __init__(self):
        self.user = User()

    def drop(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS users;')

    def create(self, db):
        db.cursor.execute('CREATE TABLE users (' + self.user.schema_create + ')')

    def insert_new_user(self, db, user, password):
        """ Insert a new User into the Database
            Parameters:
                db - database object,
                username - username,
                password - clear text password to be hashed
            Return:
                True - user created
                False - user already exists
        """
        c = db.cursor

        # hash the passwor for storage in the database
        hashed_password = generate_password_hash (password)
        user.attrs['hashed_password'] = hashed_password

        print(f"DEBUG.stm.insert_new_user user = {user}")
        print(f"DEBUG.stm.insert_new_user user._get() = {user._get()}")

        try:
            c.execute('INSERT INTO users (' + user.schema_insert + \
                ') VALUES ' + user.schema_insert_sub, user._get())
        except:
            # Insert failed so return Error
            return False

        # Save (commit) the changes
        db.conn.commit()

        return True

def refresh_users (filename, silent_mode):
    # Open the database designated by filename
    database = Database()
    database.open_db(filename)

    # Instantiate a Table object
    utm = Users_Table_Management()

    # Delete the table if it already exists
    utm.drop (database)

    # Create students table
    utm.create (database)

    # Create and Insert a New Student
    user = User()
    user.attrs['username'] = 'tomg'
    user.attrs['oyd_id'] = 15505
    user.attrs['access_level'] = 0
    user.attrs['first_name'] = 'Thomas'
    user.attrs['last_name'] = 'Grate'
    user.attrs['def_school'] = 'Redmond'
    user.attrs['def_region'] = 'Seattle'
    user.attrs['def_nat_area'] = 'West'
    user.attrs['school_list'] = '1,2,3,4'
    user.attrs['region_list'] = None

    if silent_mode:
        password = 'ironhand'
    else:
        password = str(input("New Password > "))

    if utm.insert_new_user(database, user, password):
        return
    elif not silent_mode:
        print("Error: 'users' table not refreshed")

    database.close_db()

if __name__ == "__main__":
    # if run as the main program - refresh the roster.db
    filename = 'oyd_daily.db'

    print (f"Refreshing {filename} user table file!")
    if  input("Refresh Y or n > ") == 'Y':
        print(f"Refreshing the Users table in {filename} database")
        # refresh the roster.db
        refresh_users (filename, False)
    else:
        print (f"OK, leaving the {filename} DB alone!")
        exit(0)

    # open the DB
    database = Database()
    database.open_db(filename)

    # Fetch and Print the new stocks Table
    database.cursor.execute('SELECT * FROM users')
    print_table(database, 'users', "Refreshed Users Table")
