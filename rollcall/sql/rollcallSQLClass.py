#!/usr/bin/env python2
#ref : http://zetcode.com/db/sqlitepythontutorial/

"""
SQL Class rollcall
"""

from __future__ import print_function
import os
import sys
import rollcall.exce
from rollcall.func_json import TAGS
from rollcall.main import pDir

try:
    import sqlite3 as sql
except ImportError:
    print("SQLite3 is not found!")
    sys.exit()

def find_db_path(dbName, dire = pDir()):
    """
    Generates the complete path of a DB
    returns the complete path
    """
    path = os.path.join(os.path.dirname(dire), dbName)
    return path

def connect_db(dbName, dire = pDir()):
    """
    Connect to DB
    and Return the sqlite3.Connection object
    """
    dbPath = find_db_path(dbName, dire)
    conn = sql.connect(dbPath)
    return conn

def close_db_connection(conn):
    """
    close the connection 'conn'
    where conn is sqlite3.Connection object
    """
    conn.close()

#Todo : Add tests
def get_subjects(dbName = 'rollcall.db'):
    """
    Get a List of All Subjects Present in DB
    yield subject
    """
    conn = connect_db(dbName)
    command = """SELECT name FROM sqlite_master WHERE type='table'"""
    try:
        subList = conn.execute(command)
        subList = subList.fetchall()
    except:
        conn.rollback()
        close_db_connection(conn)
        raise exce.DatabaseError("Some problem occurred in DB!")
    for sub in subList:
        yield sub[0]

#Todo : Add tests
def get_count_subject_tag(subName, tag = 'p', dbName = 'rollcall.db'):
    """
    Get the number of classes in Subject with tag
    """

    if not TAGS.has_key(tag):
        raise exce.UnknownTag("Tag: %s UNKNOWN" %(tag))

    if not subName in getSubjectList():
        raise exce.SubjectError("There is no records for %s." %(subName))

    conn = connect_db(dbName)
    command = """SELECT COUNT(*) FROM %s
    WHERE class_tag=\"%s\"""" % (subName, TAGS[tag])
    try:
        count = conn.execute(command)
        count = count.fetchall()
    except:
        conn.rollback()
        close_db_connection(conn)
        raise exce.DatabaseError("Some problem occurred in DB!")
    return count[0][0]

#Todo : Add tests
def get_total_class_subject(subName, dbName = 'rollcall.db'):
    """
    Get the total classes happened till date
    """

    if not subName in getSubjectList():
        raise exce.SubjectError("There is no records for %s." %(subName))

    conn = connect_db(dbName)
    command = """SELECT COUNT(*) FROM %s""" % (subName)
    try:
        count = conn.execute(command)
        count = count.fetchall()
    except:
        conn.rollback()
        close_db_connection(conn)
        raise exce.DatabaseError("Some problem occurred in DB!")
    return count[0][0]

#Todo : Add tests
def add_subject(subName, dbName = 'rollcall.db'):
    """
    Add a Subject to the DB
    """

    if subName in getSubjectList():
        raise exce.SubjectExists("Records for %s are already present." %(subName))

    conn = connect_db(dbName)
    cur = conn.cursor()
    command = """CREATE TABLE %s
        (
        class_no INTEGER NOT NULL,
        class_tag VARCHAR(10) NOT NULL
        CONSTRAINT chk_tag CHECK (class_tag IN ("absent",
        "present", "future", "holiday", "other")),
        class_date DATETIME NOT NULL DEFAULT(DATETIME('now', 'localtime')),
        PRIMARY KEY (class_no)
        )""" % subName
    try:
        cur.execute(command)
        conn.commit()
    except:
        conn.rollback()
        close_db_connection(conn)
        raise exce.DatabaseError("Some problem occurred in DB!")
    close_db_connection(conn)

#Todo : add tests
def delete_subject(subName, dbName = 'rollcall.db'):
    """
    Delete a Subject if Made by mistake :)
    """

    if not subName in getSubjectList():
        raise exce.SubjectError("There is no records for %s." %(subName))

    conn = connect_db(dbName)
    cur = conn.cursor()
    command = """DROP TABLE %s""" % subName
    try:
        cur.execute(command)
        conn.commit()
    except:
        conn.rollback()
        close_db_connection(conn)
        raise exce.DatabaseError("Some problem occurred in DB!")
    close_db_connection(conn)

#Todo : add tests
def update_subject(subName, tag = 'p', dbName = 'rollcall.db'):
    """
    Update Subject with Tag
    """

    if not TAGS.has_key(tag):
        raise exce.UnknownTag("Tag: %s UNKNOWN" %(tag))

    if not subName in getSubjectList():
        raise exce.SubjectError("There is no records for %s." %(subName))

    conn = connect_db(dbName)
    cur = conn.cursor()
    command = """INSERT INTO %s (class_tag)
    VALUES (\"%s\")""" %(subName, TAGS[tag])
    try:
        cur.execute(command)
        conn.commit()
    except:
        conn.rollback()
        close_db_connection(conn)
        raise exce.DatabaseError("Some problem occurred in DB!")
    close_db_connection(conn)

#Todo : Add tests
def get_subject_tag_percent(subName, tag = 'p', dbName = 'rollcall.db'):
    """
    Get Percent of tag in subName in total Records till Date
    """

    if not TAGS.has_key(tag):
        raise exce.UnknownTag("Tag: %s UNKNOWN" %(tag))

    if not subName in getSubjectList():
        raise exce.SubjectError("There is no records for %s." %(subName))

    countTag = getCountSubjectTag(subName, tag, dbName)
    countTotal = getTotalClassesSubject(subName)
    fract = countTag * 1.0 / countTotal
    return fract*100
