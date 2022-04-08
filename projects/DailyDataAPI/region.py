# region.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# for OYD Daily program

# class Regions_Table - used to query lists of regions
# Note: the schema for the Regions_Table() is defined in the Region() object
class Regions_Table(object):
    def __init__(self):
        self.regions = []
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
        c.execute('SELECT * FROM regions' + limoff)
        row = c.fetchone()

        # check if a row was returned
        if row:
            # store all rows in the list
            while row:
                self.regions.append(row)
                row = c.fetchone()

            # return success
            return 0
        else:
            # return ERROR
            return 1

    # Count
    def count(self, db):
        """ Regions_Table.count() function
            Returns number of rows in Regions table
            Parameters:
                db - Database() object
            Returns:
                number of rows in courses table"""
        try:
            c = db.cursor

            # execute the query for all users in the database
            c.execute('SELECT count(*) FROM regions')
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
        self.regions = []
        self.limit = limit
        self.offset = offset

        return self._sql_query (c=db.cursor, limit=limit, offset=offset)

    # Query for All Regions in the Database
    def query_all(self, db):
        self.regions = []
        self.limit = None
        self.offset = None

        return self._sql_query (c = db.cursor)

# class Region - used to manage available OYD Regions
# includes the Schema for the Regions Table - regions
class Region (object):
    def __init__(self, region_name=None, region_abbrev=None,
        nat_area=None, main_reg_id=None, reg_team_ids=None,
        street=None, street2=None, city=None, state=None,
        postal_code=None, country='USA',
        email=None, phone=None, status=None, standing=None):
        """Region Object: __init__ Method
            Parameters: (all default to None)
                region_name - region name
                region_abbrev - abbreviated region name
                main_reg_id - region's main regional head instructor
                reg_team_ids - members of regional team
                nat_area - school's national area
                street - street address line 1
                steet2 - street address line 2
                city - city
                state - two (2) letter state abbreviation
                postal_code - postal code
                country - country name, defaults to USA
                email - school's email address
                phone - school's phone number
                status - region operating status
                standing - region standing with OYD"""

        # Dictionary of School Attributes
        self.attrs = {'region_id': None,   # internal use only, do not change
            'region_name': region_name,
            'region_abbrev': region_abbrev,
            'main_reg_id': main_reg_id,
            'reg_team_ids': reg_team_ids,
            'nat_area': nat_area,
            'street': street,
            'street2': street2,
            'city': city,
            'state': state,
            'postal_code': postal_code,
            'country': country,
            'email': email,
            'phone': phone,
            'status': status,
            'standing': standing
            }

        self.select_status = {'Open':'0', 'Closed':'1'}

        self.select_standing = {'Good':'0', 'Behind':'1'}

        # Matching dictionary of UI Elements for Region Attributes
        self.ui2 = {
            0: {'item': 'region_name',
                'label':'Region Name',
                'edit_name':'editName',
                'edit_type':'text',
                'placeholder':'Region Name',
                'select_options': None},
            1: {'item': 'region_abbrev',
                'label':'Region Abbreviation',
                'edit_name':'editAbbrev',
                'edit_type':'text',
                'placeholder':'Region Abbreviation',
                'select_options': None},
            2: {'item': 'main_reg_id',
                'label':'Main Reg. Head Instr Id',
                'edit_name':'editRegHead',
                'edit_type':'number',
                'placeholder':'Instr OYD Id',
                'select_options':None},
            3: {'item': 'reg_team_ids',
                'label':'Regional Team Ids',
                'edit_name':'editRegTeam',
                'edit_type':'text',
                'placeholder':'Instr OYD Ids',
                'select_options':None},
            4: {'item': 'nat_area',
                'label':'National Area',
                'edit_name':'editNatArea',
                'edit_type':'select',
                'placeholder':'',
                'select_options':None},
            5: {'item': 'street',
                'label':'Street',
                'edit_name':'editStreet',
                'edit_type':'text',
                'required': True,
                'placeholder':'Street Address',
                'select_options':None},
            6: {'item': 'street2',
                'label':'Street 2',
                'edit_name':'editStreet2',
                'edit_type':'text',
                'required': False,
                'placeholder':'Street Address Line 2',
                'select_options':None},
            7: {'item': 'city',
                'label':'City',
                'edit_name':'editCity',
                'edit_type':'text',
                'required': True,
                'placeholder':'City',
                'select_options':None},
            8: {'item': 'state',
                'label':'State',
                'edit_name':'editState',
                'edit_type':'text',
                'required': True,
                'placeholder':'State',
                'select_options':None},
            9: {'item': 'postal_code',
                'label':'Postal Code',
                'edit_name':'editPostalCode',
                'edit_type':'text',
                'required': True,
                'placeholder':'98052',
                'select_options':None},
            10: {'item': 'country',
                'label':'Country',
                'edit_name':'editCountry',
                'edit_type':'text',
                'required': True,
                'placeholder':'USA',
                'select_options':None},
            11: {'item': 'email',
                'label':'School eMail',
                'edit_name':'editeMail',
                'edit_type':'text',
                'placeholder':'eMail Address',
                'select_options':None},
            12: {'item': 'phone',
                'label':'Region Phone',
                'edit_name':'editPhone',
                'edit_type':'text',
                'placeholder':'Phone',
                'select_options':None},
            13: {'item': 'status',
                'label':'Status',
                'edit_name':'editStatus',
                'edit_type':'select',
                'placeholder':'0',
                'select_options':self.select_status},
            14: {'item': 'standing',
                'label':'Standing',
                'edit_name':'editStanding',
                'edit_type':'select',
                'placeholder':'0',
                'select_options':self.select_standing}
            }

        # SQL Schema
        # Must match the attrs (attributes) above, line for line
        self.schema = ['region_id',
            'region_name',
            'region_abbrev',
            'main_reg_id',
            'reg_team_ids',
            'nat_area',
            'street',
            'street2',
            'city',
            'state',
            'postal_code',
            'country',
            'email',
            'phone',
            'status',
            'standing'
            ]

        # create the INSERT schema substituion string
        self.schema_insert = ", ".join(self.schema)

        # SQL Data Types for the SQL Schema
        # Must match the SQL Schema above, line for line
        self.types = ['integer primary key',
            'text',
            'text',
            'integer',
            'text',
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
        """ Region Object: _get method (private)
        Returns a tuple of the Region data
        Used by sql_insert """

        # assuming that dictiionaries are unordered
        # retrive the data in oder as a tuple
        results = []
        for key in self.schema:
            results.append(self.attrs[key])

        return tuple(results)

    # Method to set all region data from a SQL row tuple
    def _set (self, sql_data):
        """ Region Object: _set method (private)
        Sets Region data in the instance of the object.
        Used to set data from a sql query into the object.
        Parameters:
            sql_data - a 'row' tuple returned from a sql query for a region"""

        # copy the sql_data, a row, to self.attrs dictionary
        # use self.schema instead of self.attrs.keys() to interate
        # becaause the self.schema is a list and the order will not change
        i = 0
        for key in self.schema:
            self.attrs[key] = sql_data[i]
            i += 1

    def _sql_populate (self, c):
        """ Region Object: _sql_populate method (private)
        Populates the instance of Region from the database as a new row
        Parameters:
            c = cursor to database"""

        try:
            # Test 1, check for the SQL ID

            print(f"DEBUG: region._sql_populate region_id = {self.attrs['region_id']}")

            if self.attrs['region_id']:
                test = (self.attrs['region_id'], )
                c.execute('SELECT * FROM regions WHERE region_id=?', test)
            # Test 2, check for Region Name
            elif self.attrs['name']:
                test = (self.attrs['name'], )
                c.execute('SELECT * FROM regions WHERE name=?', test)
            else:
                # if you did't fill in any information to test, why did you call populate?
                return 1
        except Exception as e:
            print (f"ERROR: Region()._sql_populate: {e}")
            return 1    # return Error

        # check if a row is returned
        row = c.fetchone()
        if row:
            self._set(row)
            return 0
        else:
            return 1

    def _sql_insert (self, conn, c):
        """Region Object: _sql_insert method (private)
        Inserts the instance of Region into the database as a new row
        Parameters:
            conn = connection to database
            c = cursor to database"""

        # check if the region` already exists
        where = ' WHERE region_name = "' + str(self.attrs['region_name']) + '"'

        c.execute('SELECT * FROM regions' + where)
        row = c.fetchone()

        if row:
            return (1, "Region Already Exists")
        else:
            try:
                c.execute('INSERT INTO regions (' +  self.schema_insert + \
                    ') VALUES ' + self.schema_insert_sub, self._get())
            except:
                # Insert failed so return Error
                return (2, "Failed to add New Region!")

            # Save (commit) the changes
            conn.commit()

            # region_id is auto assigned on insert. So, retrive the region_id from the db
            name = (self.attrs['region_name'], )
            c.execute('SELECT region_id FROM regions WHERE region_name=?', name)
            row = c.fetchone()
            self.attrs['region_id'] = row[0]

            return (0, "Region Successfully Added!")

    def _sql_update (self, conn, c):
        """Region Object: _sql_update method (private)
        Commits all attribute in the instance of Region
        to the associated existing row in the database
        Parameters:
            conn = connection to database
            c = cursor to database"""

        if self.attrs['region_id'] is not None:
            try:
                # create the label = value string to UPDATE
                lvl = ''
                for label in self.schema:
                    lvl += label + ' = "' + str(self.attrs[label]) + '", '
                lvl = lvl [:-2]

                # update the row
                c.execute('UPDATE regions SET ' + lvl + \
                    ' WHERE region_id=' + str(self.attrs['region_id']))

                # Save (commit) the changes
                conn.commit()

                return 0    # return Success
            except Exception as e:
                print (f"ERROR: Region()._sql_update: {e}")
                return 1    # return Error
        else:
            print ("ERROR: Region()._sql_update: region_id not yet set")
            return 1    # return Error

    def _sql_delete (self, conn, c):
        """Region Object: _sql_delete method (private)
        Deletes the row in the database assoicated with the
        instance of School
        Parameters:
            conn = connection to database
            c = cursor to database"""

        # ??? Handle Exceptions Here ???
        if self.attrs['region_id'] is not None:
            try:
                # delete the row
                c.execute('DELETE FROM regions WHERE region_id=' + \
                    str(self.attrs['region_id']))

                # Save (commit) the changes
                conn.commit()

                return 0    # return Success
            except Exception as e:
                print (f"ERROR: Region()._sql_delete: {e}")
                return 1    # return Error
        else:
            print ("ERROR: Region()._sql_delete: region_id not yet set")
            return 1    # return Error

    def get (self, db):
        """ Region Object: get method
        Populates the instance of Region from the database as a new row
        Parameters:
            db = Database object from which to retrive the cursor"""

        return self._sql_populate (db.cursor)

    def put (self, db):
        """Region Object: put method
        Inserts the instance of Region into the database as a new row
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_insert(db.conn, db.cursor)

    # commit the data in Region to the DB
    def update (self, db):
        """Region Object: update method
        Commits all attributes in the instance of Region
        to the associated existing row in the database
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_update(db.conn, db.cursor)
