# student.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# for OYD Daily Program
#
# class Student_Table - used to query lists of students
# Note: the schema for the Students_Table() is defined in the Student() object
from datetime import datetime
from events import *
from school import *
from region import *
from natarea import *

class Students_Table(object):
    def __init__(self):
        self._school = None
        self.students = []
        self.students_active = []
        self.students_inactive = []
        self.students_dropped = []

        self.count_active_instr = {'total':0}
        self.count_active_adult = {'total':0}
        self.count_active_junior = {'total':0}
        self.count_active_child = {'total':0}

        self.count_inactive_instr = {'total':0}
        self.count_inactive_adult = {'total':0}
        self.count_inactive_junior = {'total':0}
        self.count_inactive_child = {'total':0}

        self.count_dropped_instr = {'total':0}
        self.count_dropped_adult = {'total':0}
        self.count_dropped_junior = {'total':0}
        self.count_dropped_child = {'total':0}

        self.limit = None
        self.offset = None

    @property
    def school(self):
        return self._school

    @school.setter
    def school(self, school):
        if school != self._school:
            self._school = school
            self._reset_results()

    # Reset the query results
    def _reset_results(self):
        self.students = []
        self.students_active = []
        self.students_inactive = []
        self.students_dropped = []

        self.count_active_instr = {'total':0}
        self.count_active_adult = {'total':0}
        self.count_active_junior = {'total':0}
        self.count_active_child = {'total':0}

        self.count_inactive_instr = {'total':0}
        self.count_inactive_adult = {'total':0}
        self.count_inactive_junior = {'total':0}
        self.count_inactive_child = {'total':0}

        self.count_dropped_instr = {'total':0}
        self.count_dropped_adult = {'total':0}
        self.count_dropped_junior = {'total':0}
        self.count_dropped_child = {'total':0}

        self.limit = None
        self.offset = None

    # Exectue the SQL query to get All Student from the Database
    # ??? modify this to allow for query by a single nat_area, region, schoool
    def _sql_query_all (self, c):
        # query for all students in the database
        c.execute('SELECT * FROM students')
        row = c.fetchone()

        # check if a row was returned
        if row:
            # store all rows in the list
            while row:
                self.students.append(row)
                row = c.fetchone()

            # return success
            return 0
        else:
            # return ERROR
            return 1

    # Exectue the SQL query to get Student from the Database based on Parameters
    #   - status, nat_area, region, and school
    def _sql_query (self, c, status=None, limit=None, offset=None):

        # build the WHERE clause
        test_params = {'status': status, 'school': self.school}
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

        # execute the query for selected students in the database
        c.execute('SELECT * FROM students' + where + limoff)
        row = c.fetchone()

        # check if a row was returned
        if row:
            # store all rows in the list
            while row:
                if status == 'active':
                    self.students_active.append(row)
                elif status == 'dropped':
                    self.students_dropped.append(row)
                else:
                    self.students.append(row)
                row = c.fetchone()

            # return success
            return 0
        else:
            # return ERROR
            return 1

    # Count
    def count(self, db, status=None):
        """ Student_Table.count() function
            Returns number of rows in students table meeting the parameters
            from the school, region, national area already set in the object
            Parameters:
                db - Database() object
                status - student status, default None
            Returns:
                number of rows in student table meeting the parameters"""

        try:
            c = db.cursor

            # build the WHERE clause
            test_params = {'status': status, 'school': self.school}
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
            c.execute('SELECT count(*) FROM students' + where)
            row = c.fetchone()

            # check if result otherwise return None
            if row:
                return row[0]
            else:
                return None
        except:
            return None

    # Count by Rank
    def count_rank(self, db, status=None, class_group=None):
        """ Student_Table.count_rank() function
            Returns number of rows in students table meeting the parameters
            from the school already set in the object
            by rank
            Parameters:
                db - Database() object
                status - student status, default None
                class_group - Instructor, Adult, Junior, Child, default = None
            Returns:
                """
        try:
            c = db.cursor

            # query by rank
            for rank in Student().select_rank.keys():

                # ??? change this to:
                # select class_group, rank, count(*) from students where
                #       {see below - class_group, rank} group
                #       by class_group, rank
                # convert result into appropraite dictionary

                # build the WHERE clause
                test_params = {'status': status, 'school': self.school,
                    'rank': rank, 'class_group' : class_group}
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
                c.execute('SELECT count(*) FROM students' + where)
                row = c.fetchone()

                # check if result otherwise return None
                if row:
                    result = row[0]
                else:
                    result = 0

                print(f"DEBUG.student.stud_table.count_rank class_group = {class_group} status = {status} rank = {rank}, result = {result}")

                if class_group == 'Instructor':
                    if status == 'active':
                        self.count_active_instr[rank] = result
                        self.count_active_instr['total'] += result
                    elif status == 'inactive':
                        self.count_inactive_instr[rank] = result
                        self.count_inactive_instr['total'] += result
                    elif status == 'dropped':
                        self.count_dropped_instr[rank] = result
                        self.count_dropped_instr['total'] += result
                elif class_group == 'Adult':
                    if status == 'active':
                        self.count_active_adult[rank] = result
                        self.count_active_adult['total'] += result
                    elif status == 'inactive':
                        self.count_inactive_adult[rank] = result
                        self.count_inactive_adult['total'] += result
                    elif status == 'dropped':
                        self.count_dropped_adult[rank] = result
                        self.count_dropped_adult['total'] += result
                elif class_group == 'Junior':
                    if status == 'active':
                        self.count_active_junior[rank] = result
                        self.count_active_junior['total'] += result
                    elif status == 'inactive':
                        self.count_inactive_junior[rank] = result
                        self.count_inactive_junior['total'] += result
                    elif status == 'dropped':
                        self.count_dropped_junior[rank] = result
                        self.count_dropped_junior['total'] += result
                elif class_group == 'Child':
                    if status == 'active':
                        self.count_active_child[rank] = result
                        self.count_active_child['total'] += result
                    elif status == 'inactive':
                        self.count_inactive_child[rank] = result
                        self.count_inactive_child['total'] += result
                    elif status == 'dropped':
                        self.count_dropped_child[rank] = result
                        self.count_dropped_child['total'] += result
            return 0, "success"
        except Exception as e:
            print(f"DEBUG.roster.Stud_Table.count_rank - excpetion = {e}")
            return 1, e

    # Query for a range of Students in the Database
    def query_range(self, db, limit, offset, status=None):
        self.limit = limit
        self.offset = offset

        return self._sql_query (c=db.cursor, limit=limit, offset=offset, status=status)

    # General Query where status can be supplied
    def query(self, db, status=None):
        return self._sql_query (c = db.cursor, status = status)

    # Query for All Students in the Database
    def query_all(self, db):
        return self._sql_query (c = db.cursor)

    # Query for Active Students in the Database
    def query_active(self, db):
        return self._sql_query (c = db.cursor, status='active')

    # Query for Active Students in the Database
    def query_dropped(self, db):
        return self._sql_query (c = db.cursor, status='dropped')

