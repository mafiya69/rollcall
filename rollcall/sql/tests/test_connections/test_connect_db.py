import unittest
import os
import sqlite3 as sql
from rollcall.sql.rollcallSQLClass import *

class TestSQL(unittest.TestCase):
    """
    Temporary Testing for SQL functions
    """
    def setUp(self):
        self.dbName = 'rollcall_check.db'
        self.dire = os.path.dirname(__file__)
        self.dbPath = find_db_path(self.dbName, self.dire)

    def test_connection(self):
        self.conn = connect_db(self.dbName, self.dire)
        self.assertTrue(isinstance(self.conn, sql.Connection))
        close_db_connection(self.conn)

    def tearDown(self):
        os.remove(self.dbPath)
