import sqlite3
import Funcs

cursor = sqlite3.connect("minecraftDatabase.db").cursor()

Funcs.dropAllTables(cursor) # delete current db
Funcs.createAllTables(cursor) # create all tables
Funcs.fillAllTablesRand(cursor, 15) # fill random data into the tables
# Start UI

# cursor.execute("""SELECT * from Serverworld""").fetchall()

"""
1. DROP all TABLES
2. CREATE all TABLES
3. fill all tables with random data
4. UI
-> buttons (select * from table) => data tmp (workArray)
-> ultimative SQL "searchbar" (select columns from table where)
  => data tmp (workArray)
  -> show/select data tmp
  -> update data tmp
  -> create/insert data tmp
  -> delete data tmp
    -> save data tmp to database
"""