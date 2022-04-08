# user.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# for OYD Daily program

from werkzeug import generate_password_hash, check_password_hash

# class User, represents the logged in user
class User(object):
    def __init__(self):
        # Note that the clear text password is not stored in the User object
        self.attrs = {'user_id': None,   # internal use only, do not change
            'username': None,
            'hashed_password': None,        # not set on validation
            'oyd_id': None,
            'access_level': None,
            'first_name': None,
            'last_name': None,
            'def_school': None,
            'def_region': None,
            'def_nat_area': None,
            'school_list': None,
            'region_list': None
            }

        # Lables for use in the Web UI
        # Note: password is showin in the lables for the UI
        self.labels = {'user_id': 'User ID',
            'username': 'Username',
            'password': 'Password',
            'oyd_id': 'OYD ID:',
            'access_level': 'Access Level',
            'first_name': 'First Name:',
            'last_name': 'Last Name:',
            'def_school': 'Default School',
            'def_region': 'Default Region',
            'def_nat_area': 'Default National Area',
            'school_list': 'School List',
            'region_list': 'Region List'
            }

        # Label types for use in the Web UI
        # Note: password is shown in the lable_types for the UI
        self.label_types = {'user_id': "text",
            'username': "text",
            'password': "text",
            'oyd_id': "text",
            'access_level': "text",
            'first_name': "text",
            'last_name': "text",
            'def_school': "text",
            'def_region': "text",
            'def_nat_area': "text",
            'school_list': "text",
            'region_list': "text"
            }

        # Table Schema
        self.schema = ['user_id',
            'username',
            'hashed_password',
            'oyd_id',
            'access_level',
            'first_name',
            'last_name',
            'def_school',
            'def_region',
            'def_nat_area',
            'school_list',
            'region_list'
            ]

        # create the INSERT schema substituion string
        self.schema_insert = ", ".join(self.schema)

        # SQL Data Types for the Table Schema
        # Must match the Table Schema above, line for line
        self.types = ['integer primary key',
            'text',
            'text',
            'integer',
            'integer',
            'text',
            'text',
            'text',
            'text',
            'text',
            'text',
            'text'
            ]

        # make the CREATE schema substituion string
        # used to create the student table
        self.schema_create = ''
        limit = len(self.schema) - 1
        i = 0
        for i in range(0, limit):
            addstr = self.schema[i] + ' ' + self.types[i] + ', '
            self.schema_create += addstr
        self.schema_create += self.schema[limit] + ' ' + self.types[limit]

        # VALUE substitution string
        self.schema_insert_sub = '(' + '?,' * (len(self.schema) - 1) + '?)'

    def _get (self):
        """ User Object: _get method (private)
        Returns a tuple of the User data
        Used by the User_Table_Management.insert_new_user """
        return tuple(self.attrs.values())

    def _set (self, sql_data):
        """ User Object: _set method (private)
        Sets User data in the instance of the object.
        Used to set data from a sql query into the object.
        Parameters:
            sql_data - a 'row' tuple returned from a sql query for a student"""

        # copy the sql_data, a row, to self.attrs dictionary
        # use self.schema instead of self.attrs.keys() to interate
        # becaause teh self.schema is a list and the order will not change
        i = 0
        for key in self.schema:
            self.attrs[key] = sql_data[i]
            i += 1

        # clear out the hashed_password
        self.attrs['hashed_password'] = None

        return

    # ??? Move to admin.py once working
    def _sql_populate (self, c):
        """ User Object: _sql_populate method (private)
        Populates the instance of User from the database as a new row
        Parameters:
            c = cursor to database"""
        try:
            # Query the database for the student by name
            test1 = (self.attrs['user_id'], )

            # Test #1, check for the OYD ID
            c.execute('SELECT * FROM users WHERE user_id = ?', test1)
            row = c.fetchone()

            if row:
                self._set(row)
                return 0
            else:
                return 1
        except Exception as e:
            return 1

    # ??? Move to admin.py once working
    def _insert_new_user(self, db, password):
        """ Insert a new User into the Database
            Parameters:
                db - database object,
                password - clear text password to be hashed
            Returns a tuple:
                Error Code
                    0 = success
                    1 = error
                Error Message - human readable messge
        """

        # get the database cursor
        c = db.cursor

        # hash the passwor for storage in the database
        hashed_password = generate_password_hash (password)
        self.attrs['hashed_password'] = hashed_password

        # check if the user already exists
        where = ' WHERE username = "' + str(self.attrs['username']) + \
            '" or ' + 'user_id = "' + str(self.attrs['user_id']) + '"'

        c.execute('SELECT * FROM users' + where)
        row = c.fetchone()

        if row:
            return (1, "User Already Exists")
        else:
            # insert the New User
            try:
                c.execute('INSERT INTO users (' + self.schema_insert + \
                    ') VALUES ' + self.schema_insert_sub, self._get())
            except:
                # Insert failed so return Error
                return (2, "Failed to add New User!")

            # Save (commit) the changes
            db.conn.commit()

            return (0, "User Successfully Added!")

    # ??? Move to admin.py once working
    def _sql_update (self, conn, c, password):
        """User Object: _sql_commit method (private)
        Commits all attribute in the instance of User
        to the associated existing row in the database
        Parameters:
            conn = connection to database
            c = cursor to database
            password - password to hash"""

        try:
            if password:
                # hash the passwor for storage in the database
                hashed_password = generate_password_hash (password)
                self.attrs['hashed_password'] = hashed_password

            # create the label = value string to UPDATE
            lvl = ''
            for label in self.schema:
                if label == 'hashed_password':
                    if password:
                        lvl += label + ' = "' + str(self.attrs[label]) + '", '
                else:
                    lvl += label + ' = "' + str(self.attrs[label]) + '", '
            lvl = lvl [:-2]

            # update the row
            c.execute('UPDATE users SET ' + lvl + \
                ' WHERE user_id=' + str(self.attrs['user_id']))

            # Save (commit) the changes
            conn.commit()

            return 0    # return Success
        except Exception as e:
            return 1    # return Error

    # ??? Move to admin.py once working
    def _sql_delete (self, conn, c):
        """User Object: _sql_delete method (private)
        Deletes the user identified by .attrs[]'user_id']
        Parameters:
            conn = connection to database
            c = cursor to database
            password - password to hash"""

        try:
            # delete the user
            c.execute('DELETE FROM users WHERE user_id = "' + \
                str(self.attrs['user_id']) + '"')

            # Save (commit) the changes
            conn.commit()

            return 0    # return Success
        except Exception as e:
            return 1    # return Error

    # populate the user object attributes from the database
    def get (self, db):
        """ User Object: populate_from_db method
        Populates the instance of User from the database as a new row
        Parameters:
            db = Database object from which to retrive the cursor"""

        return self._sql_populate (db.cursor)

    # ??? Move to admin.py once working
    # add a new user ot the users he database
    def put (self, db, password):
        """ User Object: put method
        Inserts the instance of User into database as a new row
        Parameters:
            db = Database object from which to retrive the cursor"""

        return self._insert_new_user (db, password)


    # ??? Move to admin.py once working
    # commit the data in User to the DB
    def update (self, db, password = None):
        """User Object: update method
        Updates all attributes in the instance of User
        to the associated existing row in the database
        Parameters:
            db = Database object that contains the
                connection & cursor to database
            password - password to hash, default is None"""

        return self._sql_update (db.conn, db.cursor, password)

    # ??? Move to admin.py once working
    # delete the User
    def delete (self, db):
        """user Object: delete
        Deletes the user idenfied by .attrs['user_id] from
        the database
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_delete (db.conn, db.cursor)

    # validates a user login provided the database, useername, & password
    def authenticate (self, db, username, password):
        """ Validates a User Login.
            Parameters:
                db - database object,
                username - username to validate_login,
                password - clear text password to validate
            Return:
                True - for valid user, also fills in object attrs
                False - invalid oyd_id, username, or password
            """

        # query for username
        c = db.cursor
        where = "WHERE username = '" + username + "'"
        c.execute('SELECT * FROM users ' + where)
        data = c.fetchone()            # returns a tuple

        # check if a data was returned
        if data:
            # validdate password
            if check_password_hash(str(data[2]), password):
                self._set(data)
                return True
            else:
                return False
        # error, no such user
        else:
            return False
