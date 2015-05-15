import unittest
import os
from rollcall.exce import SubjectError
from rollcall.sql.tests import helper
from rollcall.sql.rollcallSQLClass import full_path_to, get_subject_tag_percent,\
get_subjects

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
        helper.hupdate_subjects(self.dbPath)

    def test_subject_tag_percent(self):
        newName = 'Haskell'
        oldName = 'Maths'

        for eachSub in get_subjects(self.dbPath):
            self.assertAlmostEqual(get_subject_tag_percent(oldName, 'p', self.dbPath), 100.0 * 2.0 / 3.0)
            self.assertAlmostEqual(get_subject_tag_percent(oldName, 'a', self.dbPath), 100.0 * 1.0 / 3.0)
            self.assertAlmostEqual(get_subject_tag_percent(oldName, 'h', self.dbPath), 0.0)

        self.assertRaises(SubjectError, get_subject_tag_percent, newName, 'p', self.dbPath)

    def tearDown(self):
        os.remove(self.dbPath)
