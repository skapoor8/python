import pytest
from db import *
from events import *
from refreshdb import refresh_db

def test_master_event_put():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    event1 = Master_Event (event='newstudent', date='9/1/2017',
        student_sql_id=333)
    assert event1.put (db) == 0

    event2 = Master_Event (event='test', date='9/2/2017',
        student_sql_id=4444)
    assert event2.put (db) == 0

    event3 = Master_Event (event='drop', date='9/3/2017',
        student_sql_id=55555)
    assert event3.put (db) == 0

    db.close_db()

def test_new_students_event_put():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    ns1 = New_Students_Event (student_sql_id=333, oyd_id=12333,
        signup_date='9/1/2017')
    assert ns1.put (db) == 0

    ns2 = New_Students_Event (student_sql_id=4444, oyd_id=12344,
        signup_date='9/1/2017')
    assert ns2.put (db) == 0

    ns3 = New_Students_Event (student_sql_id=55555, oyd_id=12355,
        signup_date='9/1/2017')
    assert ns3.put (db) == 0

    db.close_db()

def test_testing_event_put():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    te1 = Testing_Event (student_sql_id=333, oyd_id=12333,
        test_date='9/1/2017', rank_tested='1S', pass_fail='pass')
    assert te1.put (db) == 0

    te2 = Testing_Event (student_sql_id=4444, oyd_id=12344,
        test_date='9/1/2017', rank_tested='2S', pass_fail='fail')
    assert te2.put (db) == 0

    te3 = Testing_Event (student_sql_id=55555, oyd_id=12355,
        test_date='9/1/2017', rank_tested='1D', pass_fail='pass')
    assert te3.put (db) == 0

    db.close_db()

def test_drop_event_put():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    de1 = Drop_Event (student_sql_id=333, oyd_id=12333,
        drop_date='9/1/2017', reason='moved to Albequerque, NM')
    assert de1.put (db) == 0

    de2 = Drop_Event (student_sql_id=4444, oyd_id=12344,
        drop_date='9/1/2017', reason='no showers')
    assert de2.put (db) == 0

    de3 = Drop_Event (student_sql_id=55555, oyd_id=12355,
        drop_date='9/1/2017', reason='abducted by aliens')
    assert de3.put (db) == 0

    db.close_db()
