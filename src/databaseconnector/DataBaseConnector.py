import configparser
import os
import sqlite3

class iniFileError(Exception):
    """Error class for ini-files."""
    pass

class DBError(Exception):
    """Error class for database related errors."""
    pass

class DataBaseConnector:
    """Class for connecting to database."""

    def CreateDB(self, name, inipath):
        """Create database.

        Keyword arguments:
        name -- filename for the database
        inipath -- filepath for the initiation file
        
        """
        if os.path.exists(name):
            raise DBError(f'File {name} exists, will not overwrite')
        self.ReadIni(inipath)
        filename = (f'file:{name}?mode=rwc')
        connection = sqlite3.connect(filename,uri=True)
        return connection


    def ReadMapInfo(self, inipath, dbIniConnector):
        """Read map information from the ini-file.

        Keyword arguments:
        inipath -- filepath for the initiation file (for error msg purposes)
        dbIniConnector -- config parser connector
        """
        map = dict()
        if dbIniConnector.has_section('map'):
            #Find section map from the ini-file
            map_areas = dbIniConnector.get('map','areas').split(',')
            #Find areas defined in the map
            for area in map_areas:
                area=area.strip()
                if dbIniConnector.has_option(area,'zones'):
                    #Find zones in map area from the ini file
                    map[area]=dbIniConnector.get(area,'zones').split(',')
                else:
                    raise iniFileError(f'Ini file {inipath} map info is inconsistent')
                    
        else:
            raise iniFileError(f'Ini file {inipath} does not have map info')
        return map


    def ReadIni(self, inipath):
        """Ini-file reader.
        
        Keyword arguments:
        inipath -- filepath to the ini-file
        """
        dbIni = configparser.ConfigParser()
        try:
            dbIni.read_file(open(inipath))
        except Exception as err:
            raise iniFileError(f'Unable to open {inipath}')
        if dbIni.has_option('metadata','use'):
            if not dbIni.get('metadata','use') == 'dbinit':
                raise iniFileError(f'Initfile {inipath} is not for database init')
        else:
            raise iniFileError(f'Initfile {inipath} does not have use defined')
        
        map = self.ReadMapInfo(inipath,dbIni)

        return
    
