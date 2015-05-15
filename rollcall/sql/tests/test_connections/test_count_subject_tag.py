import unittest
import os
from rollcall.exce import SubjectError, UnknownTag
from rollcall.sql.tests import helper
from rollcall.sql.rollcallSQLClass import full_path_to, \
get_count_subject_tag, get_total_class_subject, get_subjects

class TestCountSubjectTag(unittest.TestCase):
    """
    Testing class
    """
    def setUp(self):
        self.dbName = 'rollcall_check.db'
        self.dire = os.path.dirname(__file__)
        self.dbPath = full_path_to(self.dbName, self.dire)
        helper.hadd_subjects(self.dbPath)
        helper.hupdate_subjects(self.dbPath)

    def test_count_tag(self):
        for eachSub in get_subjects(self.dbPath):
            self.assertEqual(get_count_subject_tag(eachSub, 'p', self.dbPath), 2)
            self.assertEqual(get_count_subject_tag(eachSub, 'a', self.dbPath), 1)

            self.assertEqual(get_total_class_subject(eachSub, self.dbPath), 3)

        goodName = 'Maths'
        badName = 'Scala'

        self.assertRaises(SubjectError, get_count_subject_tag, badName, 'p', self.dbPath)
        self.assertRaises(UnknownTag, get_count_subject_tag, goodName, 'zz', self.dbPath)

    def tearDown(self):
        os.remove(self.dbPath)
