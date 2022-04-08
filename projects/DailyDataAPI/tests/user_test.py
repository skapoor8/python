import pytest
from db import *
from user import *
from refreshuserdb import refresh_users

def test_get():
    # reset the DB to a known state
    refresh_users ('test.db', True)

    # open the DB
    db = Database()
    assert db.open_db('test.db') == 0

    # Create a User Object
    user = User()
    user.attrs['user_id'] = 1

    # Check if the student was retrieved from DB
    assert user.get (db) == 0

    # Create an empty Student Object
    user1 = User()

    # Attempt to populate an empty (unknow) student from the DB
    assert user1.get (db) == 1

    db.close_db()

def test_put():
    # reset the DB to a known state
    refresh_users ('test.db', True)

    # open the DB
    db = Database()
    db.open_db('test.db')

    user1 = User ()
    user1.attrs['username'] = 'jonc'
    user1.attrs['oyd_id'] = 15506
    user1.attrs['access_level'] =0
    user1.attrs['first_name'] ='Jon'
    user1.attrs['last_name'] = 'Criddle'
    user1.attrs['def_school'] = 2
    user1.attrs['def_region'] = 1
    user1.attrs['def_nat_area'] = 1
    assert user1.put (db, 'ironhand') == (0, 'User Successfully Added!')

    db.close_db()

def test_update():
    # reset the DB to a known state
    refresh_users ('test.db', True)

    # open the DB
    db = Database()
    db.open_db('test.db')

    # Create a User Object
    user = User()
    user.attrs['user_id'] = 1

    # Check if the student was retrieved from DB
    assert user.get (db) == 0

    # Time Travel - Test setting multiple attrs and doing a commit
    user.attrs['def_school'] = 2
    user.attrs['def_region'] = 2
    assert user.update (db) == 0

    db.close_db()

def test_delete():
    # reset the DB to a known state
    refresh_users ('test.db', True)

    # open the DB
    db = Database()
    db.open_db('test.db')

    # Create a User Object
    user = User()
    user.attrs['user_id'] = 1

    # Check if the student was retrieved from DB
    assert user.get (db) == 0

    # Delete the user
    assert user.delete (db) == 0

    db.close_db()

def test_authenticate():
    # reset the DB to a known state
    refresh_users ('test.db', True)

    # open the DB
    db = Database()
    db.open_db('test.db')

    # create a user
    user = User()

    # authenticate a user
    assert user.authenticate (db, 'tomg', 'ironhand') == True

    db.close_db()
