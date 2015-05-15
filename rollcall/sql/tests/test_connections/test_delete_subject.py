import unittest
import os
from rollcall.exce import SubjectError, DatabaseError
from rollcall.sql.tests import helper
from rollcall.sql.rollcallSQLClass import delete_subject, full_path_to

class TestDeleteSubject(unittest.TestCase):
    """
    Testing class
    """
    def setUp(self):
        self.dbName = 'rollcall_check.db'
        self.dire = os.path.dirname(__file__)
        self.dbPath = full_path_to(self.dbName, self.dire)
        self.dummyPath = '/lol/'
        helper.hadd_subjects(self.dbPath)

    def test_delete_subject(self):
        newName = 'Haskell'
        oldName = 'Maths'

        self.assertRaises(SubjectError, delete_subject, newName, self.dbPath)
        delete_subject(oldName, self.dbPath)
        self.assertRaises(DatabaseError, delete_subject, oldName, self.dummyPath)

    def tearDown(self):
        os.remove(self.dbPath)
