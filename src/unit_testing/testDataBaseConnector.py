import unittest
import databaseconnector.DataBaseConnector as DBC

class testDataBaseConnector(unittest.TestCase):
    def setUp(self):
        self.connector = DBC.DataBaseConnector()
        filepath = 'unit_testing/testdata/'
        self.noIni = filepath+'nofile'

    def test_noIniFile(self):
        self.assertRaises(DBC.iniFileError, DBC.CreateDB,self.noIni)