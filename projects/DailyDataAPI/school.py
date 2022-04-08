# school.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# for OYD Daily program
#
# class Schools_Table - used to query lists of schools
# Note: the schema for the Schools_Table() is defined in the School() object
class Schools_Table(object):
    def __init__(self):
        self.region = None
        self.schools = []
        self.limit = None
        self.offset = None

    # Exectue the SQL query to get Schools from the Database based on the parameters
    #   - region
    def _sql_query (self, c, limit=None, offset=None):

        # build the WHERE clause
        test_params = {'school_region': self.region}
        where = ''
        where_flag = True
        and_flag = False
        for key, param in test_params.items():
             if param is not None:
                 if where_flag is True:
                     where += ' WHERE '
                     where_flag = False
                 elif and_flag is True:
                     where += ' AND '
                 where += key + " = '" + str(param) + "'"
                 and_flag = True

        # add limit and offset if presdent to query
        limoff = ''
        if self.limit:
            limoff = ' limit ' + str(limit)
        if self.offset:
            limoff += ' offset ' + str(offset)

        # execute the query for selected schools in the database
        c.execute('SELECT * FROM schools' + where + limoff)
        row = c.fetchone()

        # check if a row was returned
        if row:
            # store all rows in the list
            while row:
                self.schools.append(row)
                row = c.fetchone()

            # return success
            return 0
        else:
            # return ERROR
            return 1

    # Count
    def count(self, db, region=None):
        """ School_Table.count() function
            Returns number of rows in Schools table meeting the parameters
            Parameters:
                db - Database() object
                region - default None
            Returns:
                number of rows in schools table meeting the parameters"""
        try:
            c = db.cursor

            # build the WHERE clause
            test_params = {'school_region': region}
            where = ''
            where_flag = True
            and_flag = False
            for key, param in test_params.items():
                 if param is not None:
                     if where_flag is True:
                         where += ' WHERE '
                         where_flag = False
                     elif and_flag is True:
                         where += ' AND '
                     where += key + " = '" + str(param) + "'"
                     and_flag = True

            # execute the query for all users in the database
            c.execute('SELECT count(*) FROM schools' + where)
            row = c.fetchone()

            # check if result otherwise return None
            if row:
                return row[0]
            else:
                return None
        except:
            return None

    # Query for a range of Students in the Database
    def query_range(self, db, limit, offset, region=None):
        if region != self.region:
            self.region = region

        # invalidate amy previous query results
        self.schools = []
        self.limit = limit
        self.offset = offset

        return self._sql_query (c=db.cursor, limit=limit, offset=offset)

    # General Query where status can be supplied
    def query(self, db, region=None):
        if region != self.region:
            self.region = region

            # on any change to agove, invalidate amy previous query results
            self.schools = []
            self.limit = None
            self.offset = None

        return self._sql_query (c = db.cursor)

    # Query for All Students in the Database
    def query_all(self, db):
        # invalidate amy previous query results
        self.region = None
        self.schools = []
        self.limit = None
        self.offset = None

        return self._sql_query (c = db.cursor)

