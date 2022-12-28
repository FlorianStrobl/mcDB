import addImport
import sqlite3
import SQL
from TmpData import *
from Logger import *
import random
from InputStrToMapFilterSort import *

# print(executeUserStr("playerId2 - playerId1", "auto", ["test", "playerId"], [[0, 54], [0, 55]]))

# TODO, TMP.sort() needs to be a stable sort
# TODO, (val1, val2) <- (354, 95834)
# TODO return only 50 elements in tmp for getPage(nr, nrOfElemPerPage)
# TODO foreign keys are correct

cursor = sqlite3.connect("minecraftDatabase.db").cursor()

SQL.dropAllTables(cursor)  # delete current db
SQL.createAllTables(cursor)  # create all tables
SQL.fillAllTablesRand(cursor, 100)  # fill random data into the tables
# Start UI

table = "Serverworld"
tmp = TMP()
tmp.setData(
    data=SQL.selectTable(cursor, table),
    columnNames=SQL.selectTableColumns(cursor, table),
    tableName=table,
)

#tmp.setData(tmp.editData("""icon <- 'test' if icon is None else icon"""))

updateDataInDB(cursor, tmp)

"""
1. DROP all TABLES
2. CREATE all TABLES
3. fill all tables with random data
4. UI
-> buttons (select * from table) => data tmp (workArray)
-> ultimative SQL "searchbar" (select columns from table where)
  => data tmp (workArray)
  -> select/show data tmp
  -> update data tmp
    -> preview tmp array with lambda
  -> insert/create data tmp
  -> delete data tmp
    -> save data tmp to database
"""
