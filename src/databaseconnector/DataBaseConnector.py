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

        # read data
        data = self.ReadIni(inipath)

        filename = (f'file:{name}?mode=rwc')

        # create connection
        connection = sqlite3.connect(filename,uri=True)

        # save data
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE DBMeta(name TEXT, version REAL, comment TEXT)")
        metadata = {"name": name, "version": data['version'], "comment": data['comment']}
        cursor.execute("INSERT INTO DBMeta VALUES(:name, :version, :comment)", metadata)

        sqlcommands = self.createSQLforDB()
        for command in sqlcommands:
            cursor.execute(command)

        return connection

    def createSQLforDB(self):
        gameInfoSQL = [
            'CREATE TABLE TurnInformation(TurnNumber INTEGER PRIMARY KEY, LeaseAgreements TEXT, PartisanRoll INTEGER, Notes TEXT, year INTEGER, month TEXT)',
            'CREATE TABLE ImpulseInformation(TurnNumber INTEGER, ImpulseNumber INTEGER, side TEXT, impulseAdvance INTEGER, weatherArtic TEXT, weatherNT TEXT, weathermedit TEXT, weatherNMonsoon TEXT, weatherSMonsoon TEXT, weatherST TEXT, ImpulseNotes TEXT, PRIMARY KEY(TurnNumber, ImpulseNumber), FOREIGN KEY(TurnNumber) REFERENCES TurnInformation(TurnNumber))',
            'CREATE TABLE GameInformation(uniqueId INTEGER PRIMARY KEY, CurrentTurn INTEGER, CurrentImpulse INTEGER, Players TEXT, Notes TEXT, FOREIGN KEY(CurrentTurn, CurrentImpulse) REFERENCES ImpulseInformation(TurnNumber, ImpulseNumber))'
            ]
        tablesWOForeignKeys = [
            'CREATE TABLE Country(CountryName TEXT PRIMARY KEY, MajorPower BOOLEAN)',
            'CREATE TABLE UnitID(UnitID INTEGER PRIMARY KEY)',
            'CREATE TABLE Kit(KitName TEXT PRIMARY KEY)',
            'CREATE TABLE LandUnitType(Type TEXT PRIMARY KEY, Class TEXT)',
            'CREATE TABLE AirUnitType(Type TEXT PRIMARY KEY)',
            'CREATE TABLE NavalUnitType(Type2 TEXT PRIMARY KEY, Type TEXT, Class TEXT)'
            ]
        UnitOptionChain = [
            'CREATE TABLE Option(id INTEGER PRIMARY KEY, number INTEGER, name TEXT, description TEXT, KitName TEXT, inUse BOOLEAN, FOREIGN KEY(kitname) REFERENCES kit(KitName) )',
            'CREATE TABLE UnitOptions(optionId INTEGER, unitId INTEGER, PRIMARY KEY(optionId, unitId), FOREIGN KEY(optionId) REFERENCES Option(id), FOREIGN KEY(unitId) REFERENCES UnitID(UnitID))'
            ]
        replaceCounters = [
            'CREATE TABLE LandLease(origUnitID INTEGER, loanUnitId INTEGER, PRIMARY KEY(origUnitID, loanUnitId), FOREIGN KEY(origUnitID) REFERENCES UnitID(UnitID), FOREIGN KEY(loanUnitID) REFERENCES UnitID(UnitID))',
            'CREATE TABLE Replacements(replacedUnitID INTEGER, replacingUnitId INTEGER, PRIMARY KEY(replacedUnitID, ReplacingUnitId), FOREIGN KEY(replacedUnitID) REFERENCES UnitID(UnitID), FOREIGN KEY(ReplacingUnitID) REFERENCES UnitID(UnitID))'
            ]
        unitEntryTables = [
            'CREATE TABLE SpecialEntryUnits(UnitId INTEGER PRIMARY KEY, Reserve BOOLEAN, ge BOOLEAN, geP1 BOOLEAN, geP2 BOOLEAN, CVB BOOLEAN, FOREIGN KEY(UnitID) REFERENCES UnitID(UnitID))',
            'CREATE TABLE CBVUnits(City TEXT, UnitID INTEGER, PRIMARY KEY(City, UnitID), FOREIGN KEY(UnitID) REFERENCES SpecialEntryUnits(UnitID))',
            'CREATE TABLE RegularUnits(year INTEGER, UnitID INTEGER, PRIMARY KEY(year, UnitID), FOREIGN KEY(UnitID) REFERENCES UnitID(UnitID))'
            ]
        statusTables = [
            'CREATE TABLE UnitOnMap(UnitId INTEGER PRIMARY KEY, controlCountry TEXT, FOREIGN KEY(UnitId) REFERENCES UnitID(UnitID), FOREIGN KEY(controlCountry) REFERENCES Country(CountryName))',
            'CREATE TABLE BuildTrack(UnitId INTEGER PRIMARY KEY, controlCountry TEXT, turnsLeft INTEGER, fdShip BOOLEAN, location TEXT, FOREIGN KEY(UnitId) REFERENCES UnitID(UnitID), FOREIGN KEY(controlCountry) REFERENCES Country(CountryName))',
            'CREATE TABLE UnitStatus(UnitId INTEGER PRIMARY KEY, controlCountry TEXT, removed BOOLEAN, scrapped BOOLEAN, forcePool BOOLEAN, reservePool BOOLEAN, repairPool BOOLEAN, LLPool BOOLEAN, FOREIGN KEY(UnitId) REFERENCES UnitID(UnitID), FOREIGN KEY(controlCountry) REFERENCES Country(CountryName))'
            ]
        landUnitSQL = """CREATE TABLE LandUnits(
            UnitId INTEGER PRIMARY KEY, Type TEXT, powerCountry TEXT, homeCountry TEXT, name TEXT, buildTime INTEGER,
            buildCost INTEGER, strength INTEGER, movementSpeed INTEGER, reorgValue INTEGER, divSized BOOLEAN,
            WhitePrint BOOLEAN, railMoved BOOLEAN, towed BOOLEAN, motorized BOOLEAN, SP BOOLEAN, pink BOOLEAN, red BOOLEAN,
            heavyAA BOOLEAN, rocket BOOLEAN, missileFLAK BOOLEAN, elite BOOLEAN, commando BOOLEAN, marine BOOLEAN,
            para BOOLEAN, mountain BOOLEAN, airlanding BOOLEAN, SS BOOLEAN, guards BOOLEAN, Siberian BOOLEAN, NKVD BOOLEAN,
            bicycle BOOLEAN, 
            FOREIGN KEY(UnitId) REFERENCES UnitID(UnitID), 
            FOREIGN KEY(powerCountry) REFERENCES Country(CountryName),
            FOREIGN KEY(homeCountry) REFERENCES Country(CountryName),
            FOREIGN KEY(Type) REFERENCES LandUnitType(Type)
        )"""
        airUnitSQL = """CREATE TABLE AirUnits(
            UnitId INTEGER PRIMARY KEY, Type TEXT, powerCountry TEXT, homeCountry TEXT, unit TEXT, name TEXT, buildTime INTEGER,
            buildCost INTEGER, ATA INTEGER, ATS INTEGER, TAC INTEGER, RNG INTEGER, STR INTEGER, high BOOLEAN,
            atr BOOLEAN, para BOOLEAN, nf BOOLEAN, unarmed BOOLEAN, jet BOOLEAN, tb BOOLEAN, ext BOOLEAN,
            sh BOOLEAN, low BOOLEAN, twinengine BOOLEAN, np BOOLEAN, xatr BOOLEAN, fb BOOLEAN,
            ws BOOLEAN, bs BOOLEAN,
            FOREIGN KEY(UnitId) REFERENCES UnitID(UnitID), 
            FOREIGN KEY(powerCountry) REFERENCES Country(CountryName),
            FOREIGN KEY(homeCountry) REFERENCES Country(CountryName),
            FOREIGN KEY(Type) REFERENCES AirUnitType(Type)
        )
        """
        extraAirSQL = [
            "CREATE TABLE CVPSize(UnitId INTEGER PRIMARY KEY, StartingSize INTEGER, FOREIGN KEY(UnitId) REFERENCES AirUnits(UnitId))",
            "CREATE TABLE CVPSizeDropYear(UnitId INTEGER, DropYear INTEGER, PRIMARY KEY(UnitId, DropYear), FOREIGN KEY(UnitId) REFERENCES AirUnits(UnitId))",
            ]
        NavalUnitSQL = """CREATE TABLE NavalUnits(
            UnitId INTEGER PRIMARY KEY, Type TEXT, powerCountry TEXT, homeCountry TEXT, shipname TEXT, buildTime INTEGER,
            buildCost INTEGER, buildCost2 INTEGER, cc1 INTEGER, cc2 INTEGER, seabox INTEGER, infTransportOnly BOOLEAN,
            schnorkel BOOLEAN, walther BOOLEAN, missile BOOLEAN, milchcow BOOLEAN, ssqValue INTEGER, ATT INTEGER,
            DEF INTEGER, RNG INTEGER, MOV INTEGER, CV INTEGER, SB INTEGER, AA INTEGER, sunkDate DATE, used BOOLEAN,
            FOREIGN KEY(UnitId) REFERENCES UnitID(UnitID), 
            FOREIGN KEY(powerCountry) REFERENCES Country(CountryName),
            FOREIGN KEY(homeCountry) REFERENCES Country(CountryName),
            FOREIGN KEY(Type) REFERENCES NavalUnitType(Type2)
        )
        """
        SQLCommands = gameInfoSQL+tablesWOForeignKeys+UnitOptionChain+replaceCounters+unitEntryTables+statusTables
        SQLCommands.append(landUnitSQL)
        SQLCommands.append(airUnitSQL)
        SQLCommands.append(NavalUnitSQL)
        SQLCommands += extraAirSQL
        return SQLCommands

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
        metadata = dict(dbIni['metadata'])
        map = self.ReadMapInfo(inipath,dbIni)

        return metadata
    
