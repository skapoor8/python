import pytest
from db import *
from student import *
from refreshdb import refresh_db

def test_get():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    assert db.open_db('test.db') == 0

    # Create a Student Object
    student = Student(oyd_id=15505, first_name='Thomas', middle_name = 'Alan',
        last_name='Grate', school=1)

    # Check if the student was retrieved from DB
    assert student.get (db) == 0

    # Create an empty Student Object
    stud1 = Student()

    # Attempt to populate an empty (unknow) student from the DB
    assert stud1.get (db) == 1

    db.close_db()

def test_put():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    stud1 = Student (oyd_id=15506, first_name='Jon', last_name='Criddle',
        age=63, birth_date= '6/2/1954', school=2,
        start_date='5/30/2005', rank='3D', position='I')
    assert stud1.get (db) != 0
    assert stud1.put (db) == (0, 'New Student Added to Database')

    # try to re-insert the new student
    assert stud1.put (db) == (1, 'Failed to insert new Student into Database')

    stud2 = Student (oyd_id=15523, first_name='Michelle', last_name='Judy',
        age=36, birth_date='7/4/1981', school=2,
        start_date='1/1/2010', rank='2D', position='I')
    assert stud2.get (db) != 0
    assert stud2.put (db) == (0, 'New Student Added to Database')

    # try to re-insert the new student
    assert stud2.put (db) == (1, 'Failed to insert new Student into Database')

    stud3 = Student (oyd_id=15507, first_name='Justin', last_name='Martin',
        age=41, birth_date='7/5/1976', school=1,
        start_date='1/1/1997', rank='3D', position='AHI')
    assert stud3.get (db) != 0
    assert stud3.put (db) == (0, 'New Student Added to Database')

    # try to re-insert the new student
    assert stud3.put (db) == (1, 'Failed to insert new Student into Database')

    db.close_db()

def test_update_attr():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # Create a Student Object
    student = Student(oyd_id=15505, first_name='Thomas', middle_name = 'Alan',
        last_name='Grate', school=1)

    # Check if the student was retrieved from DB
    assert student.get (db) == 0

    # Lets Go back in Time - Test a single attr set and update
    student.attrs['age'] = 43
    assert student.update_attr (db, 'age') == 0
    student.attrs['rank'] = '4S'
    assert student.update_attr (db, 'rank') == 0
    student.attrs['next_rank'] = '4S'
    assert student.update_attr (db, 'next_rank') == 0

    db.close_db()

def test_update():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # Create a Student Object
    student = Student(oyd_id=15505, first_name='Thomas', middle_name = 'Alan',
        last_name='Grate', school=1)

    # Check if the student was retrieved from DB
    assert student.get (db) == 0

    # Time Travel - Test setting multiple attrs and doing a commit
    student.attrs['age'] = 54
    student.attrs['rank'] = '4D'
    student.attrs['next_rank'] = '5D'
    student.attrs['title'] = 'ARHI'
    assert student.update (db) == 0

    db.close_db()

def test_count():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # One student exists in DB after refresh, add more
    stud1 = Student (oyd_id=15506, first_name='Jon', last_name='Criddle',
        age=63, birth_date= '6/2/1954', school=2,
        start_date='5/30/2005', rank='3D', position='I')
    stud1.put (db) == (0, 'New Student Added to Database')

    stud2 = Student (oyd_id=15523, first_name='Jane', last_name='Judy',
        age=36, birth_date='7/4/1981', school=2,
        start_date='1/1/2010', rank='2D', status='dropped')
    stud2.put (db) == (0, 'New Student Added to Database')

    stud3 = Student (oyd_id=15507, first_name='Mark', last_name='Martin',
        age=41, birth_date='7/5/1976', school=1,
        start_date='1/1/1997', rank='3D', position='AHI')
    stud3.put (db) == (0, 'New Student Added to Database')

    st = Students_Table()
    assert st.count (db) == 4
    assert st.count (db, status='active') == 3
    assert st.count (db, status='dropped') == 1

    db.close_db()

def test_count_rank():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # One student exists in DB after refresh, add more
    stud1 = Student (oyd_id=15506, first_name='Jon', last_name='Criddle',
        age=63, birth_date= '6/2/1954', school=1,
        start_date='5/30/2005', rank='3D', position='I',
        class_group='Instructor')
    assert stud1.put (db) == (0, 'New Student Added to Database')

    stud2 = Student (oyd_id=15523, first_name='Jane', last_name='Judy',
        age=36, birth_date='7/4/1981', school=1,
        start_date='1/1/2010', rank='2D', status='dropped',
        class_group='Adult')
    assert stud2.put (db) == (0, 'New Student Added to Database')

    stud3 = Student (oyd_id=15507, first_name='Mark', last_name='Martin',
        age=41, birth_date='7/5/1976', school=1,
        start_date='1/1/1997', rank='3D', position='AHI',
        class_group='Instructor')
    assert stud3.put (db) == (0, 'New Student Added to Database')

    st = Students_Table()
    st.school = 1
    st.count_rank (db, status='active', class_group='Instructor')
    assert st.count_active_instr['3D'] == 3

    st.count_rank (db, status='dropped', class_group='Adult')
    assert st.count_dropped_adult['total'] == 1
    db.close_db()

