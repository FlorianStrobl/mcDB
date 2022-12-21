import addImport
import sqlite3
import SQL
from TmpData import *
from Logger import *
import random
from InputStrToMapFilterSort import *

#print(userStrToLambda("playerId2 - playerId1", "auto", ["test", "playerId"], [[0, 54], [0, 55]]))

# TODO, TMP.sort() needs to be a stable sort
# TODO, try .sort() on two datas (or on one data)

cursor = sqlite3.connect("minecraftDatabase.db").cursor()

SQL.dropAllTables(cursor)  # delete current db
SQL.createAllTables(cursor)  # create all tables
SQL.fillAllTablesRand(cursor, 5)  # fill random data into the tables
# Start UI

table = "Dirt"
tmp = TMP()
tmp.setData(
    data=SQL.selectTable(cursor, table),
    columnNames=SQL.selectTableColumns(cursor, table),
    tableName=table,
)
#tmp.printThis()
tmp.setData(tmp.mapData("hasGrass <- 857"))
tmp.setData(tmp.filterData("hasGrass == 857"))
tmp.setData(tmp.sortData(lambda x, y: x[1] - y[1]))
#tmp.printThis()

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
