# course.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# for OYD Daily Program

# class Courses_Table - used to query lists of courses
# Note: the schema for the Courses_Table() is defined in the School() object
class Courses_Table(object):
    def __init__(self):
        self.courses = []
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
        c.execute('SELECT * FROM courses' + limoff)
        row = c.fetchone()

        # check if a row was returned
        if row:
            # store all rows in the list
            while row:
                self.courses.append(row)
                row = c.fetchone()

            # return success
            return 0
        else:
            # return ERROR
            return 1

    # Count
    def count(self, db):
        """ Courses_Table.count() function
            Returns number of rows in Courses table
            Parameters:
                db - Database() object
            Returns:
                number of rows in courses table"""
        try:
            c = db.cursor

            # execute the query for all users in the database
            c.execute('SELECT count(*) FROM courses')
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
        # invalidate amy previous query results
        self.courses = []
        self.limit = limit
        self.offset = offset

        return self._sql_query (c=db.cursor, limit=limit, offset=offset)

    # Query for All Students in the Database
    def query_all(self, db):
        self.courses = []
        self.limit = None
        self.offset = None

        return self._sql_query (c = db.cursor)


# class Course - used to manage available OYD Courses
# includes the Schema for the Courses Table - courses
class Course(object):
    """ Course object:
        Attributes contained in Course.attrs dictionary:
            course_id - provided by system, do not set
            course_name - full text name of course name
            course_abbrev - abbbreviation of course name"""

    def __init__(self, course_name=None, course_abbrev=None):
        """ Master_Event Object: __init__ Method
            Parameters:
            1) See help for the Object definition for all attributes.
            2) all attributes can be passed to __init__ as a Parameters
               to initialize the instance"""

        # Dictionary of New_Students_Event atrributes
        self.attrs = {'course_id': None,
                    'course_name': course_name,
                    'course_abbrev': course_abbrev
                    }

        # SQL Schema
        # Must match the attrs (attributes) above, line for line
        self.schema = ['course_id',
            'course_name',
            'course_abbrev'
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

    def _get (self):
        """ Course Object: _get method (private)
        Returns a tuple of the Course data
        Used by _sql_insert """

        # assuming that dictiionaries are unordered
        # retrive the data in oder as a tuple
        results = []
        for key in self.schema:
            results.append(self.attrs[key])

        return tuple(results)

    # Method to set all course data from a SQL row tuple
    def _set (self, sql_data):
        """ Course Object: _set method (private)
        Sets Coure data in the instance of the object.
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
        """ Course Object: _sql_populate method (private)
        Populates the instance of Course from the database as a new row
        Parameters:
            c = cursor to database"""

        try:
            # Test 1, check for the SQL ID
            if self.attrs['course_id']:
                test = (self.attrs['course_id'], )
                c.execute('SELECT * FROM courses WHERE course_id=?', test)
            # Test 2, check for Course Name
            elif self.attrs['course_name']:
                test = (self.attrs['course_name'], )
                c.execute('SELECT * FROM courses WHERE course_name=?', test)
            else:
                # if you did't fill in any information to test, why did you call populate?
                return 1
        except Exception as e:
            print (f"ERROR: Course()._sql_populate: {e}")
            return 1    # return Error

        # check if a row is returned
        row = c.fetchone()
        if row:
            self._set(row)
            return 0
        else:
            return 1

    def _sql_insert (self, conn, c):
        """Course Object: _sql_insert method (private)
        Inserts the instance of Course into the database as a new row
        Parameters:
            conn = connection to database
            c = cursor to database"""

        try:
            c.execute('INSERT INTO courses (' +  self.schema_insert + \
                ') VALUES ' + self.schema_insert_sub, self._get())
        except:
            # Insert failed so return Error
            return 1

        # Save (commit) the changes
        conn.commit()

        return 0

    def _sql_update (self, conn, c):
        """Course Object: _sql_update method (private)
        Commits all attribute in the instance of Course
        to the associated existing row in the database
        Parameters:
            conn = connection to database
            c = cursor to database"""

        if self.attrs['course_id'] is not None:
            try:
                # create the label = value string to UPDATE
                lvl = ''
                for label in self.schema:
                    lvl += label + ' = "' + str(self.attrs[label]) + '", '
                lvl = lvl [:-2]

                # update the row
                c.execute('UPDATE courses SET ' + lvl + \
                    ' WHERE course_id=' + str(self.attrs['course_id']))

                # Save (commit) the changes
                conn.commit()

                return 0    # return Success
            except Exception as e:
                print (f"ERROR: Course()._sql_update: {e}")
                return 1    # return Error
        else:
            print ("ERROR: Course()._sql_update: sql_id not yet set")
            return 1    # return Error

    def get (self, db):
        """ Course Object: get method
        Populates the instance of Course from the database as a new row
        Parameters:
            db = Database object from which to retrive the cursor"""

        return self._sql_populate (db.cursor)

    def put (self, db):
        """Course Object: put method
        Inserts the instance of Course into the database as a new row
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_insert(db.conn, db.cursor)

    # commit the data in Course to the DB
    def update (self, db):
        """Course Object: update method
        Commits all attributes in the instance of Course
        to the associated existing row in the database
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_update(db.conn, db.cursor)
