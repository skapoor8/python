# natarea.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# for OYD Daily program

# class NatAreas_Table - used to query lists of national areas
# Note: the schema for the NatAreas_Table() is defined in the NatArea() object
class NatAreas_Table(object):
    def __init__(self):
        self.areas = []
        self.limit = None
        self.offset = None

    # Exectue the SQL query to get Courses from the Database
    def _sql_query (self, c, limit=None, offset=None):

        # add limit and offset if presented to query
        limoff = ''
        if self.limit:
            limoff = ' limit ' + str(limit)
        if self.offset:
            limoff += ' offset ' + str(offset)

        # execute the query for selected Courses in the database
        c.execute('SELECT * FROM areas' + limoff)
        row = c.fetchone()

        # check if a row was returned
        if row:
            # store all rows in the list
            while row:
                self.areas.append(row)
                row = c.fetchone()

            # return success
            return 0
        else:
            # return ERROR
            return 1

    # Count
    def count(self, db):
        """ NatAreas_Table.count() function
            Returns number of rows in areas table
            Parameters:
                db - Database() object
            Returns:
                number of rows in courses table"""
        try:
            c = db.cursor

            # execute the query for all users in the database
            c.execute('SELECT count(*) FROM areas')
            row = c.fetchone()

            # check if result otherwise return None
            if row:
                return row[0]
            else:
                return None
        except:
            return None

    # Query for a range of Students in the Database
    def query_range(self, db, limit, offset):
        self.areas = []
        self.limit = limit
        self.offset = offset

        return self._sql_query (c=db.cursor, limit=limit, offset=offset)

    # Query for All National Areas in the Database
    def query_all(self, db):
        self.areas = []
        self.limit = None
        self.offset = None

        return self._sql_query (c = db.cursor)