class School (object):
    def __init__(self, school_name=None, main_ins_id=None, school_region=None,
        street=None, street2=None, city=None, state=None, postal_code=None,
        country='USA',
        email=None, school_phone=None,
        status=None, standing=None):
        """School Object: __init__ Method
            Parameters: (all default to None)
                school_name - school name
                main_ins_id - school's main instructor
                school_region - school's region
                street - street address line 1
                steet2 - street address line 2
                city - city
                state - two (2) letter state abbreviation
                postal_code - postal code
                country - country name, defaults to USA
                email - school's email address
                school_phone - school's phone number
                status - school operating status
                standing - school standing with OYD"""

        # Dictionary of School Attributes
        self.attrs = {'school_id': None,   # internal use only, do not change
            'school_name': school_name,
            'main_ins_id': main_ins_id,
            'school_region': school_region,
            'street': street,
            'street2': street2,
            'city': city,
            'state': state,
            'postal_code': postal_code,
            'country': country,
            'email': email,
            'school_phone': school_phone,
            'status': status,
            'standing': standing
            }

        self.select_status = {'Open':'0', 'Closed':'1'}

        self.select_status = {'Open':'0', 'Closed':'1'}

        # Matching dictionary of UI Elements for School Attributes
        # 0:Label | 1:edit_name | 2:edit_type | 3:placeholder | 4:select options list
        self.ui = {
            # 'sql_id': ['SQL ID', 'editSqlId', 'hidden', '', None],
            'school_name': ['School Name:', 'editName', 'text', 'School Name', None],
            'main_ins_id': ['Main Instr:', 'editMainIns', 'number', '00000', None],
            'school_region': ['Region:', 'editRegion', 'select', '', None],
            'street': ['Street:', 'editStreet', 'text', 'Street Address', None],
            'street2': ['Street2:', 'editStreet2', 'text', 'Street Address Line 2', None],
            'city': ['City:', 'editCity', 'text', 'City', None],
            'state': ['State:', 'editState', 'text', 'State', None],
            'postal_code': ['Postal Code:', 'editPostalCode', 'text', '98052', None],
            'country': ['Country:', 'editCountry', 'text', 'USA', None],
            'email': ['School eMail:', 'editeMail', 'text', 'eMail Address', None],
            'school_phone': ['School Phone:', 'editPhone', 'text', 'Phone', None],
            'status': ['Status:', 'editStatus', 'select', '0', {'Open':'0', 'Closed':'1'}],
            'standing': ['Standing:', 'editStanding', 'select', '0', {'Good':'0', 'Behind':'1'}]
            }

        # Matching dictionary of UI Elements for School Attributes
        self.ui2 = {
            0: {'item': 'school_name',
                'label':'School Name',
                'edit_name':'editName',
                'edit_type':'text',
                'required': True,
                'placeholder':'School Name',
                'select_options': None},
            1: {'item': 'main_ins_id',
                'label':'Main Instr',
                'edit_name':'editMainIns',
                'edit_type':'number',
                'required': True,
                'placeholder':'00000',
                'select_options':None},
            2: {'item': 'school_region',
                'label':'Region',
                'edit_name':'editRegion',
                'edit_type':'select',
                'required': True,
                'placeholder':'Region',
                'select_options':None},
            3: {'item': 'street',
                'label':'Street',
                'edit_name':'editStreet',
                'edit_type':'text',
                'required': True,
                'placeholder':'Street Address',
                'select_options':None},
            4: {'item': 'street2',
                'label':'Street 2',
                'edit_name':'editStreet2',
                'edit_type':'text',
                'required': False,
                'placeholder':'Street Address Line 2',
                'select_options':None},
            5: {'item': 'city',
                'label':'City',
                'edit_name':'editCity',
                'edit_type':'text',
                'required': True,
                'placeholder':'City',
                'select_options':None},
            6: {'item': 'state',
                'label':'State',
                'edit_name':'editState',
                'edit_type':'text',
                'required': True,
                'placeholder':'State',
                'select_options':None},
            7: {'item': 'postal_code',
                'label':'Postal Code',
                'edit_name':'editPostalCode',
                'edit_type':'text',
                'required': True,
                'placeholder':'98052',
                'select_options':None},
            8: {'item': 'country',
                'label':'Country',
                'edit_name':'editCountry',
                'edit_type':'text',
                'required': True,
                'placeholder':'USA',
                'select_options':None},
            9: {'item': 'email',
                'label':'School eMail',
                'edit_name':'editeMail',
                'edit_type':'text',
                'required': True,
                'placeholder':'eMail Address',
                'select_options':None},
            10: {'item': 'school_phone',
                'label':'School Phone',
                'edit_name':'editPhone',
                'edit_type':'text',
                'required': True,
                'placeholder':'Phone',
                'select_options':None},
            11: {'item': 'status',
                'label':'Status',
                'edit_name':'editStatus',
                'edit_type':'select',
                'required': True,
                'placeholder':'0',
                'select_options':{'Open':'0', 'Closed':'1'}},
            12: {'item': 'standing',
                'label':'Standing',
                'edit_name':'editStanding',
                'edit_type':'select',
                'required': True,
                'placeholder':'0',
                'select_options':{'Good':'0', 'Behind':'1'}}
            }

        # SQL Schema
        # Must match the attrs (attributes) above, line for line
        self.schema = ['school_id',
            'school_name',
            'main_ins_id',
            'school_region',
            'street',
            'street2',
            'city',
            'state',
            'postal_code',
            'country',
            'email',
            'school_phone',
            'status',
            'standing'
            ]

        # create the INSERT schema substituion string
        self.schema_insert = ", ".join(self.schema)

        # SQL Data Types for the SQL Schema
        # Must match the SQL Schema above, line for line
        self.types = ['integer primary key',
            'text',
            'integer',
            'integer',
            'text',
            'text',
            'text',
            'text',
            'text',
            'text',
            'text',
            'text',
            'integer',
            'integer'
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
        """ School Object: _get method (private)
        Returns a tuple of the School data
        Used by sql_insert_new """

        # assuming that dictiionaries are unordered
        # retrive the data in oder as a tuple
        results = []
        for key in self.schema:
            results.append(self.attrs[key])

        return tuple(results)

    # Method to set all school data from a SQL row tuple
    def _set (self, sql_data):
        """ School Object: _set method (private)
        Sets School data in the instance of the object.
        Used to set data from a sql query into the object.
        Parameters:
            sql_data - a 'row' tuple returned from a sql query for a school"""

        # copy the sql_data, a row, to self.attrs dictionary
        # use self.schema instead of self.attrs.keys() to interate
        # becaause the self.schema is a list and the order will not change
        i = 0
        for key in self.schema:
            self.attrs[key] = sql_data[i]
            i += 1

    def _sql_populate (self, c):
        """ School Object: _sql_populate method (private)
        Populates the instance of School from the database as a new row
        Parameters:
            c = cursor to database"""

        try:
            # Test 1, check for the SQL ID
            if self.attrs['school_id']:
                test = (self.attrs['school_id'], )
                c.execute('SELECT * FROM schools WHERE school_id=?', test)
            # Test 2, check for School Name
            elif self.attrs['school_name']:
                test = (self.attrs['school_name'], )
                c.execute('SELECT * FROM schools WHERE school_name=?', test)
            else:
                # if you did't fill in any information to test, why did you call populate?
                return 1
        except Exception as e:
            print (f"ERROR: School()._sql_populate: {e}")
            return 1    # return Error

        # check if a row is returned
        row = c.fetchone()
        if row:
            self._set(row)
            return 0
        else:
            return 1

    def _sql_insert (self, conn, c):
        """School Object: _sql_insert method (private)
        Inserts the instance of School into the database as a new row
        Parameters:
            conn = connection to database
            c = cursor to database"""

        # check if the user already exists
        where = ' WHERE school_name = "' + str(self.attrs['school_name']) + '"'

        c.execute('SELECT * FROM schools' + where)
        row = c.fetchone()

        if row:
            return (1, "School Already Exists")
        else:
            try:
                c.execute('INSERT INTO schools (' +  self.schema_insert + \
                    ') VALUES ' + self.schema_insert_sub, self._get())
            except:
                # Insert failed so return Error
                return (2, "Failed to add New School")

            # Save (commit) the changes
            conn.commit()

            # school_id is auto assigned on insert. So, retrive the school_id from the db
            name = (self.attrs['school_name'], )
            c.execute('SELECT school_id FROM schools WHERE school_name=?', name)
            row = c.fetchone()
            self.attrs['school_id'] = row[0]

            return (0, "School Successfully Added!")

    def get_schools (nat_area=None, region=None):
        pass

    def _sql_update (self, conn, c):
        """School Object: _sql_update method (private)
        Commits all attribute in the instance of School
        to the associated existing row in the database
        Parameters:
            conn = connection to database
            c = cursor to database"""

        if self.attrs['school_id'] is not None:
            try:
                # create the label = value string to UPDATE
                lvl = ''
                for label in self.schema:
                    lvl += label + ' = "' + str(self.attrs[label]) + '", '
                lvl = lvl [:-2]

                # update the row
                c.execute('UPDATE schools SET ' + lvl + \
                    ' WHERE school_id=' + str(self.attrs['school_id']))

                # Save (commit) the changes
                conn.commit()

                return 0    # return Success
            except Exception as e:
                print (f"ERROR: School()._sql_update: {e}")
                return 1    # return Error
        else:
            print ("ERROR: School()._sql_update: school_id not yet set")
            return 1    # return Error

    def _sql_delete (self, conn, c):
        """School Object: _sql_delete method (private)
        Deletes the row in the database assoicated with the
        instance of School
        Parameters:
            conn = connection to database
            c = cursor to database"""

        # ??? Handle Exceptions Here ???
        if self.attrs['school_id'] is not None:
            try:
                # delete the row
                c.execute('DELETE FROM schools WHERE school_id=' + \
                    str(self.attrs['school_id']))

                # Save (commit) the changes
                conn.commit()

                return 0    # return Success
            except Exception as e:
                print (f"ERROR: School()._sql_delete: {e}")
                return 1    # return Error
        else:
            print ("ERROR: School()._sql_delete: school_id not yet set")
            return 1    # return Error

    def get (self, db):
        """ School Object: get method
        Populates the instance of School from the database as a new row
        Parameters:
            db = Database object from which to retrive the cursor"""

        return self._sql_populate (db.cursor)

    def put (self, db):
        """School Object: put method
        Inserts the instance of School into the database as a new row
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_insert(db.conn, db.cursor)

    def delete(self, db):
        """School Object: delete method
        Delets the row associated with the instance of School
        from the database
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_delete(db.conn, db.cursor)

    #    commit the data in Student to the DB
    def update (self, db):
        """School Object: update_school method
        Commits all attributes in the instance of School
        to the associated existing row in the database
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_update(db.conn, db.cursor)
