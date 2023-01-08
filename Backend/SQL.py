from typing import Optional
import addImport
import Logger
import DDL
from GenData import GenerateTableData as GTD


# get [keys, values] from an dictionary
def getKeyValues(dictionnary: dict) -> [list[str], list[str]]:
    keys = []
    values = []
    for key, value in dictionnary.items():
        keys.append(key)
        values.append(value)
    return [keys, values]


# get ./DDL.py dictionary values as [keys, values]
def getAllTableStr() -> [list[str], list[str]]:
    keys = (
        getKeyValues(DDL.tablesStrong)[0]
        + getKeyValues(DDL.tablesWeak)[0]
        + getKeyValues(DDL.tableRelations)[0]
    )
    values = (
        getKeyValues(DDL.tablesStrong)[1]
        + getKeyValues(DDL.tablesWeak)[1]
        + getKeyValues(DDL.tableRelations)[1]
    )
    return [keys, values]


# sqlite3: CREATE TABLE
def createAllTables(cursor) -> None:
    # from all the tables
    for tableStr in getAllTableStr()[1]:
        try:
            cursor.execute(tableStr)
        except:
            Logger.Logger.error("while trying to create table", tableStr)
            returnWHERE
    cursor.connection.commit()


# sqlite3: DROP TABLE (all)
def dropAllTables(cursor) -> None:
    for key in getAllTableStr()[0]:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {key};")
        except:
            Logger.Logger.error("while dropping table", key)
    cursor.connection.commit()


# sqlite3: DROP TABLE (single)
def dropTable(cursor, tableName: str) -> None:
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {tableName};")
    except:
        Logger.Logger.error("while dropping table", tableName)
        return
    cursor.connection.commit()


# fill all tables with random data
def fillAllTablesRand(cursor, nr: int = 1) -> None:
    for table in getAllTableStr()[0]:
        # switch which generates the correct data,
        # INSERT INTO the table, and commits() it to the tables
        tmpData = []
        if table == "Serverworld":
            tmpData = GTD.generateServerworlds(nr)
            #print("did serverworld")
        elif table == "Player":
            tmpData = GTD.generatePlayers(nr)
            #print("did player")
        elif table == "MEntities":
            tmpData = GTD.generateMEntities(nr)
            #print("did MEntities")
        elif table == "Block":
            tmpData = GTD.generateBlocks(nr)
            #print("did block")
        elif table == "Wood":
            tmpData = GTD.generateWoods(nr, cursor)
            #print("did wood")
            if tmpData is None:
                Logger.Logger.error(
                    "While generating Wood. Maybe the table 'Block' is empty"
                )
                return None
        elif table == "Dirt":
            tmpData = GTD.generateDirt(nr, cursor)
            #print("did dirt")
            if tmpData is None:
                Logger.Logger.error(
                    "While generating Dirt. Maybe the table 'Block' is empty"
                )
                return None
        elif table == "plays":
            tmpData = GTD.generatePlays(nr, cursor)
            #print("did play")
            if tmpData is None:
                Logger.Logger.error(
                    "While generating plays. Maybe the table 'Player' or 'Serverworld' is empty"
                )
                return None
        elif table == "populatedBy":
            tmpData = GTD.generatePopulatedBy(nr, cursor)
            #print("did populatedBy")
            if tmpData is None:
                Logger.Logger.error(
                    "While generating populatedBy. Maybe the table 'Serverworld' or 'MEntities' is empty"
                )
                return None
        elif table == "buildOf":
            tmpData = GTD.generateBuildOf(nr, cursor)
            #print("did build of")
            if tmpData is None:
                Logger.Logger.error(
                    "While generating buildOf. Maybe the table 'Serverworld' or 'Block' is empty"
                )
                return None

        # insert the generated data into the DB
        insertIntoTable(cursor, table, tmpData)


