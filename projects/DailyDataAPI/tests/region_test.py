import pytest
from db import *
from region import *
from refreshdb import refresh_db

def test_get():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    assert db.open_db('test.db') == 0

    # Create a Region Object
    region = Region(region_name='Seattle', region_abbrev="SEA",
        main_reg_id = 15500, reg_team_ids = "15500, 15513, 15505",
        nat_area = 1, street="7858 Leary Way", city = "Redmond",
        state = "WA", postal_code = "98052", email="seattle@8taughtas1.com",
        phone = "(206) 555-1212", status = 0, standing = 0)
    assert region.put(db) == (0, 'Region Successfully Added!')

    # Check if the region was retrieved from DB
    assert region.get (db) == 0

    # Create an empty Region Object
    region1 = Region()

    # Attempt to populate an empty (unknow) region from the DB
    assert region1.get (db) == 1

    db.close_db()

def test_put():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    region1 = Region(region_name='Seattle', region_abbrev="SEA",
        main_reg_id = 15500, reg_team_ids = "15500, 15513, 15505",
        nat_area = 1, street="7858 Leary Way", city = "Redmond",
        state = "WA", postal_code = "98052", email="seattle@8taughtas1.com",
        phone = "(206) 555-1212", status = 0, standing = 0)
    assert region1.get (db) != 0
    assert region1.put (db) == (0, 'Region Successfully Added!')

    region2 = Region(region_name='Boston', region_abbrev="BOS",
        main_reg_id = 16600, reg_team_ids = "16600, 16613, 16605",
        nat_area = 2, street="123 Main St.", city = "Boston",
        state = "MA", postal_code = "02134", email="boston@8taughtas1.com",
        phone = "(555) 555-1212", status = 0, standing = 0)
    assert region2.get (db) != 0
    assert region2.put (db) == (0, 'Region Successfully Added!')

    db.close_db()

def test_update():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    # Create a Region Object
    region = Region(region_name='Seattle', region_abbrev="SEA",
        main_reg_id = 15500, reg_team_ids = "15500, 15513, 15505",
        nat_area = 1, street="7858 Leary Way", city = "Redmond",
        state = "WA", postal_code = "98052", email="seattle@8taughtas1.com",
        phone = "(206) 555-1212", status = 0, standing = 0)
    region.put(db)

    # Check if the Region was retrieved from DB
    assert region.get (db) == 0

    # Time Travel - Test setting multiple attrs and doing a commit
    region.attrs['region_name'] = "Boston"
    region.attrs['region_abbrev'] = 'BOS'
    assert region.update (db) == 0

    db.close_db()

def test_count():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    region1 = Region(region_name='Seattle', region_abbrev="SEA",
        main_reg_id = 15500, reg_team_ids = "15500, 15513, 15505",
        nat_area = 1, street="7858 Leary Way", city = "Redmond",
        state = "WA", postal_code = "98052", email="seattle@8taughtas1.com",
        phone = "(206) 555-1212", status = 0, standing = 0)
    assert region1.put (db) == (0, 'Region Successfully Added!')

    region2 = Region(region_name='Boston', region_abbrev="BOS",
        main_reg_id = 16600, reg_team_ids = "16600, 16613, 16605",
        nat_area = 2, street="123 Main St.", city = "Boston",
        state = "MA", postal_code = "02134", email="boston@8taughtas1.com",
        phone = "(555) 555-1212", status = 0, standing = 0)
    assert region2.put (db) == (0, 'Region Successfully Added!')

    rt = Regions_Table()
    assert rt.count (db) == 3

    db.close_db()

def test_query_range():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    region1 = Region(region_name='Seattle', region_abbrev="SEA",
        main_reg_id = 15500, reg_team_ids = "15500, 15513, 15505",
        nat_area = 1, street="7858 Leary Way", city = "Redmond",
        state = "WA", postal_code = "98052", email="seattle@8taughtas1.com",
        phone = "(206) 555-1212", status = 0, standing = 0)
    assert region1.put (db) == (0, 'Region Successfully Added!')

    region2 = Region(region_name='Boston', region_abbrev="BOS",
        main_reg_id = 16600, reg_team_ids = "16600, 16613, 16605",
        nat_area = 2, street="123 Main St.", city = "Boston",
        state = "MA", postal_code = "02134", email="boston@8taughtas1.com",
        phone = "(555) 555-1212", status = 0, standing = 0)
    assert region2.put (db) == (0, 'Region Successfully Added!')

    rt = Regions_Table()
    assert rt.query_range (db=db, limit=1, offset=0) == 0
    assert len(rt.regions) == 1

def test_query_all():
    # reset the DB to a known state
    refresh_db ('test.db')

    # open the DB
    db = Database()
    db.open_db('test.db')

    region1 = Region(region_name='Seattle', region_abbrev="SEA",
        main_reg_id = 15500, reg_team_ids = "15500, 15513, 15505",
        nat_area = 1, street="7858 Leary Way", city = "Redmond",
        state = "WA", postal_code = "98052", email="seattle@8taughtas1.com",
        phone = "(206) 555-1212", status = 0, standing = 0)
    assert region1.put (db) == (0, 'Region Successfully Added!')

    region2 = Region(region_name='Boston', region_abbrev="BOS",
        main_reg_id = 16600, reg_team_ids = "16600, 16613, 16605",
        nat_area = 2, street="123 Main St.", city = "Boston",
        state = "MA", postal_code = "02134", email="boston@8taughtas1.com",
        phone = "(555) 555-1212", status = 0, standing = 0)
    assert region2.put (db) == (0, 'Region Successfully Added!')

    rt = Regions_Table()
    assert rt.query_all (db=db) == 0
    assert len(rt.regions) == 3
