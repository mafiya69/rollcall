#!/usr/bin/env python2

"""
Helper Module for SQL Tests
"""

import os
from os.path import realpath, dirname
import sys

import rollcall.sql.rollcallSQLClass as rcsql

def hadd_subjects(dbPath):
    """
    Helper Method which add subjects to DB at dbPath
    """
    rcsql.add_subject('Maths', dbPath)
    rcsql.add_subject('Physics', dbPath)
    rcsql.add_subject('Chemistry', dbPath)
    rcsql.add_subject('Python', dbPath)

def hupdate_subjects(dbPath):
    """
    Helper Method which updates each subject with two 'p' & one 'a'
    """
    for subject in rcsql.get_subjects(dbPath):
        rcsql.update_subject(subject, 'p', dbPath)
        rcsql.update_subject(subject, 'p', dbPath)
        rcsql.update_subject(subject, 'a', dbPath)
