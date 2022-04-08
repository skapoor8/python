# events.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# for OYD Daily Program

# class Master_Event - used to track all OYD Daily Program events
# includes the Schema for the Master Events Table - masterevents
class Master_Event(object):
    """ Master_Event object:
        Attributes contained in Master_Event.attrs dictionary:
            sql_id - from Student object
            event - values: info, newstudent, attendance, mlt-attendance, ncourse, test, drop
            date - date of event
            student_sql_id - student's sql id from Student table if Studen event
            info_sql_id - information's sql id from Informations Table
            nat_area_name - student or informatoion's national area
            region_name - student or information's region
            school_name - student or information's school
            first_name - student or information's first name
            last_name - student or information's last name
            age - student or information's age
            occupation - student or information's occupation
            rank - student's rank (if student related event)
            rank_tested - rank for which the student tested (if testing event)
            pass_fail - pass or fail for rank tested (if testing event)
            course_name - name of course (if mlt-attendance event)
            """

    def __init__(self, event=None, date=None, student_sql_id=None, info_sql_id=None,
        nat_area_name=None, region_name=None, school_name=None,
        first_name=None, last_name=None,
        age = None, occupation=None,
        rank=None, rank_tested=None, pass_fail=None,
        course_name=None):
        """ Master_Event Object: __init__ Method
            Parameters:
            1) See help for the Object definition for all attributes.
            2) all attributes can be passed to __init__ as a Parameters
               to initialize the instance"""

        # Dictionary of New_Students_Event atrributes
        self.attrs = {'sql_id': None,
                    'event': event,
                    'date': date,
                    'student_sql_id': student_sql_id,
                    'info_sql_id': info_sql_id,
                    'nat_area_name': nat_area_name,
                    'region_name': region_name,
                    'school_name': school_name,
                    'first_name': first_name,
                    'last_name': last_name,
                    'age': age,
                    'occupation': occupation,
                    'rank': rank,
                    'rank_tested': rank_tested,
                    'pass_fail': pass_fail,
                    'course_name': course_name
                    }

        # SQL Schema
        # Must match the attrs (attributes) above, line for line
        self.schema = ['sql_id',
            'event',
            'date',
            'student_sql_id',
            'info_sql_id',
            'nat_area_name',
            'region_name',
            'school_name',
            'first_name',
            'last_name',
            'age',
            'occupation',
            'rank',
            'rank_tested',
            'pass_fail',
            'course_name'
            ]

        # create the INSERT schema substituion string
        self.schema_insert = ", ".join(self.schema)

        # SQL Data Types for the SQL Schema
        # Must match the SQL Schema above, line for line
        self.types = ['integer primary key',
            'text',
            'datetime',
            'integer',
            'integer',
            'text',
            'text',
            'text',
            'text',
            'text',
            'integer',
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
        """ Master_Event Object: _get method (private)
        Returns a tuple of the Master_Event data
        Used by _sql_insert """

        # assuming that dictiionaries are unordered
        # retrive the data in oder as a tuple
        results = []
        for key in self.schema:
            results.append(self.attrs[key])

        return tuple(results)

    def _sql_insert (self, db):
        """Master_Event Object: _sql_insert method (private)
        Inserts the instance of Master Event into the database as a new row
        Parameters:
            db = database"""

        conn = db.conn
        c = db.cursor

        try:
            c.execute('INSERT INTO masterevents (' +  self.schema_insert + \
                ') VALUES ' + self.schema_insert_sub, self._get())
        except:
            # Insert failed so return Error
            return 1

        # Save (commit) the changes
        conn.commit()

        return 0

    def put (self, db):
        """Master_Event Object: put method
        Inserts the instance of Master_Event into the database as a new row
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_insert(db)

# class New_Students_Event - used to track new student events
# includes the Schema for the New Student Events Table - newstudents
class New_Students_Event(object):
    """ New_Students_Event object:
        Attributes contained in New_Students_Event.attrs dictionary:
            student_sql_id - from Student object
            oyd_id - Oom Yung Doe ID from Student object
            signup_date - start_date from Student object"""

    def __init__(self, student_sql_id=None, oyd_id=None, signup_date=None):
        """ New_Students_Event Object: __init__ Method
            Parameters:
            1) See help for the Object definition for all attributes.
            2) all attributes can be passed to __init__ as a Parameters
               to initialize the instance"""

        # Dictionary of New_Students_Event atrributes
        self.attrs = {'sql_id': None,
                    'student_sql_id': student_sql_id,
                    'oyd_id': oyd_id,
                    'signup_date': signup_date
                    }

        # SQL Schema
        # Must match the attrs (attributes) above, line for line
        self.schema = ['sql_id',
            'student_sql_id',
            'oyd_id',
            'signup_date'
            ]

        # create the INSERT schema substituion string
        self.schema_insert = ", ".join(self.schema)

        # SQL Data Types for the SQL Schema
        # Must match the SQL Schema above, line for line
        self.types = ['integer primary key',
            'integer',
            'integer',
            'datetime'
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
        """ New_Student_Event Object: _get method (private)
        Returns a tuple of the New_Student_Event data
        Used by _sql_insert """

        # assuming that dictiionaries are unordered
        # retrive the data in oder as a tuple
        results = []
        for key in self.schema:
            results.append(self.attrs[key])

        return tuple(results)

    def _sql_insert (self, db):
        """New_Students_Event Object: _sql_insert method (private)
        Inserts the instance of New Student to the database as a new row
        Parameters:
             db = database"""

        conn = db.conn
        c = db.cursor

        try:
            c.execute('INSERT INTO newstudents (' +  self.schema_insert + \
                ') VALUES ' + self.schema_insert_sub, self._get())

        except:
            # Insert failed so return Error
            return 1

        # Save (commit) the changes
        conn.commit()

        return 0

    def put (self, db):
        """New_Students_Event Object: put method
        Inserts the instance of New_Students_Event into the database as a new row
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_insert(db)

