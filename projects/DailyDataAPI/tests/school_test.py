import pytest
from db import *
from school import *
from refreshdb import refresh_db

def test_get():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    assert db.open_db('test.db') == 0

    # Create a School Object
    school = School(school_name='Seattle')

    # Check if the school was retrieved from DB
    assert school.get (db) == 0

    # Create an empty School Object
    school1 = School()

    # Attempt to populate an empty (unknow) school from the DB
    assert school1.get (db) == 1

    db.close_db()

def test_put():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    school1 = School(school_name='Medford', main_ins_id = 16601,
        school_region = 2,
        street="7858 Leary Way", city = "Medford",
        state = "MA", postal_code = "02145", email="medford@8taughtas1.com",
        school_phone = "(206) 555-1212", status = 0, standing = 0)
    assert school1.get (db) != 0
    assert school1.put (db) == (0, 'School Successfully Added!')

    school2 = School(school_name='West Cambridge', main_ins_id = 16600,
        school_region = 2, street="123 Main St.", city = "Boston",
        state = "MA", postal_code = "02134", email="wcambridge@8taughtas1.com",
        school_phone = "(555) 555-1212", status = 0, standing = 0)
    assert school2.get (db) != 0
    assert school2.put (db) == (0, 'School Successfully Added!')

    db.close_db()

def test_update():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # Create a School Object
    school = School(school_name='South Bellevue', main_ins_id = 15500,
        school_region = 1,
        street="12345 156th Ave SE", city = "Bellevue",
        state = "WA", postal_code = "98009", email="sbellevue@8taughtas1.com",
        school_phone = "(425) 555-1212", status = 0, standing = 0)
    school.put(db)

    # Check if the School was retrieved from DB
    assert school.get (db) == 0

    # Time Travel - Test setting multiple attrs and doing a commit
    school.attrs['school_name'] = "East Cambridge"
    school.attrs['main_ins_id'] = '16699'
    assert school.update (db) == 0

    db.close_db()

def test_count():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    st = Schools_Table()
    st.region = 1
    assert st.count (db) == 4

    db.close_db()

def test_query_range():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    st = Schools_Table()
    st.region = 1
    assert st.query_range (db=db, limit=2, offset=0, region=1) == 0
    assert len(st.schools) == 2

def test_query():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    st = Schools_Table()
    st.region = 1
    assert st.query (db=db, region=1) == 0
    assert len(st.schools) == 4

def test_query_all():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    st = Schools_Table()
    st.region = 1
    assert st.query_all (db=db) == 0
    assert len(st.schools) == 4