# class NatArea - used to manage available OYD National Areas
# includes the Schema for the National Areas Table - areas
class NatArea (object):
    def __init__(self, area_name=None, area_abbrev=None):
        """NatArea Object: __init__ Method
            Parameters: (all default to None)
                area_name - national area name
                area_abbrev - abbreviated name of national area"""

        # Dictionary of School Attributes
        self.attrs = {'nat_area_id': None,   # internal use only, do not change
            'area_name': area_name,
            'area_abbrev': area_abbrev
            }

        # Matching dictionary of UI Elements for NatArea Attributes
        self.ui2 = {
            0: {'item': 'area_name',
                'label':'Area Name',
                'edit_name':'editAreaName',
                'edit_type':'text',
                'placeholder':'Area Name',
                'select_options': None},
            1: {'item': 'area_abbrev',
                'label':'Area Abbreviation',
                'edit_name':'editAreaAbbrev',
                'edit_type':'text',
                'placeholder':'Abbreviation',
                'select_options':None}
            }

        # SQL Schema
        # Must match the attrs (attributes) above, line for line
        self.schema = ['nat_area_id',
            'area_name',
            'area_abbrev'
            ]

        # create the INSERT schema substituion string
        self.schema_insert = ", ".join(self.schema)

        # SQL Data Types for the SQL Schema
        # Must match the SQL Schema above, line for line
        self.types = ['integer primary key',
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

    # Method to get a tuuple of all school data
    def _get (self):
        """ NatArea Object: _get method (private)
        Returns a tuple of the NatArea data
        Used by sql_insert """

        # assuming that dictiionaries are unordered
        # retrive the data in oder as a tuple
        results = []
        for key in self.schema:
            results.append(self.attrs[key])

        return tuple(results)

    # Method to set all NatArea data from a SQL row tuple
    def _set (self, sql_data):
        """ NatArea Object: _set method (private)
        Sets NatArea data in the instance of the object.
        Used to set data from a sql query into the object.
        Parameters:
            sql_data - a 'row' tuple returned from a sql query for a National Area"""

        # copy the sql_data, a row, to self.attrs dictionary
        # use self.schema instead of self.attrs.keys() to interate
        # becaause the self.schema is a list and the order will not change
        i = 0
        for key in self.schema:
            self.attrs[key] = sql_data[i]
            i += 1

    def _sql_populate (self, c):
        """ NatArea Object: _sql_populate method (private)
        Populates the instance of NatArea from the database as a new row
        Parameters:
            c = cursor to database"""

        try:
            # Test 1, check for the SQL ID
            if self.attrs['nat_area_id']:
                test = (self.attrs['nat_area_id'], )
                c.execute('SELECT * FROM areas WHERE nat_area_id=?', test)
            # Test 2, check for NatArea Name
            elif self.attrs['area_name']:
                test = (self.attrs['area_name'], )
                c.execute('SELECT * FROM areas WHERE area_name=?', test)
            else:
                # if you did't fill in any information to test, why did you call populate?
                return 1
        except Exception as e:
            print (f"ERROR: NatArea()._sql_populate: {e}")
            return 1    # return Error

        # check if a row is returned
        row = c.fetchone()
        if row:
            self._set(row)
            return 0
        else:
            return 1

    def _sql_insert (self, conn, c):
        """NatArea Object: _sql_insert method (private)
        Inserts the instance of NatArea into the database as a new row
        Parameters:
            conn = connection to database
            c = cursor to database"""

        try:
            c.execute('INSERT INTO areas (' +  self.schema_insert + \
                ') VALUES ' + self.schema_insert_sub, self._get())
        except:
            # Insert failed so return Error
            return (1, 'Failed to add New Area!')

        # Save (commit) the changes
        conn.commit()

        # sql_id is auto assigned on insert. So, retrive the sql_id from the db
        name = (self.attrs['area_name'], )
        c.execute('SELECT nat_area_id FROM areas WHERE area_name=?', name)
        row = c.fetchone()
        self.attrs['nat_area_id'] = row[0]

        return (0, 'Area Successfully Added!')

    def _sql_update (self, conn, c):
        """NatArea Object: _sql_update method (private)
        Commits all attribute in the instance of NatArea
        to the associated existing row in the database
        Parameters:
            conn = connection to database
            c = cursor to database"""

        if self.attrs['nat_area_id'] is not None:
            try:
                # create the label = value string to UPDATE
                lvl = ''
                for label in self.schema:
                    lvl += label + ' = "' + str(self.attrs[label]) + '", '
                lvl = lvl [:-2]

                # update the row
                c.execute('UPDATE areas SET ' + lvl + \
                    ' WHERE nat_area_id=' + str(self.attrs['nat_area_id']))

                # Save (commit) the changes
                conn.commit()

                return 0    # return Success
            except Exception as e:
                print (f"ERROR: NatArea()._sql_update: {e}")
                return 1    # return Error
        else:
            print ("ERROR: NatArea()._sql_update: sql_id not yet set")
            return 1    # return Error

    def _sql_delete (self, conn, c):
        """NatArea Object: _sql_delete method (private)
        Deletes the row in the database assoicated with the
        instance of School
        Parameters:
            conn = connection to database
            c = cursor to database"""

        # ??? Handle Exceptions Here ???
        if self.attrs['nat_area_id'] is not None:
            try:
                # delete the row
                c.execute('DELETE FROM areas WHERE nat_area_id=' + \
                    str(self.attrs['nat_area_id']))

                # Save (commit) the changes
                conn.commit()

                return 0    # return Success
            except Exception as e:
                print (f"ERROR: NatArea()._sql_delete: {e}")
                return 1    # return Error
        else:
            print ("ERROR: NatArea()._sql_delete: sql_id not yet set")
            return 1    # return Error

    def get (self, db):
        """ NatArea Object: get method
        Populates the instance of NatArea from the database as a new row
        Parameters:
            db = Database object from which to retrive the cursor"""

        return self._sql_populate (db.cursor)

    def put (self, db):
        """NatArea Object: put method
        Inserts the instance of NatArea into the database as a new row
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_insert(db.conn, db.cursor)

    # commit the data in NatArea to the DB
    def update (self, db):
        """Nat Are aObject: update method
        Commits all attributes in the instance of NatArea
        to the associated existing row in the database
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_update(db.conn, db.cursor)
