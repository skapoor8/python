import pytest
from db import *
from natarea import *
from refreshdb import refresh_db

def test_get():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    assert db.open_db('test.db') == 0

    # Create a NatArea Object
    natarea = NatArea(area_name='West', area_abbrev="WST")
    natarea.put(db)

    # Check if the natarea was retrieved from DB
    assert natarea.get (db) == 0

    # Create an empty NatArea Object
    natarea1 = NatArea()

    # Attempt to populate an empty (unknow) natarea from the DB
    assert natarea1.get (db) == 1

    db.close_db()

def test_put():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    natarea1 = NatArea(area_name='South', area_abbrev="STH")
    assert natarea1.get (db) != 0
    assert natarea1.put (db) == (0, 'Area Successfully Added!')

    natarea2 = NatArea(area_name='East', area_abbrev="EST")
    assert natarea2.get (db) != 0
    assert natarea2.put (db) == (0, 'Area Successfully Added!')

    db.close_db()

def test_update():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # Create a NatArea Object
    natarea = NatArea(area_name='West', area_abbrev="WST")
    natarea.put(db)

    # Check if the NatArea was retrieved from DB
    assert natarea.get (db) == 0

    print (f"DEBUG.natarea_test test_update natarea.attrs['nat_area_id'] = {natarea.attrs['nat_area_id']} ")

    # Time Travel
    natarea.attrs['area_name'] = "South"
    natarea.attrs['area_abbrev'] = 'STH'
    assert natarea.update (db) == 0

    db.close_db()

def test_count():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    natarea1 = NatArea(area_name='West', area_abbrev="WST")
    assert natarea1.put (db) == (0, 'Area Successfully Added!')

    natarea2 = NatArea(area_name='East', area_abbrev="EST")
    assert natarea2.put (db) == (0, 'Area Successfully Added!')

    na = NatAreas_Table()
    assert na.count (db) == 3

    db.close_db()

def test_query_range():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    natarea1 = NatArea(area_name='West', area_abbrev="WST")
    assert natarea1.put (db) == (0, 'Area Successfully Added!')

    natarea2 = NatArea(area_name='East', area_abbrev="EST")
    assert natarea2.put (db) == (0, 'Area Successfully Added!')

    na = NatAreas_Table()
    assert na.query_range (db=db, limit=1, offset=0) == 0
    assert len(na.areas) == 1

def test_query_all():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    natarea1 = NatArea(area_name='West', area_abbrev="WST")
    assert natarea1.put (db) == (0, 'Area Successfully Added!')

    natarea2 = NatArea(area_name='East', area_abbrev="EST")
    assert natarea2.put (db) == (0, 'Area Successfully Added!')

    na = NatAreas_Table()
    assert na.query_all (db=db) == 0
    assert len(na.areas) == 3
