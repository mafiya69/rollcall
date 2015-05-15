import unittest
import os
from rollcall.exce import SubjectError, UnknownTag
from rollcall.sql.tests import helper
from rollcall.sql.rollcallSQLClass import full_path_to, update_subject

class TestUpdateSubject(unittest.TestCase):
    """
    Testing class
    """
    def setUp(self):
        self.dbName = 'rollcall_check.db'
        self.dire = os.path.dirname(__file__)
        self.dbPath = full_path_to(self.dbName, self.dire)
        self.dummyPath = '/lol/'
        helper.hadd_subjects(self.dbPath)

    def test_update_subject(self):
        newName = 'Haskell'
        oldName = 'Maths'

        self.assertRaises(SubjectError, update_subject, newName, 'p', self.dbPath)
        self.assertRaises(UnknownTag, update_subject, oldName, 'zz', self.dbPath)

        update_subject(oldName, 'a', self.dbPath)

    def tearDown(self):
        os.remove(self.dbPath)
