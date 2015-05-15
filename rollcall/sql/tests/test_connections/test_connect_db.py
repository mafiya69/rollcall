import unittest
import os
import sqlite3 as sql
from rollcall.sql.rollcallSQLClass import full_path_to, connect_db, close_db_connection
from rollcall.exce import DatabaseError

class TestConnectDB(unittest.TestCase):
    """
    Testing class
    """
    def setUp(self):
        self.dbName = 'rollcall_check.db'
        self.dire = os.path.dirname(__file__)
        self.dbPath = full_path_to(self.dbName, self.dire)
        self.dummyPath = '/lol/'

    def test_connect_db(self):
        self.conn = connect_db(self.dbPath)
        self.assertTrue(isinstance(self.conn, sql.Connection))
        close_db_connection(self.conn)

        self.assertRaises(DatabaseError, connect_db, self.dummyPath)

    def tearDown(self):
        os.remove(self.dbPath)
