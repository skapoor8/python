import pytest
from db import *
from course import *
from refreshdb import refresh_db

def test_get():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    assert db.open_db('test.db') == 0

    # Create a Course Object
    course = Course(course_name='Bagua', course_abbrev="BGWA")
    course.put(db)

    # Check if the course was retrieved from DB
    assert course.get (db) == 0

    # Create an empty Course Object
    course1 = Course()

    # Attempt to populate an empty (unknow) course from the DB
    assert course1.get (db) == 1

    db.close_db()

def test_put():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    course1 = Course (course_name='Bagua', course_abbrev="BGWA")
    assert course1.get (db) != 0
    assert course1.put (db) == 0

    course2 = Course (course_name='Ship Pal Gae Dan Hyung', course_abbrev="SPGDH")
    assert course2.get (db) != 0
    assert course2.put (db) == 0

    db.close_db()

def test_update():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # Create a Course Object
    course = Course(course_name='Bagua', course_abbrev="BGWA")
    course.put(db)

    # Check if the Course was retrieved from DB
    assert course.get (db) == 0

    # Time Travel - Test setting multiple attrs and doing a commit
    course.attrs['course_name'] = "Dan Hyung - Ship Pal Gae"
    course.attrs['course_abbrev'] = 'DH-SPG'
    assert course.update (db) == 0

    db.close_db()

def test_count():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    course1 = Course (course_name='Bagua', course_abbrev="BGWA")
    assert course1.put (db) == 0

    course2 = Course (course_name='Ship Pal Gae Dan Hyung', course_abbrev="SPGDH")
    assert course2.put (db) == 0

    ct = Courses_Table()
    assert ct.count (db) == 3

    db.close_db()

def test_query_range():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    course1 = Course (course_name='Bagua', course_abbrev="BGWA")
    assert course1.put (db) == 0

    course2 = Course (course_name='Ship Pal Gae Dan Hyung', course_abbrev="SPGDH")
    assert course2.put (db) == 0

    ct = Courses_Table()
    assert ct.query_range (db=db, limit=1, offset=0) == 0
    assert len(ct.courses) == 1

def test_query_all():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    course1 = Course (course_name='Bagua', course_abbrev="BGWA")
    assert course1.put (db) == 0

    course2 = Course (course_name='Ship Pal Gae Dan Hyung', course_abbrev="SPGDH")
    assert course2.put (db) == 0

    ct = Courses_Table()
    assert ct.query_all (db=db) == 0
    assert len(ct.courses) == 3
