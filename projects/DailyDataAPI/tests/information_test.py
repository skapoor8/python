import pytest
from db import *
from information import *
from refreshdb import refresh_db

def test_get():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    assert db.open_db('test.db') == 0

    # Create a Information Object
    information = Information(school=1, first_name='John', last_name='Doe')

    # Check if the information was retrieved from DB
    assert information.get (db) == 0

    # Create an empty Information Object
    stud1 = Information()

    # Attempt to populate an empty (unknow) information from the DB
    assert stud1.get (db) == 1

    db.close_db()

def test_put():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    info1 = Information (school=2, date='9/1/2018',
        first_name='Jon', last_name='Criddle',
        age=63, birth_date= '6/2/1954',
        class_group='adult')
    assert info1.get (db) != 0
    assert info1.put (db) == (0, 'New Information Added to Database')

    info2 = Information (school=2, date='9/1/2018',
        first_name='Michelle', last_name='Judy',
        age=36, birth_date='7/4/1981',
        class_group='adult')
    assert info2.get (db) != 0
    assert info2.put (db) == (0, 'New Information Added to Database')

    info3 = Information (school=3, date='9/1/2018',
        first_name='Justin', last_name='Martin',
        age=41, birth_date='7/5/1976',
        class_group='adult')
    assert info3.get (db) != 0
    assert info3.put (db) == (0, 'New Information Added to Database')

    db.close_db()

def test_update_attr():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # Create a Information Object
    information = Information(school=1, first_name='John', last_name='Doe')

    # Check if the information was retrieved from DB
    assert information.get (db) == 0

    # Lets Go back in Time - Test a single attr set and update
    information.attrs['age'] = 27
    assert information.update_attr (db, 'age') == 0
    information.attrs['birth_date'] = '9/1/1990'
    assert information.update_attr (db, 'birth_date') == 0
    information.attrs['class_group'] = 'adult'
    assert information.update_attr (db, 'class_group') == 0

    db.close_db()

def test_update():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # Create a Information Object
    information = Information(school=1, first_name='John', last_name='Doe')

    # Check if the information was retrieved from DB
    assert information.get (db) == 0

    # Time Travel - Test setting multiple attrs and doing a commit
    information.attrs['age'] = 37
    information.attrs['birth_date'] = '9/1/1980'
    information.attrs['class_group'] = 'adult'
    information.attrs['street'] = '123 Main St'
    information.attrs['city'] = 'Redmond'
    information.attrs['state'] = 'WA'
    information.attrs['postal_code'] = '98052'
    assert information.update (db) == 0

    db.close_db()
