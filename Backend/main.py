import sqlite3
import random
import addImport
from Logger import *
import SQL
from TmpData import *
from InputStrToMapFilterSort import *
from GUI.main import loadGUI

cursor: sqlite3.Connection.cursor = sqlite3.connect("minecraftDatabase.db").cursor()

SQL.dropAllTables(cursor)  # reset the current db
SQL.createAllTables(cursor)  # create all tables
SQL.fillAllTablesRand(cursor, 151)  # fill random data into the tables

# DEBUG Code
_tmp = TMP()
_tmp.setData(
    data=[
        [5, 8, "6"],
        [7, 3, "hey"],
        [44, 5, "6"],
        [1, 7, None],
    ],
    columnNames=["a", "b", "c"],
    tableName="DEBUG",
)
# test: "slice", ,"columns", "sort", "map", "filter"
_tmp.replaceTmp(
    _tmp.editData(
        """
  slice 1; length
  &&
  b, c, a
  &&
  a1 - a2
  &&
  b <- 3 + len(data) * 0 + index * 0
  &&
  a < 44
  &&
  True
""",
        "auto",
        True,
    )
)  # execute an edit data which should work without printing an error
print(
    "Edit Data Works:",
    _tmp.tableName == "DEBUG"
    and _tmp.columnNames == ["b", "c", "a"]
    and _tmp.data == [[3, None, 1], [3, "hey", 7]],
)

loadGUI()

# v = tmp.editData("""session_begin <- 0 && session_begin, player_id, serverworld_id, role, player_position""") # TODO, if i swap, should i swap the order of the columns in the UI too?
