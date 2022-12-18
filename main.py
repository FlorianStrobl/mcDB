import sys
sys.path.append(".\Backend")
sys.path.append(".\GUI")

import sqlite3
import SQL
from TmpData import *

cursor = sqlite3.connect("minecraftDatabase.db").cursor()

SQL.dropAllTables(cursor) # delete current db
SQL.createAllTables(cursor) # create all tables
SQL.fillAllTablesRand(cursor, 100) # fill random data into the tables
# Start UI

tmp = TMP()
tmp.setData(SQL.selectTable(cursor, "Wood"))
#tmp.printThis()

# select data from TMP

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