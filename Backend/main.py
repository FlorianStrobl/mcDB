import sqlite3
import random
import addImport
import SQL
from TmpData import *
from GUI.main import loadGUI

# comment
cursor: sqlite3.Connection.cursor = sqlite3.connect("minecraftDatabase.db").cursor()

# SQL.dropAllTables(cursor)  # do not reset the current db at the start
SQL.createAllTables(cursor)  # create all tables if not exist
# SQL.fillAllTablesRand(cursor, 10)  # do not fill random data into the tables

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
  (b,) <- 3 + len(data) * 0 + index * 0
  &&
  (a, b, c) <- (a, b, c)
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