def test_query_range():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # One student exists in DB after refresh, add more
    stud1 = Student (oyd_id=15506, first_name='Jon', last_name='Criddle',
        age=63, birth_date= '6/2/1954', school=1,
        start_date='5/30/2005', rank='3D', position='I',
        class_group='Instructor')
    assert stud1.put (db) == (0, 'New Student Added to Database')

    stud2 = Student (oyd_id=15523, first_name='Jane', last_name='Judy',
        age=36, birth_date='7/4/1981', school=1,
        start_date='1/1/2010', rank='2D', status='dropped',
        class_group='Adult')
    assert stud2.put (db) == (0, 'New Student Added to Database')

    stud3 = Student (oyd_id=15507, first_name='Mark', last_name='Martin',
        age=41, birth_date='7/5/1976', school=1,
        start_date='1/1/1997', rank='3D', position='AHI',
        class_group='Instructor')
    assert stud3.put (db) == (0, 'New Student Added to Database')

    st = Students_Table()
    st.school = 1
    assert st.query_range (db=db, limit=2, offset=0, status='active') == 0
    assert len(st.students_active) == 2

def test_query():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # One student exists in DB after refresh, add more
    stud1 = Student (oyd_id=15506, first_name='Jon', last_name='Criddle',
        age=63, birth_date= '6/2/1954', school=1,
        start_date='5/30/2005', rank='3D', position='I',
        class_group='Instructor')
    assert stud1.put (db) == (0, 'New Student Added to Database')

    stud2 = Student (oyd_id=15523, first_name='Jane', last_name='Judy',
        age=36, birth_date='7/4/1981', school=1,
        start_date='1/1/2010', rank='2D', status='dropped',
        class_group='Adult')
    assert stud2.put (db) == (0, 'New Student Added to Database')

    stud3 = Student (oyd_id=15507, first_name='Mark', last_name='Martin',
        age=41, birth_date='7/5/1976', school=1,
        start_date='1/1/1997', rank='3D', position='AHI',
        class_group='Instructor')
    assert stud3.put (db) == (0, 'New Student Added to Database')

    st = Students_Table()
    st.school = 1
    assert st.query (db=db, status='active') == 0
    assert len(st.students_active) == 3

def test_query_all():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # One student exists in DB after refresh, add more
    stud1 = Student (oyd_id=15506, first_name='Jon', last_name='Criddle',
        age=63, birth_date= '6/2/1954', school=1,
        start_date='5/30/2005', rank='3D', position='I',
        class_group='Instructor')
    assert stud1.put (db) == (0, 'New Student Added to Database')

    stud2 = Student (oyd_id=15523, first_name='Jane', last_name='Judy',
        age=36, birth_date='7/4/1981', school=1,
        start_date='1/1/2010', rank='2D', status='dropped',
        class_group='Adult')
    assert stud2.put (db) == (0, 'New Student Added to Database')

    stud3 = Student (oyd_id=15507, first_name='Mark', last_name='Martin',
        age=41, birth_date='7/5/1976', school=1,
        start_date='1/1/1997', rank='3D', position='AHI',
        class_group='Instructor')
    assert stud3.put (db) == (0, 'New Student Added to Database')

    st = Students_Table()
    st.school = 1
    assert st.query_all (db=db) == 0
    assert len(st.students) == 4

def test_query_active():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # One student exists in DB after refresh, add more
    stud1 = Student (oyd_id=15506, first_name='Jon', last_name='Criddle',
        age=63, birth_date= '6/2/1954', school=1,
        start_date='5/30/2005', rank='3D', position='I',
        class_group='Instructor')
    assert stud1.put (db) == (0, 'New Student Added to Database')

    stud2 = Student (oyd_id=15523, first_name='Jane', last_name='Judy',
        age=36, birth_date='7/4/1981', school=1,
        start_date='1/1/2010', rank='2D', status='dropped',
        class_group='Adult')
    assert stud2.put (db) == (0, 'New Student Added to Database')

    stud3 = Student (oyd_id=15507, first_name='Mark', last_name='Martin',
        age=41, birth_date='7/5/1976', school=1,
        start_date='1/1/1997', rank='3D', position='AHI',
        class_group='Instructor')
    assert stud3.put (db) == (0, 'New Student Added to Database')

    st = Students_Table()
    st.school = 1
    assert st.query_active (db=db) == 0
    assert len(st.students_active) == 3

def test_query_dropped():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # One student exists in DB after refresh, add more
    stud1 = Student (oyd_id=15506, first_name='Jon', last_name='Criddle',
        age=63, birth_date= '6/2/1954', school=1,
        start_date='5/30/2005', rank='3D', position='I',
        class_group='Instructor')
    assert stud1.put (db) == (0, 'New Student Added to Database')

    stud2 = Student (oyd_id=15523, first_name='Jane', last_name='Judy',
        age=36, birth_date='7/4/1981', school=1,
        start_date='1/1/2010', rank='2D', status='dropped',
        class_group='Adult')
    assert stud2.put (db) == (0, 'New Student Added to Database')

    stud3 = Student (oyd_id=15507, first_name='Mark', last_name='Martin',
        age=41, birth_date='7/5/1976', school=1,
        start_date='1/1/1997', rank='3D', position='AHI',
        class_group='Instructor')
    assert stud3.put (db) == (0, 'New Student Added to Database')

    st = Students_Table()
    st.school = 1
    assert st.query_dropped (db=db) == 0
    assert len(st.students_dropped) == 1
