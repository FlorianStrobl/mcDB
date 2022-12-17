import sqlite3
import DDL as ddl

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

connection = sqlite3.connect("minecraftDatabase.db")
cursor = connection.cursor()

ddl.dropAllDatabases(cursor)
ddl.createAllDatabases(cursor)
ddl.fillAllDatabasesRand(cursor, 150)

# cursor.execute("""INSERT INTO Serverworld (serverworld_id, name, icon)
# VALUES (7,"s","j");""")

# print(cursor.execute("""select * from Serverworld""").fetchall())
