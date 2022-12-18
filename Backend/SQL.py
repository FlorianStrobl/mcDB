from GenData import GenerateTableData as GTD
import DDL
from Logger import *

# get [keys, values] from an object
def getKeyValues(dictionnary: dict) -> [list[str], list[str]]:
    keys = []
    values = []
    for key, value in dictionnary.items():
        keys.append(key)
        values.append(value)
    return [keys, values]


# get DDL.py values
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


# sqlite3: DROP TABLE
def dropAllTables(cursor) -> None:
    keys = getAllTableStr()[0]
    for key in keys:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {key};")
        except:
            Logger.error("while dropping table", key)
    cursor.connection.commit()


# sqlite3: INSERT INTO, random values
def fillAllTablesRand(cursor, nr: int = 1) -> None:
    allTables = getAllTableStr()[0]  # keys
    for table in allTables:
        if table == "Serverworld":
            tmpData = GTD.generateServerworlds(nr)
            for data in tmpData:
                try:
                    if data[2] is None:
                        cursor.execute(
                            f"INSERT INTO Serverworld (serverworld_id, name, icon) VALUES ({data[0]}, '{data[1]}', null)"
                        )
                    else:
                        cursor.execute(
                            f"INSERT INTO Serverworld (serverworld_id, name, icon) VALUES ({data[0]}, '{data[1]}', '{data[2]}')"
                        )
                except:
                    Logger.error("while inserting", data)
            cursor.connection.commit()
        elif table == "Player":
            tmpData = GTD.generatePlayers(nr)
            for data in tmpData:
                try:
                    cursor.execute(
                        f"INSERT INTO Player (player_id, username, skin) VALUES ({data[0]}, '{data[1]}', '{data[2]}')"
                    )
                except:
                    Logger.error("while inserting", data)
            cursor.connection.commit()
        elif table == "MEntities":
            tmpData = GTD.generateMEntities(nr)
            for data in tmpData:
                try:
                    cursor.execute(
                        f"INSERT INTO MEntities (m_entities_id, entity_postion, birthday, entity_type) VALUES ({data[0]}, '{data[1]}', {data[2]}, {data[3]})"
                    )
                except:
                    Logger.error("while inserting", data)
            cursor.connection.commit()
        elif table == "Block":
            tmpData = GTD.generateBlocks(nr)
            for data in tmpData:
                try:
                    cursor.execute(
                        f"INSERT INTO Block (absolute_position, block_type) VALUES ('{data[0]}', {data[1]})"
                    )
                except:
                    Logger.error("while inserting", data)
            cursor.connection.commit()
        elif table == "Wood":
            tmpData = GTD.generateWoods(nr)
            for data in tmpData:
                # TODO absolute_position has to exist in Block
                try:
                    cursor.execute(
                        f"INSERT INTO Wood (absolute_position, isOnFire) VALUES ('{data[0]}', {data[1]})"
                    )
                except:
                    Logger.error("while inserting", data)
            cursor.connection.commit()
        elif table == "Dirt":
            tmpData = GTD.generateDirt(nr)
            for data in tmpData:
                # TODO absolute_position has to exist in Block
                try:
                    cursor.execute(
                        f"INSERT INTO Dirt (absolute_position, hasGras) VALUES ('{data[0]}', {data[1]})"
                    )
                except:
                    Logger.error("while inserting", data)
            cursor.connection.commit()
        elif table == "plays":
            tmpData = GTD.generatePlays(nr)
            # TODO
            for data in tmpData:
                try:
                    cursor.execute(
                        f"INSERT INTO plays (player_id, serverworld_id, session_begin, player_position, role) VALUES ({data[0]}, {data[1]}, {data[2]}, '{data[3]}', '{data[4]}')"
                    )
                except:
                    Logger.error("while inserting", data)
            cursor.connection.commit()
        elif table == "populatedBy":
            tmpData = GTD.generatePopulatedBy(nr)
            # TODO
            for data in tmpData:
                try:
                    cursor.execute(
                        f"INSERT INTO populatedBy (m_entities_id, serverworld_id) VALUES ({data[0]}, {data[1]})"
                    )
                except:
                    Logger.error("while inserting", data)
            cursor.connection.commit()
        elif table == "buildOf":
            tmpData = GTD.generateBuildOf(nr)
            # TODO
            for data in tmpData:
                try:
                    cursor.execute(
                        f"INSERT INTO buildOf (absolute_position, serverworld_id) VALUES ('{data[0]}', {data[1]})"
                    )
                except:
                    Logger.error("while inserting", data)
            cursor.connection.commit()


# sqlite3: SELECT, e.g. selectTable(cursor, "Wood", "absolute_position", "isOnFire==1")
def selectTable(
    cursor, tableName: str, columnNames: str = "*", where: str = "True"
) -> list[tuple]:
    try:
        return cursor.execute(
            f"SELECT {columnNames} FROM {tableName} where {where}"
        ).fetchall()
    except:
        Logger.error("while fetching data from table", tableName)
    return []

def selectTableColumns(cursor, tableName: str) -> list:
    try:
        cursor.execute(f"SELECT * from {tableName}")
        return [description[0] for description in cursor.description]
    except:
        Logger.error("while fetching the column names from table", tableName)
    return []