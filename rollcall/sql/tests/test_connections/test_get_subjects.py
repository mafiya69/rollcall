import unittest
import os
from rollcall.sql.tests import helper
from rollcall.sql.rollcallSQLClass import full_path_to, get_subjects

class TestGetSubjects(unittest.TestCase):
    """
    Testing class
    """
    def setUp(self):
        self.dbName = 'rollcall_check.db'
        self.dire = os.path.dirname(__file__)
        self.dbPath = full_path_to(self.dbName, self.dire)
        helper.hadd_subjects(self.dbPath)

    def test_get_subject(self):
        subList = list(get_subjects(self.dbPath))
        mySubList=['Maths', 'Physics', 'Chemistry', 'Python']
        for eachSub in mySubList:
            self.assertTrue(eachSub in subList)
        self.assertEqual(len(subList),len(mySubList))

    def tearDown(self):
        os.remove(self.dbPath)
