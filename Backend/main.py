import sqlite3
import random
import addImport
import SQL
from TmpData import *
from InputStrToMapFilterSort import *
from GUI.main import *

# TODO, (val1, val2) <- (354, 95834)
# TODO foreign keys are correct

cursor = sqlite3.connect("minecraftDatabase.db").cursor()

SQL.dropAllTables(cursor)  # delete current db
SQL.createAllTables(cursor)  # create all tables
SQL.fillAllTablesRand(cursor, 20)  # fill random data into the tables

table = "plays"
tmp = TMP()
tmp.setData(
    data=SQL.selectTable(cursor, table),
    columnNames=SQL.selectTableColumns(cursor, table),
    tableName=table,
)

# tmp.setData(tmp.editData("""int((absolute_position1).split(", ")[0][1:]) - int((absolute_position2).split(", ")[0][1:]) && block_type1 - block_type2""", "sort"))
tmp.setData(tmp.editData("""(session_begin) <- random.randint(5, 12) &&session_begin1 - session_begin2 &&(0 if role1 == role2 else (-1 if role1 == "Player" else (1 if role2 == "Player" else (-1 if role1 == "Moderator" else 1)))) &&session_begin <= 8"""))
#tmp.setData(tmp.editData("""(session_begin) <- random.randint(5, 12)"""))

updateDataInDB(cursor, tmp)

from GUI.main import loadGUI
loadGUI()

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
