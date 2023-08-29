import force_pool_analysis.ExcelReader as ER
import unittest
import pandas as pd

class testExcelReader(unittest.TestCase):
    def setUp(self):
        self.reader = ER.ExcelReader()
        filepath = 'unit_testing/testdata/'
        noFilename = 'notList.xlsx'
        self.noFile = filepath+noFilename
        incorrectMetafile = 'edited.xlsx'
        self.incorrectMeta = filepath+incorrectMetafile
        incorrectDataFile = 'incorrect sheets.xlsx'
        self.incorrectFile = filepath+incorrectDataFile
        incorrectColumnsFile = 'incorrectColumsn.xlsx'
        self.incorrectColumns = filepath+incorrectColumnsFile
        self.correctAirDf = filepath+'airDf.pkl'
        self.correctLandDf = filepath + 'landDf.pkl'
        self.correctNavalDf = filepath + 'navalDf.pkl'


    def test_wrongFileDoesNotExists(self):
        self.assertRaises(ER.dataFileError, self.reader.openFile,self.noFile)

    def test_incorrectFile(self):
        self.assertRaises(ER.dataFileError, self.reader.openFile, self.incorrectFile)

    def test_incorrectColumns(self):
        self.assertRaises(ER.dataFileError, self.reader.openFile, self.incorrectColumns)

    def test_returnsDataFrame(self):
        obj = self.reader.openFile(self.incorrectMeta)
        self.assertIsInstance(obj, ER.unitData)

    def test_returnsWarningOnWrongCreator(self):
        obj = self.reader.openFile(self.incorrectMeta)
        self.assertRegex(obj.warnings, 'File creator not Froon')

    def test_returnsWarningOnWrong(self):
        obj = self.reader.openFile(self.incorrectMeta)
        self.assertRegex(obj.warnings, 'File last save date is not Jan 1st 2019')

    def test_returnsCorrectDataFrames(self):
        obj = self.reader.openFile(self.incorrectMeta)
        dfCorrectLand = pd.read_pickle(self.correctLandDf)
        dfCorrectAir = pd.read_pickle(self.correctAirDf)
        dfCorrectNaval = pd.read_pickle(self.correctNavalDf)
        landEqual = obj.landUnits.equals(dfCorrectLand)
        airEqual = obj.airUnits.equals(dfCorrectAir)
        navalEqual = obj.navalUnits.equals(dfCorrectNaval)

        self.assertTrue(all([landEqual,airEqual,navalEqual]))

if __name__ == '__main__':
    unittest.main()