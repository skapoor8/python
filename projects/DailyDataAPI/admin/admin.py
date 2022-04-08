# admin.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# for OYD Daily Program

from db import *
from user import *
from school import *
from werkzeug import generate_password_hash, check_password_hash

class Users_Table_Management (object):
    """ Users_Table_Management object
        Management functions for 'users' Table """

    def __init__(self):
        self.user = User()

    def drop_table(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS users;')

    def create_table(self, db):
        db.cursor.execute('CREATE TABLE users (' + self.user.schema_create + ')')

    def insert_new_user(self, db, user, password):
        """ Insert a new User into the Database
            Parameters:
                db - database object,
                username - username,
                password - clear text password to be hashed
            Returns a tuple:
                Error Code
                    0 = success
                    1 = error
                Error Message - human readable messge
        """

        c = db.cursor

        # hash the passwor for storage in the database
        hashed_password = generate_password_hash (password)
        user.attrs['hashed_password'] = hashed_password

        # check if the user already exists
        where = ' WHERE username = "' + str(user.attrs['username']) + \
            '" or ' + 'user_id = "' + str(user.attrs['user_id']) + '"'

        c.execute('SELECT * FROM users' + where)
        row = c.fetchone()

        if row:
            return (1, "User Already Exists")
        else:
            # insert the New User
            try:
                c.execute('INSERT INTO users (' + user.schema_insert + \
                    ') VALUES ' + user.schema_insert_sub, user._get())
            except:
                # Insert failed so return Error
                return (2, "Failed to add New User!")

            # Save (commit) the changes
            db.conn.commit()

            return (0, "User Successfully Added!")

class Users_Table (object):
    """ Users_Table object
        Presentation functions for 'users' Table """

    def __init__(self):
        self.user = User()

    def count_rows(self, db):
        """ User_Table.count() function
            Returns number of rows in users table
            Parameters:
                db - Database() object
            Returns:
                number of rows in user table"""
        try:
            c = db.cursor

            # execute the query for all users in the database
            c.execute('SELECT count(*) FROM users')
            row = c.fetchone()

            # check if result other return None
            if row:
                return row[0]
            else:
                return None
        except:
            return None

    def get_all(self, db, limit = None, offset = None):
        """ User_Table.get_all() function
            Returns all users in the users table
            Parameters:
                db - Database() object
                limit - number of rows to retrieve
                offset - starting row from which to receive
            Returns a tuple
                error:
                    0 = success
                    1 = no data
                    2 = failed query
                rows: a tuple of tuples - one row per user"""
        try:
            c = db.cursor

            # add limit and offset if presdent to query
            limoff = ''
            if limit is not None:
                limoff = ' limit ' + str(limit)
            if offset is not None:
                limoff += ' offset ' + str(offset)

            # execute the query for all users in the database
            c.execute('SELECT * FROM users' + limoff)
            rows = c.fetchall()

            # check if a row was returned
            if rows:
                return (0, rows, "Success")
            else:
                return (1, None, "No Users Found in Database")
        except:
            return (2, None, "Query for Users Failed")

class Schools_Table_Management (object):
    """ Schools_Table_Management object
        Management functions for 'schools' Table """

    def __init__(self):
        pass

    def drop_table(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS schools;')

    def create_table(self, db):
        db.cursor.execute('CREATE TABLE schools (' + School().schema_create + ')')


class Regions_Table_Management (object):
    """ Regions_Table_Management object
        Management functions for 'regions' Table """

    def __init__(self):
        pass

    def drop_table(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS regions;')

    def create_table(self, db):
        db.cursor.execute('CREATE TABLE regions (' + Region().schema_create + ')')

class NatAreas_Table_Management (object):
    """ NatAreas_Table_Management object
        Management functions for 'areas' Table """

    def __init__(self):
        pass

    def drop_table(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS areas;')

    def create_table(self, db):
        db.cursor.execute('CREATE TABLE areas (' + NatArea().schema_create + ')')
