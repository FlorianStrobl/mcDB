import sqlite3
import SQL

cursor = sqlite3.connect("minecraftDatabase.db").cursor()

SQL.dropAllTables(cursor) # delete current db
SQL.createAllTables(cursor) # create all tables
SQL.fillAllTablesRand(cursor, 100) # fill random data into the tables
# Start UI

print(SQL.selectTable(cursor, "Wood", "absolute_position"))

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