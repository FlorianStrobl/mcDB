from GenData import GenerateTableData as GTD
import DDL
from Logger import *


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
            Logger.error("while trying to create table", tableStr)
    cursor.connection.commit()

# def createTable(cursor, tableName: str) -> None:
#     # from all the tables
#     for tableStr in getAllTableStr():
#         try:
#             if tableName in tableStr:
#                 cursor.execute(tableStr)
#         except:
#             Logger.error("while trying to create table", tableStr)
#     cursor.connection.commit()

# sqlite3: DROP TABLE (all)
def dropAllTables(cursor) -> None:
    for key in getAllTableStr()[0]:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {key};")
        except:
            Logger.error("while dropping table", key)
    cursor.connection.commit()


# sqlite3: DROP TABLE (single)
def dropTable(cursor, tableName: str) -> None:
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {tableName};")
    except:
        Logger.error("while dropping table", tableName)
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
            tmpData = GTD.generateWoods(nr)
        elif table == "Dirt":
            tmpData = GTD.generateDirt(nr)
        elif table == "plays":
            tmpData = GTD.generatePlays(nr)
        elif table == "populatedBy":
            tmpData = GTD.generatePopulatedBy(nr)
        elif table == "buildOf":
            tmpData = GTD.generateBuildOf(nr)

        # insert the generated data into the DB
        insertIntoTable(cursor, table, tmpData)


# sqlite3: INSERT INTO values for a certain table
def insertIntoTable(cursor, table: str, tmpData: list[any]) -> None:
    _data = None  # data for potential error message
    try:
        if table == "Serverworld":
            for data in tmpData:
                _data = data
                tmpPart = "null"
                if not data[2] is None:
                    tmpPart = f"'{data[2]}'"
                cursor.execute(
                    f"INSERT INTO Serverworld (serverworld_id, name, icon) VALUES ({data[0]}, '{data[1]}', {tmpPart})"
                )
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
                # TODO absolute_position has to exist in Block
                cursor.execute(
                    f"INSERT INTO Wood (absolute_position, isOnFire) VALUES ('{data[0]}', {data[1]})"
                )
        elif table == "Dirt":
            for data in tmpData:
                _data = data
                # TODO absolute_position has to exist in Block
                cursor.execute(
                    f"INSERT INTO Dirt (absolute_position, hasGrass) VALUES ('{data[0]}', {data[1]})"
                )
        elif table == "plays":
            for data in tmpData:
                _data = data
                # TODO player_id and serverworld_id have to exist
                cursor.execute(
                    f"INSERT INTO plays (player_id, serverworld_id, session_begin, player_position, role) VALUES ({data[0]}, {data[1]}, {data[2]}, '{data[3]}', '{data[4]}')"
                )
        elif table == "populatedBy":
            for data in tmpData:
                _data = data
                # TODO m_entities_id and serverworld_id have to exist
                cursor.execute(
                    f"INSERT INTO populatedBy (m_entities_id, serverworld_id) VALUES ({data[0]}, {data[1]})"
                )
        elif table == "buildOf":
            for data in tmpData:
                _data = data
                # TODO absolute_position and serverworld_id have to exist
                cursor.execute(
                    f"INSERT INTO buildOf (absolute_position, serverworld_id) VALUES ('{data[0]}', {data[1]})"
                )
    except:
        Logger.error(f"while inserting data into {table} with the data:", _data)
    cursor.connection.commit()


# sqlite3: UPDATE
def updateDataInTable(cursor, table: str, newData: list[any]) -> None:
    # TODO
    return None


# sqlite3: SELECT
# e.g. selectTable(cursor, "Wood", "absolute_position", "isOnFire==1")
def selectTable(
    cursor, tableName: str, columnNames: str = "*", where: str = "True"
) -> list[list]:
    try:
        return [
            list(v)
            for v in cursor.execute(
                f"SELECT {columnNames} FROM {tableName} where {where}"
            ).fetchall()
        ]
    except:
        Logger.error(
            "while fetching data with the SQLite3 instruction: ",
            f"SELECT {columnNames} FROM {tableName} where {where}",
        )
    return []


# sqlite3: get the column names of a table
def selectTableColumns(cursor, tableName: str) -> list:
    try:
        cursor.execute(f"SELECT * from {tableName}")
        return [description[0] for description in cursor.description]
    except:
        Logger.error("while fetching the column names from table", tableName)
    return []
