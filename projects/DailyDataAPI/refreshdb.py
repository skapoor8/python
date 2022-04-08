# refreshdb.py
# written by: Thomas A. Grate
# copyright (c) 2017 by Thomas A. Grate, all rights reserved.
#
# Refreshes Selected Tables in the OYD Daily Program Database for Testing

import sqlite3
from db import *
from natarea import *
from region import *
from school import *
from student import *
from information import *
from events import *
from course import *
from attendance import *
from print_table import *

class Students_Table_Management (object):
    """ Students_Table_Managment object
        Management functions for 'students' Table """

    def __init__(self):
        self.student = Student()

    def drop(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS students;')

    def create(self, db):
        db.cursor.execute('CREATE TABLE students (' + self.student.schema_create + ')')

class New_Students_Events_Table_Management (object):
    """ New_Students_Events_Table_Managment object
        Management functions for 'newstudents' Table """

    def __init__(self):
        self.nse = New_Students_Event()

    def drop(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS newstudents;')

    def create(self, db):
        db.cursor.execute('CREATE TABLE newstudents (' + self.nse.schema_create + ')')

class Testing_Events_Table_Management (object):
    """ Testing_Events_Table_Managment object
        Management functions for 'testingevents' Table """

    def __init__(self):
        self.te = Testing_Event()

    def drop(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS testingevents;')

    def create(self, db):
        db.cursor.execute('CREATE TABLE testingevents (' + self.te.schema_create + ')')

class Drop_Events_Table_Management (object):
    """ Drop_Events_Table_Managment object
        Management functions for 'dropevents' Table """

    def __init__(self):
        self.de = Drop_Event()

    def drop(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS dropevents;')

    def create(self, db):
        db.cursor.execute('CREATE TABLE dropevents (' + self.de.schema_create + ')')

class Master_Events_Table_Management (object):
    """ Master_Events_Table_Managment object
        Management functions for 'masterevents' Table """

    def __init__(self):
        self.me = Master_Event()

    def drop(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS masterevents;')

    def create(self, db):
        db.cursor.execute('CREATE TABLE masterevents (' + self.me.schema_create + ')')

class Informations_Table_Management (object):
    """ Informations_Table_Managment object
        Management functions for 'informations' Table """

    def __init__(self):
        self.information = Information()

    def drop(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS informations;')

    def create(self, db):
        db.cursor.execute('CREATE TABLE informations (' + self.information.schema_create + ')')

class NatAreas_Table_Management (object):
    """ NatAreas_Table_Managment object
        Management functions for 'areas' Table """

    def __init__(self):
        self.area = NatArea()

    def drop(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS areas;')

    def create(self, db):
        db.cursor.execute('CREATE TABLE areas (' + self.area.schema_create + ')')


class Regions_Table_Management (object):
    """ Regions_Table_Managment object
        Management functions for 'regions' Table """

    def __init__(self):
        self.region = Region()

    def drop(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS regions;')

    def create(self, db):
        db.cursor.execute('CREATE TABLE regions (' + self.region.schema_create + ')')

class Schools_Table_Management (object):
    """ Schools_Table_Managment object
        Management functions for 'schools' Table """

    def __init__(self):
        self.school = School()

    def drop(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS schools;')

    def create(self, db):
        db.cursor.execute('CREATE TABLE schools (' + self.school.schema_create + ')')

class Courses_Table_Management (object):
    """ Courses_Table_Managment object
        Management functions for 'courses' Table """

    def __init__(self):
        self.course = Course()

    def drop(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS courses;')

    def create(self, db):
        db.cursor.execute('CREATE TABLE courses (' + self.course.schema_create + ')')

class Attendance_Table_Management (object):
    """ Attendance_Table_Managment object
        Management functions for 'attendance' Table """

    def __init__(self):
        self.attendance = Attendance()

    def drop(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS attendance;')

    def create(self, db):
        db.cursor.execute('CREATE TABLE attendance (' + self.attendance.schema_create + ')')

class MLTAttendance_Table_Management (object):
    """ MLTAttendance_Table_Managment object
        Management functions for 'mltattendance' Table """

    def __init__(self):
        self.mltattendance = MLTAttendance()

    def drop(self, db):
        db.cursor.execute('DROP TABLE IF EXISTS mltattendance;')

    def create(self, db):
        db.cursor.execute('CREATE TABLE mltattendance (' + self.mltattendance.schema_create + ')')

def refresh_students (filename, silent_mode):
    # Open the database designated by filename
    database = Database()
    database.open_db(filename)

    # Instantiate a Table object
    stm = Students_Table_Management()

    # Delete the table if it already exists
    stm.drop (database)

    # Create students table
    stm.create (database)

    # Create a Student Object
    student = Student(oyd_id=15505, first_name='Thomas', middle_name = 'Alan',
        last_name='Grate', age= 53, birth_date = '5/10/1964', school=1,
        start_date = '5/31/2006', position = 'HI', rank = '3D', next_rank = '4D',
        class_group = 'Instructor')
    result = student.put (database)

    if not silent_mode:
        # Print the updated students table
        title = f"Refresh {filename} Students Table: Added Students to Database"
        print_table (database, 'students', title)

    database.close_db()

def refresh_newstudents (filename, silent_mode):
    # Open the database designated by filename
    database = Database()
    database.open_db(filename)

    # Instantiate a Table object
    stm = New_Students_Events_Table_Management()

    # Delete the table if it already exists
    stm.drop (database)

    # Create students table
    stm.create (database)

    if not silent_mode:
        # Print the updated students table
        title = f"Refresh {filename} NewStudents Table: Added NewStudents to Database"
        print_table (database, 'newstudents', title)

    database.close_db()

def refresh_testingevents (filename, silent_mode):
    # Open the database designated by filename
    database = Database()
    database.open_db(filename)

    # Instantiate a Table object
    stm = Testing_Events_Table_Management()

    # Delete the table if it already exists
    stm.drop (database)

    # Create students table
    stm.create (database)

    if not silent_mode:
        # Print the updated students table
        title = f"Refresh {filename} Testing Events Table: Added TestingEvents to Database"
        print_table (database, 'testingevents', title)

    database.close_db()

def refresh_dropevents (filename, silent_mode):
    # Open the database designated by filename
    database = Database()
    database.open_db(filename)

    # Instantiate a Table object
    stm = Drop_Events_Table_Management()

    # Delete the table if it already exists
    stm.drop (database)

    # Create students table
    stm.create (database)

    if not silent_mode:
        # Print the updated students table
        title = f"Refresh {filename} Drop Events Table: Added DropEvents to Database"
        print_table (database, 'dropevents', title)

    database.close_db()

def refresh_masterevents (filename, silent_mode):
    # Open the database designated by filename
    database = Database()
    database.open_db(filename)

    # Instantiate a Table object
    stm = Master_Events_Table_Management()

    # Delete the table if it already exists
    stm.drop (database)

    # Create students table
    stm.create (database)

    if not silent_mode:
        # Print the updated students table
        title = f"Refresh {filename} Master Events Table: Added MasterEvents to Database"
        print_table (database, 'masterevents', title)

    database.close_db()

def refresh_informations (filename, silent_mode):
    # Open the database designated by filename
    database = Database()
    database.open_db(filename)

    # Instantiate a Table object
    stm = Informations_Table_Management()

    # Delete the table if it already exists
    stm.drop (database)

    # Create students table
    stm.create (database)

    information = Information(school=1, date='9/1/2017',
        first_name='John', last_name='Doe', age=37)
    result = information.put (database)

    if not silent_mode:
        # Print the updated students table
        title = f"Refresh {filename} Informations Table: Added Informations to Database"
        print_table (database, 'informations', title)

    database.close_db()

def refresh_areas (filename, silent_mode):
    # Open the database designated by filename
    database = Database()
    database.open_db(filename)

    # Instantiate a Table object
    stm = NatAreas_Table_Management()

    # Delete the table if it already exists
    stm.drop (database)

    # Create students table
    stm.create (database)

    natarea = NatArea (area_name='West', area_abbrev="WST")
    natarea.put(database)

    if not silent_mode:
        # Print the updated students table
        title = f"Refresh {filename} National Areas Table: Added Areas to Database"
        print_table (database, 'areas', title)

    database.close_db()

def refresh_regions (filename, silent_mode):
    # Open the database designated by filename
    database = Database()
    database.open_db(filename)

    # Instantiate a Table object
    stm = Regions_Table_Management()

    # Delete the table if it already exists
    stm.drop (database)

    # Create students table
    stm.create (database)

    region = Region (region_name='Pacific NW', region_abbrev="PNW",
        nat_area=1, main_reg_id='15500', email='david@seattleoyd.com',
        street='7858 Leary Way', city='Redmond', state='WA', postal_code='98052',
        phone='(425) 202-4898', status='0', standing='0')
    region.put(database)

    if not silent_mode:
        # Print the updated students table
        title = f"Refresh {filename} Regions Table: Added Regions to Database"
        print_table (database, 'regions', title)

    database.close_db()

def refresh_schools (filename, silent_mode):
    # Open the database designated by filename
    database = Database()
    database.open_db(filename)

    # Instantiate a Table object
    schtm = Schools_Table_Management()

    # Delete the table if it already exists
    schtm.drop (database)

    # Create students table
    schtm.create (database)

    # Create and Insert a New Student
    if not silent_mode:
        print(f"Refresh {filename} Schools Table: Adding first school")
        print("--------------------------")

    school = School(school_name='Redmond', school_region=1,
        main_ins_id='15507', email='redmond@8taughtas1.com',
        street='7858 Leary Way', city='Redmond', state='WA', postal_code='98052',
        school_phone='(425) 202-4898', status='0', standing='0')
    school.put(database)

    school = School(school_name='Kirkland', school_region=1,
        main_ins_id='15519', email='kirkland@8taughtas1.com',
        street='11506 124th Ave NE', city='Kirkland', state='WA', postal_code='98033',
        school_phone='(425) 803-6800', status='0', standing='0')
    school.put(database)

    school = School(school_name='Seattle', school_region=1,
        main_ins_id='15500', email='seattle@8taughtas1.com',
        street='12354', city='Seatle', state='WA', postal_code='98125',
        school_phone='(206) 817-2600', status='0', standing='0')
    school.put(database)

    school = School(school_name='Root Academy', school_region=1,
        main_ins_id='99999', email='rootacademy@8taughtas1.com',
        street='2332 N 116th St', city='Seattle', state='WA', postal_code='98133',
        school_phone='(206) 817-2600', status='0', standing='0')
    school.put(database)

    if not silent_mode:
        # Print the updated students table
        title = f"Refresh {filename} Schools Table: Added Schools to Database"
        print_table (database, 'schools', title)

    database.close_db()

def refresh_courses (filename, silent_mode):
    # Open the database designated by filename
    database = Database()
    database.open_db(filename)

    # Instantiate a Table object
    schtm = Courses_Table_Management()

    # Delete the table if it already exists
    schtm.drop (database)

    # Create students table
    schtm.create (database)

    course = Course (course_name='Bagua Program Year 1', course_abbrev="Bagua1")
    course.put(database)

    if not silent_mode:
        # Print the updated students table
        title = f"Refresh {filename} Courses Table: Added Courses to Database"
        print_table (database, 'courses', title)

    database.close_db()

def refresh_attendance (filename, silent_mode):
    # Open the database designated by filename
    database = Database()
    database.open_db(filename)

    # Instantiate a Table object
    atm = Attendance_Table_Management()

    # Delete the table if it already exists
    atm.drop (database)

    # Create students table
    atm.create (database)

    if not silent_mode:
        # Print the updated students table
        title = f"Refresh {filename} Attendance Table: Added Attendance to Database"
        print_table (database, 'attendance', title)

    database.close_db()

def refresh_MLTattendance (filename, silent_mode):
    # Open the database designated by filename
    database = Database()
    database.open_db(filename)

    # Instantiate a Table object
    atm = MLTAttendance_Table_Management()

    # Delete the table if it already exists
    atm.drop (database)

    # Create students table
    atm.create (database)

    if not silent_mode:
        # Print the updated students table
        title = f"Refresh {filename} MLT Attendance Table: Added mltattendance to Database"
        print_table (database, 'mltattendance', title)

    database.close_db()

# Refresh the Whole Database - used by Tests
def refresh_db (filename):
    refresh_areas (filename, True)
    refresh_regions (filename, True)
    refresh_schools (filename, True)
    refresh_newstudents (filename, True)
    refresh_testingevents (filename, True)
    refresh_dropevents (filename, True)
    refresh_masterevents (filename, True)
    refresh_courses (filename, True)
    refresh_attendance (filename, True)
    refresh_MLTattendance (filename, True)
    refresh_informations (filename, True)
    refresh_students (filename, True)

if __name__ == "__main__":
    # if run as the main program - refresh the oyd_daily.db
    # filename = 'oyd_daily.db'
    filename = 'test.db'

    print (f"Refreshing {filename} database file!")
    print ("WARNING: BE VERY CAREFUL IN THE USE OF THIS APP")
    print (f"It can delete all data in the {filename} database")
    print ("-------------------------------------------------")
    print ('')

    # National Areas Table
    if  input("Refresh National Areas Table: Y or n > ") == 'Y':
        print(f"Refreshing {filename} National Areas Table")
        # refresh the roster.db
        refresh_areas (filename, False)
    else:
        print (f"OK, leaving the {filename} - National Areas Table untouched!")
        print('')

    # Regions Table
    if  input("Refresh Regions Table: Y or n > ") == 'Y':
        print(f"Refreshing {filename} Regions Table")
        # refresh the roster.db
        refresh_regions (filename, False)
    else:
        print (f"OK, leaving the {filename} - Regions Table untouched!")
        print('')

    # Schools Table
    if  input("Refresh Schools Table: Y or n > ") == 'Y':
        print(f"Refreshing {filename} Schools Table")
        # refresh the roster.db
        refresh_schools (filename, False)
    else:
        print (f"OK, leaving the {filename} - Schools Table untouched!")
        print('')

    # Students Table
    if  input("Refresh Students Table: Y or n > ") == 'Y':
        print(f"Refreshing {filename} Students Table")
        # refresh the roster.db
        refresh_students (filename, False)
    else:
        print (f"OK, leaving the {filename} - Students Table untouched!")
        print('')

    # Informations Table
    if  input("Refresh Informations Table: Y or n > ") == 'Y':
        print(f"Refreshing {filename} Informations Table")
        # refresh the roster.db
        refresh_informations (filename, False)
    else:
        print (f"OK, leaving the {filename} - Informations Table untouched!")
        print('')

    # MasterEvents Table
    if  input("Refresh MasterEvents Table: Y or n > ") == 'Y':
        print(f"Refreshing {filename} MasterEvents Table")
        # refresh the roster.db
        refresh_masterevents (filename, False)
    else:
        print (f"OK, leaving the {filename} - MasterEvents Table untouched!")
        print('')

    # NewStudents Table
    if  input("Refresh NewStudents(Events) Table: Y or n > ") == 'Y':
        print(f"Refreshing {filename} NewStudents Table")
        # refresh the roster.db
        refresh_newstudents (filename, False)
    else:
        print (f"OK, leaving the {filename} - NewStudents(Events) Table untouched!")
        print('')

    # TestingEvents Table
    if  input("Refresh TestingEvents Table: Y or n > ") == 'Y':
        print(f"Refreshing {filename} TestingEvents Table")
        # refresh the roster.db
        refresh_testingevents (filename, False)
    else:
        print (f"OK, leaving the {filename} - TestingEvents Table untouched!")
        print('')

    # DropEvents Table
    if  input("Refresh DropEvents Table: Y or n > ") == 'Y':
        print(f"Refreshing {filename} DropEvents Table")
        # refresh the roster.db
        refresh_dropevents (filename, False)
    else:
        print (f"OK, leaving the {filename} - DropEvents Table untouched!")
        print('')

    # Courses Table
    if  input("Refresh Courses Table: Y or n > ") == 'Y':
        print(f"Refreshing {filename} Courses Table")
        # refresh the roster.db
        refresh_courses (filename, False)
    else:
        print (f"OK, leaving the {filename} - Courses Table untouched!")
        print('')

    # Attendance Table
    if  input("Refresh Attendance Table: Y or n > ") == 'Y':
        print(f"Refreshing {filename} Attendance Table")
        # refresh the roster.db
        refresh_attendance (filename, False)
    else:
        print (f"OK, leaving the {filename} - Attendance Table untouched!")
        print('')

    # MLTAttendance Table
    if  input("Refresh MLTAttendance Table: Y or n > ") == 'Y':
        print(f"Refreshing {filename} MLTAttendance Table")
        # refresh the roster.db
        refresh_MLTattendance (filename, False)
    else:
        print (f"OK, leaving the {filename} - MLT Attendance Table untouched!")
        print('')
