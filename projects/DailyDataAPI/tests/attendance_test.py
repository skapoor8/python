import pytest
from db import *
from attendance import *
from refreshdb import refresh_db
from datetime import datetime

def test_attendanceDaily():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    sql_id_list = [1, 22, 333, 4444, 55555]
    now = datetime.now()
    txt_date = str(now.month) + '/' + str(now.day) + '/' + \
        str(now.year)

    assert attendanceDaily(db, sql_id_list, txt_date) == 0

    c = db.cursor
    c.execute('SELECT * FROM attendance')
    row = c.fetchone()

    assert row[1] == 1
    row = c.fetchone()
    assert row[1] == 22
    row = c.fetchone()
    assert row[1] == 333
    row = c.fetchone()
    assert row[1] == 4444
    row = c.fetchone()
    assert row[1] == 55555

    db.close_db()

def test_attendanceMLT():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    sql_id_list = [1, 22, 333, 4444, 55555]
    now = datetime.now()
    txt_date = str(now.month) + '/' + str(now.day) + '/' + \
        str(now.year)

    for stud_sql_id in sql_id_list:
        assert attendanceMLT(db, stud_sql_id, txt_date, 1, 1) == 0

    c = db.cursor
    c.execute('SELECT * FROM mltattendance')
    row = c.fetchone()

    assert row[1] == 1
    row = c.fetchone()
    assert row[1] == 22
    row = c.fetchone()
    assert row[1] == 333
    row = c.fetchone()
    assert row[1] == 4444
    row = c.fetchone()
    assert row[1] == 55555

    db.close_db()