# sqlite3: INSERT INTO values for a certain table
# returns True if successful, None if not
def insertIntoTable(cursor, table: str, tmpData: list[list]) -> bool:
    tmpData = list(tmpData)
    _data = None  # data for potential error messag
    # fix strings with " or ' in them
    for i, v in enumerate(tmpData):
        if type(tmpData[i]) == type((1, "some tuple")):
            tmpData[i] = list(tmpData[i])  # fix tuples
        for ii, vv in enumerate(v):
            MAX_INT = 9007199254740991
            if type(vv) == type(""):  # if its a string
                # fix ' and " in strings
                tmpData[i][ii] = tmpData[i][ii].replace("'", "`", MAX_INT)
                tmpData[i][ii] = tmpData[i][ii].replace('"', "`", MAX_INT)

    #print("insert generated data into .db")
    try:
        if table == "Serverworld":
            #print("before for loop")
            for data in tmpData:
                _data = data
                tmpPart = "null"
                if data[2] is not None:
                    tmpPart = f"'{data[2]}'"
                cursor.execute(
                    f"INSERT INTO Serverworld (serverworld_id, name, icon) VALUES ({data[0]}, '{data[1]}', {tmpPart})"
                )
            #print("after for loop")
        elif table == "Player":
            for data in tmpData:
                _data = data
                cursor.execute(
                    f"INSERT INTO Player (player_id, username, skin) VALUES ({data[0]}, '{data[1]}', '{data[2]}')"
                )
        elif table == "MEntities":
            for data in tmpData:
                _data = data
                cursor.execute(
                    f"INSERT INTO MEntities (m_entities_id, entity_position, birthday, entity_type) VALUES ({data[0]}, '{data[1]}', {data[2]}, {data[3]})"
                )
        elif table == "Block":
            for data in tmpData:
                _data = data
                cursor.execute(
                    f"INSERT INTO Block (absolute_position, block_type) VALUES ('{data[0]}', {data[1]})"
                )
        elif table == "Wood":
            for data in tmpData:
                _data = data
                cursor.execute(
                    f"INSERT INTO Wood (absolute_position, isOnFire) VALUES ('{data[0]}', {data[1]})"
                )
        elif table == "Dirt":
            for data in tmpData:
                _data = data
                cursor.execute(
                    f"INSERT INTO Dirt (absolute_position, hasGrass) VALUES ('{data[0]}', {data[1]})"
                )
        elif table == "plays":
            for data in tmpData:
                _data = data
                cursor.execute(
                    f"INSERT INTO plays (player_id, serverworld_id, session_begin, player_position, role) VALUES ({data[0]}, {data[1]}, {data[2]}, '{data[3]}', '{data[4]}')"
                )
        elif table == "populatedBy":
            for data in tmpData:
                _data = data
                cursor.execute(
                    f"INSERT INTO populatedBy (m_entities_id, serverworld_id) VALUES ({data[0]}, {data[1]})"
                )
        elif table == "buildOf":
            for data in tmpData:
                _data = data
                cursor.execute(
                    f"INSERT INTO buildOf (absolute_position, serverworld_id) VALUES ('{data[0]}', {data[1]})"
                )
    except:
        Logger.Logger.error(f"while inserting data into {table} with the data:", _data)
        # raise Exception("bad data")
        return False
    cursor.connection.commit()
    return True


# sqlite3: SELECT
# e.g. selectTable(cursor, "Wood", "absolute_position", "isOnFire==1")
def selectTable(
    cursor, tableName: str, columnNames: str = "*", where: str = "True"
) -> Optional[list[list]]:
    try:
        return [
            list(v)
            for v in cursor.execute(
                f"SELECT {columnNames} FROM {tableName} WHERE {where}"
            ).fetchall()
        ]
    except:
        Logger.Logger.error(
            "while fetching data with the SQLite3 instruction: ",
            f"SELECT {columnNames} FROM {tableName} WHERE {where}",
        )
        return None


# sqlite3: get the column names of a table
def selectTableColumns(cursor, tableName: str) -> Optional[list]:
    try:
        cursor.execute(f"SELECT * FROM {tableName}")
        return [description[0] for description in cursor.description]
    except:
        Logger.Logger.error("while fetching the column names from table", tableName)
        return None