# class Testing_Event - used to track student testing events
# includes the Schema for the Testing Events Table - testingevents
class Testing_Event(object):
    """ Testing_Event object:
        Attributes contained in Testing_Event.attrs dictionary:
            student_sql_id - from Student object
            oyd_id - Oom Yung Doe ID from Student object
            test_date - date of test_date
            rank_tested - Two digit rank value (1S - 7D)
            pass_fail - Pass, Fail"""

    def __init__(self, student_sql_id=None, oyd_id=None, test_date=None,
        rank_tested=None, pass_fail=None):
        """ Testing_Event Object: __init__ Method
            Parameters:
            1) See help for the Object definition for all attributes.
            2) all attributes can be passed to __init__ as a Parameters
               to initialize the instance"""

        # Dictionary of New_Students_Event atrributes
        self.attrs = {'sql_id': None,
                    'student_sql_id': student_sql_id,
                    'oyd_id': oyd_id,
                    'test_date': test_date,
                    'rank_tested': rank_tested,
                    'pass_fail': pass_fail
                    }

        # SQL Schema
        # Must match the attrs (attributes) above, line for line
        self.schema = ['sql_id',
            'student_sql_id',
            'oyd_id',
            'test_date',
            'rank_tested',
            'pass_fail'
            ]

        # create the INSERT schema substituion string
        self.schema_insert = ", ".join(self.schema)

        # SQL Data Types for the SQL Schema
        # Must match the SQL Schema above, line for line
        self.types = ['integer primary key',
            'integer',
            'integer',
            'datetime',
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
        """ Testing_Event Object: _get method (private)
        Returns a tuple of the Testing_Event data
        Used by _sql_insert """

        # assuming that dictiionaries are unordered
        # retrive the data in oder as a tuple
        results = []
        for key in self.schema:
            results.append(self.attrs[key])

        return tuple(results)

    def _sql_insert (self, db):
        """Testing_Event Object: _sql_insert method (private)
        Inserts the instance of Testing Event to the database as a new row
        Parameters:
            db = database"""

        conn = db.conn
        c = db.cursor

        try:
            c.execute('INSERT INTO testingevents (' +  self.schema_insert + \
                ') VALUES ' + self.schema_insert_sub, self._get())

            # write an event to the Master Events Tables
            test_event_txt = 'test - ' + self.attrs['pass_fail']
            me = Master_Event(test_event_txt, self.attrs['test_date'],
                self.attrs['student_sql_id'])
            me.put(db)
        except:
            # Insert failed so return Error
            return 1

        # Save (commit) the changes
        conn.commit()

        return 0

    def put (self, db):
        """Testing_Event Object: put method
        Inserts the instance of Testing_Event into the database as a new row
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_insert(db)

# class Drop_Event - used to track student drop events
# includes the Schema for the Drop Events Table - dropevents
class Drop_Event(object):
    """ Drop_Event object:
        Attributes contained in Drop_Event.attrs dictionary:
            student_sql_id - from Student object
            oyd_id - Oom Yung Doe ID from Student object
            drop_date - Date Dropped
            reason - Reason provided by student for dropping"""

    def __init__(self, student_sql_id=None, oyd_id=None, drop_date=None,
        reason=None):
        """ Drop_Event Object: __init__ Method
            Parameters:
            1) See help for the Object definition for all attributes.
            2) all attributes can be passed to __init__ as a Parameters
               to initialize the instance"""

        # Dictionary of New_Students_Event atrributes
        self.attrs = {'sql_id': None,
                    'student_sql_id': student_sql_id,
                    'oyd_id': oyd_id,
                    'drop_date': drop_date,
                    'reason': reason
                    }

        # SQL Schema
        # Must match the attrs (attributes) above, line for line
        self.schema = ['sql_id',
            'student_sql_id',
            'oyd_id',
            'drop_date',
            'reason'
            ]

        # create the INSERT schema substituion string
        self.schema_insert = ", ".join(self.schema)

        # SQL Data Types for the SQL Schema
        # Must match the SQL Schema above, line for line
        self.types = ['integer primary key',
            'integer',
            'integer',
            'datetime',
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
        """ Drop_Event Object: _get method (private)
        Returns a tuple of the New_Student_Event data
        Used by _sql_insert """

        # assuming that dictiionaries are unordered
        # retrive the data in oder as a tuple
        results = []
        for key in self.schema:
            results.append(self.attrs[key])

        return tuple(results)

    def _sql_insert (self, db):
        """Drop_Event Object: _sql_insert method (private)
        Inserts the instance of Drop Event to the database as a new row
        Parameters:
            db = database"""

        conn = db.conn
        c = db.cursor

        try:
            c.execute('INSERT INTO dropevents (' +  self.schema_insert + \
                ') VALUES ' + self.schema_insert_sub, self._get())

        except:
            # Insert failed so return Error
            return 1

        # Save (commit) the changes
        conn.commit()

        return 0

    def put (self, db):
        """Drop_Event Object: put method
        Inserts the instance of Drop_Event into the database as a new row
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_insert(db)
