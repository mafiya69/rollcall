import unittest
import os
from rollcall.sql.tests import helper
from rollcall.exce import SubjectExists
from rollcall.sql.rollcallSQLClass import full_path_to, add_subject

class TestAddSubjects(unittest.TestCase):
    """
    Testing class
    """
    def setUp(self):
        self.dbName = 'rollcall_check.db'
        self.dire = os.path.dirname(__file__)
        self.dbPath = full_path_to(self.dbName, self.dire)
        helper.hadd_subjects(self.dbPath)

    def test_add_subject(self):
        newName = 'Haskell'
        oldName = 'Maths'

        self.assertRaises(SubjectExists, add_subject, oldName, self.dbPath)
        add_subject(newName, self.dbPath)

    def tearDown(self):
        os.remove(self.dbPath)
