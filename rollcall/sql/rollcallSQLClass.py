#!/usr/bin/env python2
#ref : http://zetcode.com/db/sqlitepythontutorial/

"""
SQL Class rollcall
"""

from __future__ import print_function
import os
import sys
import rollcall.exce as exce
from rollcall.func_json import TAGS
from rollcall.main import pDir, full_path_to

try:
    import sqlite3 as sql
except ImportError:
    print("SQLite3 is not found!")
    sys.exit()

dbNameDef = 'rollcall.db'
dbPathDef = full_path_to(dbNameDef)

def connect_db(dbPath = dbPathDef):
    """
    Connect to DB
    and Return the sqlite3.Connection object
    """
    try:
        conn = sql.connect(dbPath)
    except:
        raise exce.DatabaseError("Unable to open Database File!")
    return conn

def close_db_connection(conn):
    """
    close the connection 'conn'
    where conn is sqlite3.Connection object
    """
    conn.close()

def get_subjects(dbPath = dbPathDef):
    """
    Get a List of All Subjects Present in DB
    yield subject
    """
    conn = connect_db(dbPath)
    command = "SELECT name FROM sqlite_master WHERE type='table'"
    try:
        subQuery = conn.execute(command)
        subList = subQuery.fetchall()
    except:
        conn.rollback()
        close_db_connection(conn)
        raise exce.DatabaseError("Some problem occurred in DB!")
    close_db_connection(conn)
    for sub in subList:
        yield sub[0]

def get_count_subject_tag(subName, tag = 'p', dbPath = dbPathDef):
    """
    Get the number of classes in Subject with tag
    """

    if not TAGS.has_key(tag):
        raise exce.UnknownTag("Tag: %s UNKNOWN" %(tag))

    if not subName in get_subjects(dbPath):
        raise exce.SubjectError("There is no records for %s." %(subName))

    conn = connect_db(dbPath)
    command = """SELECT COUNT(*) FROM %s
    WHERE class_tag=\"%s\"""" % (subName, TAGS[tag])
    try:
        count = conn.execute(command)
        count = count.fetchall()
    except:
        conn.rollback()
        close_db_connection(conn)
        raise exce.DatabaseError("Some problem occurred in DB!")
    close_db_connection(conn)
    return count[0][0]

def get_total_class_subject(subName, dbPath = dbPathDef):
    """
    Get the total classes happened till date
    """

    if not subName in get_subjects(dbPath):
        raise exce.SubjectError("There is no records for %s." %(subName))

    conn = connect_db(dbPath)
    command = """SELECT COUNT(*) FROM %s""" % (subName)
    try:
        count = conn.execute(command)
        count = count.fetchall()
    except:
        conn.rollback()
        close_db_connection(conn)
        raise exce.DatabaseError("Some problem occurred in DB!")
    close_db_connection(conn)
    return count[0][0]

#Todo : Add tests
def add_subject(subName, dbPath = dbPathDef):
    """
    Add a Subject to the DB
    """

    if subName in get_subjects(dbPath):
        raise exce.SubjectExists("Records for %s are already present." %(subName))

    conn = connect_db(dbPath)
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
def delete_subject(subName, dbPath = dbPathDef):
    """
    Delete a Subject if Made by mistake :)
    """

    if not subName in get_subjects(dbPath):
        raise exce.SubjectError("There is no records for %s." %(subName))

    conn = connect_db(dbPath)
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

def update_subject(subName, tag = 'p', dbPath = dbPathDef):
    """
    Update Subject with Tag
    """

    if not TAGS.has_key(tag):
        raise exce.UnknownTag("Tag: %s UNKNOWN" %(tag))

    if not subName in get_subjects(dbPath):
        raise exce.SubjectError("There is no records for %s." %(subName))

    conn = connect_db(dbPath)
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

def get_subject_tag_percent(subName, tag = 'p', dbPath = dbPathDef):
    """
    Get Percent of tag in subName in total Records till Date
    """

    if not TAGS.has_key(tag):
        raise exce.UnknownTag("Tag: %s UNKNOWN" %(tag))

    if not subName in get_subjects(dbPath):
        raise exce.SubjectError("There is no records for %s." %(subName))

    count_tag = get_count_subject_tag(subName, tag, dbPath)
    count_total = get_total_class_subject(subName, dbPath)
    fract = count_tag * 1.0 / count_total
    return fract*100
