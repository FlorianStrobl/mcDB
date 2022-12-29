import addImport
import sqlite3
import SQL
from TmpData import *
from Logger import *
import random
from InputStrToMapFilterSort import *

from GUI.main import loadGUI

# print(executeUserStr("playerId2 - playerId1", "auto", ["test", "playerId"], [[0, 54], [0, 55]]))

# TODO, TMP.sort() needs to be a stable sort
# TODO foreign keys are correct
# TODO, (val1, val2) <- (354, 95834)
# not TODO return only 50 elements in tmp for getPage(nr, nrOfElemPerPage)

cursor = sqlite3.connect("minecraftDatabase.db").cursor()

SQL.dropAllTables(cursor)  # delete current db
SQL.createAllTables(cursor)  # create all tables
SQL.fillAllTablesRand(cursor, 1)  # fill random data into the tables

table = "Serverworld"
tmp = TMP()
tmp.setData(
    data=SQL.selectTable(cursor, table),
    columnNames=SQL.selectTableColumns(cursor, table),
    tableName=table,
)

print(tmp.getData()[100-3:])
tmp.setData(tmp.editData("""0""", "sort"))
print(tmp.getData()[:3])

updateDataInDB(cursor, tmp)

# loadGUI()

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
