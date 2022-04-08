import pytest
from db import *

def test_Database():
    # Open the database and get the Connection and Cursor

    # Create a Datbase object
    db = Database()
    assert db.conn is None
    assert db.cursor is None

    # Open the DB
    assert db.open_db('test.db') == 0
    assert db.conn is not None
    assert db.cursor is not None

    # Close the DB
    assert db.close_db() == 0
    assert db.conn is None
    assert db.cursor is None
