from GenData import GenerateTableData as GTD
import DDL

# get [keys, values] from an object
def getKeyValues(dictionnary: dict) -> [[str], [str]]:
    keys = []
    values = []
    for key, value in dictionnary.items():
        keys.append(key)
        values.append(value)
    return [keys, values]


# get DDL.py values
def getAllTableStr() -> [[str], [str]]:
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
        cursor.execute(tableStr)
    cursor.connection.commit()


# sqlite3: DROP TABLE
def dropAllTables(cursor) -> None:
    keys = getAllTableStr()[0]
    for key in keys:
        cursor.execute(f"DROP TABLE IF EXISTS {key};")
    cursor.connection.commit()


# sqlite3: INSERT INTO, random values
def fillAllTablesRand(cursor, nr: int = 1) -> None:
    allTables = getAllTableStr()[0]  # keys
    for table in allTables:
        if table == "Serverworld":
            tmpData = GTD.generateServerworlds(nr)
            for data in tmpData:
                if data[2] is None:
                    cursor.execute(
                        f"INSERT INTO Serverworld (serverworld_id, name, icon) VALUES ({data[0] & (2**33-1)}, '{data[1]}', null)"
                    )
                else:
                    cursor.execute(
                        f"INSERT INTO Serverworld (serverworld_id, name, icon) VALUES ({data[0] & (2**33-1)}, '{data[1]}', '{data[2]}')"
                    )
            cursor.connection.commit()
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
