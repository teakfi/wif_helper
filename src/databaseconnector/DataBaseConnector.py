import configparser
import os
import sqlite3

class iniFileError(Exception):
    pass

class DBError(Exception):
    pass

class DataBaseConnector:

    def CreateDB(self, name, inipath):
        if os.path.exists(name):
            raise DBError(f'File {name} exists, will not overwrite')
        self.ReadIni(inipath)
        filename = (f'file:{name}?mode=rwc')
        connection = sqlite3.connect(filename,uri=True)
        return connection


    def ReadMapInfo(self, inipath, dbIniConnector):
        map = dict()
        if dbIniConnector.has_section('map'):
            map_areas = dbIniConnector.get('map','areas').split(',')
            for area in map_areas:
                area=area.strip()
                if dbIniConnector.has_option(area,'zones'):
                    map[area]=dbIniConnector.get(area,'zones').split(',')
                else:
                    raise iniFileError(f'Ini file {inipath} map info is inconsistent')
                    
        else:
            raise iniFileError(f'Ini file {inipath} does not have map info')
        return map


    def ReadIni(self, inipath):
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
    
