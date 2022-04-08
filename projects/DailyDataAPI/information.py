# information.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# for OYD Daily Program
#
from events import *
from school import *
from region import *
from natarea import *

# class Information: This class represents a single information.
# An "information" is a prospective student who contacted the school
# via a phone call, email, social media, or coming into the school.
# The schema for the database table for informations is defined
# by the Information() object
class Information(object):
    """ Information object:
        Attributes contained in Information.attrs dictionary:
            info_sql_id - internal use only, do not change
            school
            date
            first_name
            last_name
            age
            birth_date
            class_group - Adult, Junior, Child
            street, street2, city, state, postal_code - adddress info
            country - defaults to 'USA'
            email, mobile_phone, home_phone - contact info
            parental_contact
            how_found - how the information found school
            occupation
            interest - what is the info's interest in training
            body_issues - Injuries, Surgeries, Body Issues
            notes - notes and comments by instructor
            """

    def __init__(self,
        school=None, date=None,
        first_name=None, last_name=None,
        age=0, birth_date=None, class_group=None,
        street=None, street2=None, city=None, state=None, postal_code=None,
        country='USA', email=None, mobile_phone=None, home_phone=None,
        parental_contact=None,
        how_found=None, occupation=None, interest=None,
        body_issues=None, notes=None):
        """Information Object: __init__ Method
            Parameters:
                1) See help for the Object definition for all attributes.
                2) all attributes can be passed to __init__ as a Parameters
                   to initialize the instance"""


        # Dictionary of Student Attributes
        self._sql_id = None             # internal use only, do not change
        self.attrs = {'info_sql_id': None,   # internal use only, do not change
            'school': school,
            'date': date,
            'first_name': first_name,
            'last_name': last_name,
            'age': age,
            'birth_date': birth_date,
            'class_group': class_group,
            'street': street,
            'street2': street2,
            'city': city,
            'state': state,
            'postal_code': postal_code,
            'country': country,
            'email': email,
            'mobile_phone': mobile_phone,
            'home_phone': home_phone,
            'parental_contact': parental_contact,
            'how_found': how_found,
            'occupation': occupation,
            'interest': interest,
            'body_issues': body_issues,
            'notes': notes
            }

        self.select_class_group = {"adul":"Adult", "junior":"Junior",
            "child":"Child"}

        # Matching dictionary of Human Readable Titles for Information Atributes
        self.labels = {'info_sql_id': 'SQL ID',
            'school': 'School:',
            'date': 'Date:',
            'first_name': 'First Name:',
            'last_name': 'Last Name:',
            'age': 'Age:',
            'birth_date': 'Birth Date:',
            'class_group': 'Class:',
            'street': 'Street:',
            'street2': 'Street2:',
            'city': 'City:',
            'state': 'State / Prov:',
            'postal_code': 'Postal Code:',
            'country': 'Country:',
            'email': 'eMail:',
            'mobile_phone': 'Mobile Phone:',
            'home_phone': 'Home Phone:',
            'parental_contact': 'Parental Contact:',
            'how_found': 'How Found:',
            'occupation': 'Occupation:',
            'interest': 'Interest:',
            'body_issues': 'Body Issues:',
            'notes': 'Notes:'
            }

        # Matching dictionary of UI input types for Student Atributes
        self.label_types = {'info_sql_id': "hidden",
            'school': "number",           # select
            'date': "date",
            'first_name': "text",
            'last_name': "text",
            'age': "number",
            'birth_date': "date",
            'class_group': 'text',      # select
            'street': 'text',
            'street2': 'text',
            'city': 'text',
            'state': 'text',            # select
            'postal_code': 'text',
            'country': 'text',          # select
            'email': 'email',
            'mobile_phone': 'text',
            'home_phone': 'text',
            'parental_contact': 'text',
            'how_found': 'text',
            'occupation': 'text',
            'interest': 'text',
            'body_issues': 'text',
            'notes': 'text'
            }

        # SQL Schema
        # Must match the attrs (attributes) above, line for line
        self.schema = ['info_sql_id',
            'school',
            'date',
            'first_name',
            'last_name',
            'age',
            'birth_date',
            'class_group',
            'street',
            'street2',
            'city',
            'state',
            'postal_code',
            'country',
            'email',
            'mobile_phone',
            'home_phone',
            'parental_contact',
            'how_found',
            'occupation',
            'interest',
            'body_issues',
            'notes'
            ]

        # create the INSERT schema substituion string
        self.schema_insert = ", ".join(self.schema)

        # SQL Data Types for the SQL Schema
        # Must match the SQL Schema above, line for line
        self.types = ['integer primary key',
            'integer',
            'datetime',
            'text',
            'text',
            'integer',
            'datetime',
            'text',
            'text',
            'text',
            'text',
            'text',
            'text',
            'text',
            'text',
            'text',
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

        # print(f"DEBUG: Information.init limit = {limit}")
        # print(f"DEBUG: Informations.init len(self.schema) = {len(self.schema)}")
        # print(f"DEBUG: Informations.init len(self.types) = {len(self.types)}")

        i = 0
        for i in range(0, limit):
            addstr = self.schema[i] + ' ' + self.types[i] + ', '
            self.schema_create += addstr
        self.schema_create += self.schema[limit] + ' ' + self.types[limit]

        # VALUE substitution string
        self.schema_insert_sub = '(' + '?,' * (len(self.schema) - 1) + '?)'

    # Method to get a tuuple of all student data
    def _get (self):
        """ Information Object: _get method (private)
        Returns a tuple of the Student data
        Used by sql_insert_new """

        # assuming that dictiionaries are unordered
        # retrive the data in oder as a tuple
        results = []
        for key in self.schema:
            results.append(self.attrs[key])

        return tuple(results)

    # Method to set all student data from a SQL row tuple
    def _set (self, sql_data):
        """ Information Object: _set method (private)
        Sets Information data in the instance of the object.
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

        # set separate _sql_id used for internal consistencu
        self._sql_id = self.attrs['info_sql_id']

    def _sql_populate (self, c):
        """ Information Object: _sql_populate method (private)
        Populates the instance of Information from the database as a new row
        Parameters:
            c = cursor to database"""

        try:
            # Test 0, check for the SQL ID
            if self.attrs['info_sql_id']:
                test = (self.attrs['info_sql_id'], )
                c.execute('SELECT * FROM informations WHERE info_sql_id=?', test)
            # Test #1, check for First, Last Name & School
            elif self.attrs['last_name'] and self.attrs['first_name'] \
                and self.attrs['school']:
                test = (self.attrs['first_name'], self.attrs['last_name'],
                    self.attrs['school'])
                c.execute('SELECT * FROM informations WHERE first_name=? AND \
                    last_name=? and school=?', test)
            else:
                # if you did't fill in any information to test, why did you call populate?
                return 1
        except Exception as e:
            print (f"ERROR: _set_populate: {e}")
            return 1    # return Error

        # check if a row is returned
        row = c.fetchone()
        if row:
            self._set(row)
            return 0
        else:
            return 1

    def _sql_insert (self, db, conn, c):
        """Information Object: _sql_insert_new method (private)
        Inserts the instance of Information to the database as a new row
        Parameters:
            conn = connection to database
            c = cursor to database"""

        try:
            c.execute('INSERT INTO informations (' +  self.schema_insert + \
                ') VALUES ' + self.schema_insert_sub, self._get())
        except:
            # Insert failed so return Error
            return (1, 'Failed to insert new Information into Database')

        # Save (commit) the changes
        conn.commit()

        # student_sql_id is auto assigned on insert. So, retrive the student_sql_id from the db
        name = (self.attrs['first_name'], self.attrs['last_name'],
            self.attrs['school'])
        c.execute('SELECT info_sql_id FROM informations WHERE first_name=? AND \
            last_name=? AND school=?', name)
        row = c.fetchone()
        self.attrs['info_sql_id'] = row[0]
        self._sql_id = row[0]

        # look up the school name, region name, and nat_area name
        # for writing the Master Events Table which is de-normalized
        school = School()
        school.school_id = self.attrs['school']
        school.get(db)
        region = Region()
        region.region_id = school.attrs['school_region']
        region.get(db)
        nat_area = NatArea ()
        nat_area.nat_area_id = region.attrs['nat_area']
        nat_area.get(db)

        # write an event to the Master Events Tables
        me = Master_Event(event = 'info', date = self.attrs['date'],
            info_sql_id = self.attrs['info_sql_id'],
            nat_area_name = nat_area.attrs['area_name'],
            region_name = region.attrs['region_name'],
            school_name = school.attrs['school_name'],
            age = self.attrs['age'],
            first_name = self.attrs['first_name'],
            last_name = self.attrs['last_name'],
            occupation = self.attrs['occupation'])
        me.put(db)

        return (0, 'New Information Added to Database')

    def _sql_update_attr (self, conn, c, label):
        """Information Object: _sql_update_attr method (private)
        Updates a specific attribute in the instance of Information
        to the associated existing row in the database
        Parameters:
            conn = connection to database
            c = cursor to database
            label = name of attribute to be udpated to db
            attr = attribute to be updated"""

        if self._sql_id is not None:
            try:
                c.execute('UPDATE informations SET ' + label + ' = "' + \
                    str(self.attrs[label]) + '" WHERE info_sql_id=' + str(self._sql_id))

                # Save (commit) the changes
                conn.commit()

                return 0    # return Success
            except Exception as e:
                print (f"ERROR: _set_update_attr: {e}")
                return 1    # return Error
        else:
            print ("ERROR: _set_update_attr: _sql_id not yet set")
            return 1    # return Error

    def _sql_commit (self, conn, c):
        """Information Object: _sql_commit method (private)
        Commits all attribute in the instance of Information
        to the associated existing row in the database
        Parameters:
            conn = connection to database
            c = cursor to database"""

        if self._sql_id is not None:
            try:
                # create the label = value string to UPDATE
                lvl = ''
                for label in self.schema:
                    lvl += label + ' = "' + str(self.attrs[label]) + '", '
                lvl = lvl [:-2]

                # update the row
                c.execute('UPDATE informations SET ' + lvl + \
                    ' WHERE info_sql_id=' + str(self._sql_id))

                # Save (commit) the changes
                conn.commit()

                return 0    # return Success
            except Exception as e:
                print (f"ERROR: _set_commit: {e}")
                return 1    # return Error
        else:
            print ("ERROR: _set_commit: _sql_id not yet set")
            return 1    # return Error

    def get (self, db):
        """ Information Object: get method
        Populates the instance of Information from the database as a new row
        Parameters:
            db = Database object from which to retrive the cursor"""

        return self._sql_populate (db.cursor)

    def put (self, db):
        """Information Object: put method
        Inserts the instance of Student into the database as a new row
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_insert(db, db.conn, db.cursor)

    def update_attr (self, db, label):
        """Information Object: update_attr method
        Updates a specific attribute in the instance of Information
        to the associated existing row in the database
        Parameters:
            db = Database object that contains the
                connection & cursor to database
            label = name of attribute to be udpated to db
            attr = attribute to be updated"""

        return self._sql_update_attr(db.conn, db.cursor, label)

    #    commit the data in Student to the DB
    def update (self, db):
        """Information Object: update method
        Commits all attributes in the instance of Information
        to the associated existing row in the database
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_commit(db.conn, db.cursor)
