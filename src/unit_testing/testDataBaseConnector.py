import unittest
import databaseconnector.DataBaseConnector as DBC
import sqlite3
import os

class testDataBaseConnector(unittest.TestCase):
    """Testing database connector"""
    def setUp(self):
        """setUp for testing with different ini-files to check correct behaviour"""
        self.connector = DBC.DataBaseConnector()
        filepath = 'unit_testing/testdata/'
        self.noIni = filepath+'nofile'
        self.wrongIni = filepath+'wrongDB.ini'
        self.wrongMap = filepath+'wrongMapInfoDB.ini'
        self.correctIni = filepath+'correctDB.ini'
        self.existingDB = filepath+'existing.DB'
        
    def test_noIniFile(self):
        self.assertRaises(DBC.iniFileError, self.connector.CreateDB, 'name.db',self.noIni)

    def test_incorrectIniFile(self):
        self.assertRaises(DBC.iniFileError, self.connector.CreateDB, 'name.db', self.wrongIni)
    
    def test_incorrectMapInfo(self):
        self.assertRaises(DBC.iniFileError, self.connector.CreateDB, 'name.db', self.wrongMap)

    def test_correctIniFileCreatesConnection(self):
        connection = self.connector.CreateDB('name.db', self.correctIni)
        self.assertIsInstance(connection, sqlite3.Connection)
        if os.path.exists('name.db'):
            os.remove('name.db')

    def test_correctIniFileConnectionProducesCorrectMetaData(self):
        connection = self.connector.CreateDB('name.db', self.correctIni)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM DBmeta")
        row = cursor.fetchone()
        correctmeta = ('name.db', 0.1, 'minimal setup for testing purposes')
        self.assertEqual(row, correctmeta, 'Failed on metadata')

        if os.path.exists('name.db'):
            os.remove('name.db')

    def test_correctDBStructure(self):
        connection = self.connector.CreateDB('name.db', self.correctIni)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'")
        result = cursor.fetchall()
        correctNumberOfTables = 25
        self.assertEqual(len(result), correctNumberOfTables, 'WrongNumberOfTAbles')
        if os.path.exists('name.db'):
            os.remove('name.db')


    def test_overwriteExistingDB(self):
        self.assertRaises(DBC.DBError, self.connector.CreateDB, self.existingDB, self.correctIni)