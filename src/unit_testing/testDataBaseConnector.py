import unittest
import databaseconnector.DataBaseConnector as DBC
import sqlite3
import os

class testDataBaseConnector(unittest.TestCase):
    def setUp(self):
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

    def test_correctIniFile(self):
        connection = self.connector.CreateDB('name.db', self.correctIni)
        self.assertIsInstance(connection, sqlite3.Connection)
        if os.path.exists('name.db'):
            os.remove('name.db')

    def test_overwriteExistingDB(self):
        self.assertRaises(DBC.DBError, self.connector.CreateDB, self.existingDB, self.correctIni)