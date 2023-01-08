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
        elif table == "Player":
            tmpData = GTD.generatePlayers(nr)
        elif table == "MEntities":
            tmpData = GTD.generateMEntities(nr)
        elif table == "Block":
            tmpData = GTD.generateBlocks(nr)
        elif table == "Wood":
            tmpData = GTD.generateWoods(nr, cursor)
            if tmpData is None:
                Logger.Logger.error(
                   "While generating Wood. Maybe the table 'Block' is empty"
                )
                return None
        elif table == "Dirt":
            tmpData = GTD.generateDirt(nr, cursor)
            if tmpData is None:
                Logger.Logger.error(
                   "While generating Dirt. Maybe the table 'Block' is empty"
                )
                return None
        elif table == "plays":
            tmpData = GTD.generatePlays(nr, cursor)
            if tmpData is None:
                Logger.Logger.error(
                    "While generating plays. Maybe the table 'Player' or 'Serverworld' is empty"
                )
                return None
        elif table == "populatedBy":
            tmpData = GTD.generatePopulatedBy(nr, cursor)
            if tmpData is None:
                Logger.Logger.error(
                    "While generating populatedBy. Maybe the table 'Serverworld' or 'MEntities' is empty"
                )
                return None
        elif table == "buildOf":
            tmpData = GTD.generateBuildOf(nr, cursor)
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
    BULK_INSERT_LIMIT = 5000

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

    tableSQLInsert = {
        "Serverworld": "INSERT INTO Serverworld (serverworld_id, name, icon) VALUES (?, ?, ?)",
        "Player": "INSERT INTO Player (player_id, username, skin) VALUES (?, ?, ?)",
        "MEntities": "INSERT INTO MEntities (m_entities_id, entity_position, birthday, entity_type) VALUES (?, ?, ?, ?)",
        "Block": "INSERT INTO Block (absolute_position, block_type) VALUES (?, ?)",
        "Wood": "INSERT INTO Wood (absolute_position, isOnFire) VALUES (?, ?)",
        "Dirt": "INSERT INTO Dirt (absolute_position, hasGrass) VALUES (?, ?)",
        "plays": "INSERT INTO plays (player_id, serverworld_id, session_begin, player_position, role) VALUES (?, ?, ?, ?, ?)",
        "populatedBy": "INSERT INTO populatedBy (m_entities_id, serverworld_id) VALUES (?, ?)",
        "buildOf":"INSERT INTO buildOf (absolute_position, serverworld_id) VALUES (?, ?)",
    }

    try:
        if not table in tableSQLInsert:
            # the table does not exist!
            Logger.Logger.error("table does not exist", table)
            return False

        if len(tmpData) < BULK_INSERT_LIMIT:
            # single insert for better error messages
            for data in tmpData:
                _data = data
                cursor.execute(tableSQLInsert[table], data)
        else:
            # bulk insert for better performance:
            # saidly no precise error message anymore
            _data = tmpData
            cursor.executemany(
                tableSQLInsert[table],
                tmpData,
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
    cursor, tableName: str, columnNames: str = "*"
) -> Optional[list[list]]:
    try:
        return [
            list(v)
            for v in cursor.execute(
                f"SELECT {columnNames} FROM {tableName}"
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
