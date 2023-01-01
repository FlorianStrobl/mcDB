import sqlite3
import random
import addImport
from Logger import *
import SQL
from TmpData import *
from InputStrToMapFilterSort import *
from GUI.main import loadGUI

# TODO foreign keys are correct

cursor = sqlite3.connect("minecraftDatabase.db").cursor()

SQL.dropAllTables(cursor)  # delete current db
SQL.createAllTables(cursor)  # create all tables
SQL.fillAllTablesRand(cursor, 10)  # fill random data into the tables

table = "plays"
tmp = TMP()
tmp.setData(
    data=SQL.selectTable(cursor, table),
    columnNames=SQL.selectTableColumns(cursor, table),
    tableName=table,
)

# tmp.setData(tmp.editData("""int((absolute_position1).split(", ")[0][1:]) - int((absolute_position2).split(", ")[0][1:]) && block_type1 - block_type2""", "sort"))

v = tmp.editData(
    """
    (session_begin1 - session_begin2) if (role1 == role2) else (1 if (role2 == "Player" or role1 != "Player" and role1 != "Moderator") else -1)

    && (session_begin, role) <- (session_begin//2, role + "'s")

    && slice 0,3

    && role.lower() != "rand"
""", "auto"
)
tmp.replaceTmp(v)
v = tmp.editData("""session_begin <- 0 && session_begin, player_id, serverworld_id, role, player_position""") # TODO, if i swap, should i swap the order of the columns in the UI too?
tmp.replaceTmp(v)
updateDataInDB(cursor, tmp)

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
