# region imports
import sqlite3

# import tkinter
import ddl

# import genData
# endregion

"""
DROP all TABLES
CREATE all TABLES
fill all tables with random data

UI
-> ultimative SQL "searchbar"
-> show data
-> update data
-> create data
-> delete data
"""

connection = sqlite3.connect("minecraftDatabase.db")
cursor = connection.cursor()

ddl.dropAllDatabases(cursor)
ddl.createAllDatabases(cursor)
ddl.fillAllDatabasesRand(cursor, 10)

# cursor.execute("""INSERT INTO Serverworld (serverworld_id, name, icon)
# VALUES (7,"s","j");""")

# print(cursor.execute("""select * from Serverworld""").fetchall())
