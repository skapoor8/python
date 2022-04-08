# attendance.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# for OYD Daily Program
from events import *
from student import *
from natarea import *
from region import *
from school import *
from course import *

class Attendance (object):
    def __init__(self, student_sql_id=None,
        attendance_date=None, class_group=None):
        """Attendance Object: __init__ Method
            Parameters: (all default to None)
                student_sql_id - Student's SQL ID
                attendance_date - date of attenance"""

        # Dictionary of School Attributes
        self.attrs = {'attd_id': None,   # internal use only, do not change
            'student_sql_id': student_sql_id,
            'attendance_date': attendance_date
            }

        # SQL Schema
        # Must match the attrs (attributes) above, line for line
        self.schema = ['attd_id',
            'student_sql_id',
            'attendance_date',
            ]

        # create the INSERT schema substituion string
        self.schema_insert = ", ".join(self.schema)

        # SQL Data Types for the SQL Schema
        # Must match the SQL Schema above, line for line
        self.types = ['integer primary key',
            'integer',
            'datetime',
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
        """ Attendance Object: _get method (private)
        Returns a tuple of the Attendance data"""

        # assuming that dictiionaries are unordered
        # retrive the data in oder as a tuple
        results = []
        for key in self.schema:
            results.append(self.attrs[key])

        return tuple(results)

class MLTAttendance (object):
    def __init__(self, student_sql_id=None,
        date=None, course=None, lesson=None):
        """MLTAttendance Object: __init__ Method
            Parameters: (all default to None)
                student_sql_id - Student's SQL ID
                date - date of attenance
                course - course attended (from course list)
                lesson - lesson number"""

        # Dictionary of School Attributes
        self.attrs = {'MLTattd_id': None,   # internal use only, do not change
            'student_sql_id': student_sql_id,
            'date': date,
            'course': course,
            'lesson': lesson
            }

        # SQL Schema
        # Must match the attrs (attributes) above, line for line
        self.schema = ['MLTattd_id',
            'student_sql_id',
            'date',
            'course',
            'lesson'
            ]

        # create the INSERT schema substituion string
        self.schema_insert = ", ".join(self.schema)

        # SQL Data Types for the SQL Schema
        # Must match the SQL Schema above, line for line
        self.types = ['integer primary key',
            'integer',
            'datetime',
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

    # Method to get a tuuple of all student data
    def _get (self):
        """ MLTAttendance Object: _get method (private)
        Returns a tuple of the MLTAttendance data"""

        # assuming that dictiionaries are unordered
        # retrive the data in oder as a tuple
        results = []
        for key in self.schema:
            results.append(self.attrs[key])

        return tuple(results)

# Daily Attendance Function
# Commits one line to the Attendance Event Table per student_sql_id provided
def attendanceDaily (db, student_sql_id_list, date):
    """ attendanceDaily function
        Makes an entry for each student_sql_id in the list, into the
        Attendance Table using database and data provided.
        Parameters:
        db - database object,
        student_sql_id_list - Python List of Student SQL IDs,
        date - date of attenance"""

    conn = db.conn
    c = db.cursor

    # process each student_sql_id
    for stud_sql_id in student_sql_id_list:
        attd = Attendance(student_sql_id = stud_sql_id, attendance_date=date)

        try:
            c.execute('INSERT INTO attendance (' + attd.schema_insert + \
                ') VALUES ' + attd.schema_insert_sub, attd._get())

            # get the Student record
            stud = Student()
            stud.attrs['student_sql_id'] = stud_sql_id
            stud.get(db)

            # look up the school name, region name, and nat_area name
            # for writing the Master Events Table which is de-normalized
            school = School()
            school.attrs['school_id'] = stud.attrs['school']
            school.get(db)

            region = Region()
            region.attrs['region_id'] = school.attrs['school_region']
            region.get(db)

            nat_area = NatArea()
            nat_area.attrs['nat_area_id'] = region.attrs['nat_area']
            nat_area.get(db)

            # write an event to the Master Events Tables
            mstrevent = Master_Event(event = 'attendance',
                date = date,
                student_sql_id = stud_sql_id,
                nat_area_name = nat_area.attrs['area_name'],
                region_name = region.attrs['region_name'],
                school_name = school.attrs['school_name'],
                age = stud.attrs['age'],
                first_name = stud.attrs['first_name'],
                last_name = stud.attrs['last_name'])
            mstrevent.put(db)

        except:
            return 1

        # commit the data to the database
        conn.commit()

    return 0

# MLT Attendance Function
# commits one line to the MLT Attendace Event Table per call to the fuction
def attendanceMLT (db, student_sql_id, date, course, lesson):
    """ attendanceDaily function
        Makes an entry for each student_sql_id in the list, into the
        Attendance Table using database and data provided.
        Parameters:
        db - database object,
        student_sql_id_list - Python List of Student SQL IDs,
        date - date of attenance,
        course - refernce number of course taken from Course Table
        lesson - lesson number witnin the course"""

    conn = db.conn
    c = db.cursor

    mlt_attd = MLTAttendance(student_sql_id = student_sql_id,
        date=date, course = course, lesson = lesson)

    try:
        c.execute('INSERT INTO mltattendance (' + mlt_attd.schema_insert + \
            ') VALUES ' + mlt_attd.schema_insert_sub, mlt_attd._get())

        # get the Student record
        stud = Student()
        stud.attrs['student_sql_id'] = student_sql_id
        stud.get(db)

        # look up the school name, region name, and nat_area name
        # for writing the Master Events Table which is de-normalized
        school = School()
        school.attrs['school_id'] = stud.attrs['school']
        school.get(db)
        region = Region()
        region.attrs['region_id'] = school.attrs['school_region']
        region.get(db)
        nat_area = NatArea ()
        nat_area.attrs['nat_area_id'] = region.attrs['nat_area']
        nat_area.get(db)

        # look up the course
        crs = Course()
        crs.attrs['course_id'] = course
        crs.get(db)

        # write an event to the Master Events Tables
        mstrevent = Master_Event(event = 'MLTattendance',
            date = date,
            student_sql_id = student_sql_id,
            nat_area_name = nat_area.attrs['area_name'],
            region_name = region.attrs['region_name'],
            school_name = school.attrs['school_name'],
            age = stud.attrs['age'],
            first_name = stud.attrs['first_name'],
            last_name = stud.attrs['last_name'],
            course_name = crs.attrs['course_name'])
        mstrevent.put(db)

    except:
        return 1

    # commit the data to the database
    conn.commit()

    return 0