# class Student: This class represents a single student
# the schema for the database table for students is defined
# by the Student() object
class Student(object):
    """ Student object:
        Attributes contained in Student.attrs dictionary:
            student_sql_id - internal use only, do not change
            oyd_id - Oom Yung Doe ID
            first_name
            middle_name - defaults to an empty string
            last_name
            nickname
            age
            birth_date
            school - school number from schools table
            start_date
            status - defaults to 'active'
            drop_reason - reason for dropping
            position - defaults to empty string
            rank
            next_rank
            class_group - instructor, adult, junior, child
            street, street2, city, state, postal_code - adddress info
            country - defaults to 'USA'
            email, mobile_phone, home_phone - contact info
            parental_contact
            occupation
            how_found
            intern_points
            last_test_date
            next_test_date
            facebook
            instagram
            twitter"""

    def __init__(self, oyd_id=None,
        first_name=None, middle_name='', last_name=None, nickname=None,
        age=0, birth_date=None,
        school=0,
        start_date=None, status="active", drop_reason=None,
        position='', rank=None, next_rank=None, class_group=None,
        street=None, street2=None, city=None, state=None, postal_code=None,
        country='USA', email=None, mobile_phone=None, home_phone=None,
        parental_contact=None,
        occupation=None, how_found=None,
        intern_points=0,
        last_test_date=None, next_test_date=None,
        facebook=None, instagram=None, twitter=None):
        """Student Object: __init__ Method
            Parameters:
                1) See help for the Object definition for all attributes.
                2) all attributes can be passed to __init__ as a Parameters
                   to initialize the instance"""

        # Dictionary of Student Attributes
        self._sql_id = None             # internal use only, do not change
        self.attrs = {'student_sql_id': None,   # internal use only, do not change
            'oyd_id': oyd_id,
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'nickname': nickname,
            'age': age,
            'birth_date': birth_date,
            'school': school,
            'start_date': start_date,
            'status': status,
            'drop_reason': drop_reason,
            'position': position,
            'rank': rank,
            'next_rank': next_rank,
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
            'occupation': occupation,
            'how_found': how_found,
            'intern_points': intern_points,
            'last_test_date': last_test_date,
            'next_test_date': next_test_date,
            'facebook': facebook,
            'instagram': instagram,
            'twitter': twitter
            }

        self.select_status = {
            "All":None, "Active":"active", "Inactive":"inactive",
            "Dropped":"dropped"}

        self.select_position = {
            "None":"None", "AI":"AI", "I":"Instr", "AHI":"AHI", "HI":"HI",
            "ARHI":"ARHI", "RHI":"RHI", "ANI":"ANI", "NI":"NI"}

        self.select_rank = {"WB":"WB", "1S":"1S", "2S":"2S", "3S":"3S",
            "4S":"4S", "5S":"5S", "6S":"6S", "1D":"1D", "2D":"2D",
            "3D":"3D", "4D":"4D", "5D":"5D", "6D":"6D", "7D":"7D"}

        self.select_next_rank = {"1S":"1S", "2S":"2S", "3S":"3S", "4S":"4S",
            "5S":"5S", "6S":"6S", "1D":"1D", "2D":"2D", "3D":"3D",
            "4D":"4D", "5D":"5D", "6D":"6D", "7D":"7D", "8D":"8D"}

        self.select_class_group = {"instr":"Instr", "adul":"Adult", "junior":"Junior",
            "child":"Child"}

        # Matching dictionary of Human Reacable Titles for Student Atributes
        self.labels = {'student_sql_id': 'SQL ID',
            'oyd_id': 'OYD ID:',
            'first_name': 'First Name:',
            'middle_name': 'Middle Name:',
            'last_name': 'Last Name:',
            'nickname': 'Nickname:',
            'age': 'Age:',
            'birth_date': 'Birth Date:',
            'school': 'School:',
            'start_date': 'Start Date:',
            'status': 'Status:',
            'drop_reason': 'Drop Reason:',
            'position': 'Position:',
            'rank': 'Rank:',
            'next_rank': 'Next Rank:',
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
            'occupation': 'Occupation:',
            'how_found': 'How Found School:',
            'intern_points': 'Intern Points:',
            'last_test_date': 'Last Test Date:',
            'next_test_date': 'Next Test Date:',
            'facebook': 'Facebook:',
            'instagram': 'Instagram',
            'twitter': 'Twitter:'
            }

        # Matching dictionary of UI input types for Student Atributes
        self.label_types = {'student_sql_id': "hidden",
            'oyd_id': 'number',
            'first_name': "text",
            'middle_name': "text",
            'last_name': "text",
            'nickname': "text",
            'age': "number",
            'birth_date': 'date',
            'school': 'number',         # select
            'start_date': 'date',
            'status': 'text',           # select
            'drop_reason': 'text',
            'position': 'text',         # select
            'rank': 'text',             # select
            'next_rank': 'text',        # select
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
            'occupation': 'text',
            'how_found': 'text',
            'intern_points': 'number',
            'last_test_date': 'date',
            'next_test_date': 'date',
            'facebook': 'text',
            'instagram': 'text',
            'twitter': 'text'
            }

        # SQL Schema
        # Must match the attrs (attributes) above, line for line
        self.schema = ['student_sql_id',
            'oyd_id',
            'first_name',
            'middle_name',
            'last_name',
            'nickname',
            'age',
            'birth_date',
            'school',
            'start_date',
            'status',
            'drop_reason',
            'position',
            'rank',
            'next_rank',
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
            'occupation',
            'how_found',
            'intern_points',
            'last_test_date',
            'next_test_date',
            'facebook',
            'instagram',
            'twitter'
            ]

        # create the INSERT schema substituion string
        self.schema_insert = ", ".join(self.schema)

        # SQL Data Types for the SQL Schema
        # Must match the SQL Schema above, line for line
        self.types = ['integer primary key',
            'integer',
            'text',
            'text',
            'text',
            'text',
            'integer',
            'datetime',
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
            'text',
            'text',
            'text',
            'integer',
            'datetime',
            'datetime',
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

    # Method to get a tuuple of all student data
    def _get (self):
        """ Student Object: _get method (private)
        Returns a tuple of the Student data
        Used by _sql_insert """

        # assuming that dictiionaries are unordered
        # retrive the data in oder as a tuple
        results = []
        for key in self.schema:
            results.append(self.attrs[key])

        return tuple(results)

    # Method to set all student data from a SQL row tuple
    def _set (self, sql_data):
        """ Student Object: _set method (private)
        Sets Student data in the instance of the object.
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
        self._sql_id = self.attrs['student_sql_id']

    def _sql_populate (self, c):
        """ Student Object: _sql_populate method (private)
        Populates the instance of Student from the database as a new row
        Parameters:
            c = cursor to database"""

        try:
            # Test 0, check for the SQL ID
            if self.attrs['student_sql_id']:
                test = (self.attrs['student_sql_id'], )
                c.execute('SELECT * FROM students WHERE student_sql_id=?', test)
            # Test 1, check for the OYD ID
            elif self.attrs['oyd_id']:
                test = (self.attrs['oyd_id'], )
                c.execute('SELECT * FROM students WHERE oyd_id=?', test)
            # Test #2, check for First, Last Name & School
            elif self.attrs['last_name'] and self.attrs['first_name'] \
                and self.attrs['school']:
                test = (self.attrs['first_name'], self.attrs['last_name'],
                    self.attrs['school'])
                c.execute('SELECT * FROM students WHERE first_name=? AND \
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
        """Student Object: _sql_insert method (private)
        Inserts the instance of Student to the database as a new row
        Parameters:
            conn = connection to database
            c = cursor to database"""

        try:
            c.execute('INSERT INTO students (' +  self.schema_insert + \
                ') VALUES ' + self.schema_insert_sub, self._get())
        except:
            # Insert failed so return Error
            return (1, "Failed to insert new Student into Database")

        # Save (commit) the changes
        conn.commit()

        # student_sql_id is auto assigned on insert. So, retrive the student_sql_id from the db
        name = (self.attrs['first_name'], self.attrs['last_name'],
            self.attrs['school'])
        c.execute('SELECT student_sql_id FROM students WHERE first_name=? AND \
            last_name=? AND school=?', name)
        row = c.fetchone()
        self.attrs['student_sql_id'] = row[0]
        self._sql_id = row[0]

        # write an event to New Students Events Table
        ns = New_Students_Event(self.attrs['student_sql_id'], self.attrs['oyd_id'],
            self.attrs['start_date'])
        ns.put(db)

        # look up the school name, region name, and nat_area name
        # for writing the Master Events Table which is de-normalized
        school = School()
        school.attrs['school_id'] = self.attrs['school']
        school.get(db)
        region = Region()
        region.attrs['region_id'] = school.attrs['school_region']
        region.get(db)
        nat_area = NatArea ()
        nat_area.attrs['nat_area_id'] = region.attrs['nat_area']
        nat_area.get(db)

        # write an event to the Master Events Tables
        me = Master_Event(event = 'newstudent',
            date = self.attrs['start_date'],
            student_sql_id = self.attrs['student_sql_id'],
            nat_area_name = nat_area.attrs['area_name'],
            region_name = region.attrs['region_name'],
            school_name = school.attrs['school_name'],
            age = self.attrs['age'],
            first_name = self.attrs['first_name'],
            last_name = self.attrs['last_name'],
            occupation = self.attrs['occupation'])
        me.put(db)

        return (0, "New Student Added to Database")

    def _sql_update_attr (self, db, conn, c, label):
        """Student Object: _sql_update_attr method (private)
        Updates a specific attribute in the instance of Student
        to the associated existing row in the database
        Parameters:
            conn = connection to database
            c = cursor to database
            label = name of attribute to be udpated to db
            attr = attribute to be updated"""

        if self._sql_id is not None:
            try:
                c.execute('UPDATE students SET ' + label + ' = "' + \
                    str(self.attrs[label]) + '" WHERE student_sql_id=' + str(self._sql_id))

                # Save (commit) the changes
                conn.commit()

                # check if this is a 'dropped' event
                now = datetime.now()
                txt_date = str(now.month) + '/' + str(now.day) + '/' + \
                    str(now.year)
                if label == 'status' and self.attrs['status'] == 'dropped':
                    # write an event to Drop Events Table
                    ns = Drop_Event(self.attrs['student_sql_id'], self.attrs['oyd_id'],
                        txt_date, self.attrs['drop_reason'])
                    ns.put(db)

                    # look up the school name, region name, and nat_area name
                    # for writing the Master Events Table which is de-normalized
                    school = School()
                    school.attrs['school_id'] = self.attrs['school']
                    school.get(db)
                    region = Region()
                    region.attrs['region_id'] = school.attrs['school_region']
                    region.get(db)
                    nat_area = NatArea ()
                    nat_area.attrs['nat_area_id'] = region.attrs['nat_area']
                    nat_area.get(db)

                    # write an event to the Master Events Tables
                    me = Master_Event(event = 'drop',
                        date = txt_date,
                        student_sql_id = self.attrs['student_sql_id'],
                        nat_area_name = nat_area.attrs['area_name'],
                        region_name = region.attrs['region_name'],
                        school_name = school.attrs['school_name'],
                        age = self.attrs['age'],
                        first_name = self.attrs['first_name'],
                        last_name = self.attrs['last_name'])
                    me.put(db)
                # check if this is a 'testing' event
                elif label == 'last_test_date':
                    # write an event to Testing Events Table
                    te = Testing_Event(self.attrs['student_sql_id'], self.attrs['oyd_id'],
                        self.attrs['last_test_date'], self.attrs['rank'], 'pass')
                    te.put(db)

                    # look up the school name, region name, and nat_area name
                    # for writing the Master Events Table which is de-normalized
                    school = School()
                    school.attrs['school_id'] = self.attrs['school']
                    school.get(db)
                    region = Region()
                    region.attrs['region_id'] = school.attrs['school_region']
                    region.get(db)
                    nat_area = NatArea ()
                    nat_area.attrs['nat_area_id'] = region.attrs['nat_area']
                    nat_area.get(db)

                    # write an event to the Master Events Tables
                    me = Master_Event(event = 'test',
                        date = self.attrs['last_test_date'],
                        student_sql_id = self.attrs['student_sql_id'],
                        nat_area_name = nat_area.attrs['area_name'],
                        region_name = region.attrs['region_name'],
                        school_name = school.attrs['school_name'],
                        age = self.attrs['age'],
                        first_name = self.attrs['first_name'],
                        last_name = self.attrs['last_name'])
                    me.put(db)
                return 0    # return Success
            except Exception as e:
                print (f"ERROR: _set_update_attr: {e}")
                return 1    # return Error
        else:
            print ("ERROR: _set_update_attr: _sql_id not yet set")
            return 1    # return Error

    def _sql_commit (self, conn, c):
        """Student Object: _sql_commit method (private)
        Commits all attribute in the instance of Student
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
                c.execute('UPDATE students SET ' + lvl + \
                    ' WHERE student_sql_id=' + str(self._sql_id))

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
        """ Student Object: get method
        Populates the instance of Student from the database as a new row
        Parameters:
            db = Database object from which to retrive the cursor"""

        return self._sql_populate (db.cursor)

    def put (self, db):
        """Student Object: put method
        Inserts the instance of Student into the database as a new row
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_insert(db, db.conn, db.cursor)

    def update_attr (self, db, label):
        """Student Object: update_attr method
        Updates a specific attribute in the instance of Student
        to the associated existing row in the database
        Parameters:
            db = Database object that contains the
                connection & cursor to database
            label = name of attribute to be udpated to db
            attr = attribute to be updated"""

        return self._sql_update_attr(db, db.conn, db.cursor, label)

    #    commit the data in Student to the DB
    def update (self, db):
        """Student Object: update method
        Commits all attributes in the instance of Student
        to the associated existing row in the database
        Parameters:
            db = Database object that contains the
                connection & cursor to database"""

        return self._sql_commit(db.conn, db.cursor)
