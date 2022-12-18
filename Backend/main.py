import addImport
import sqlite3
import SQL
from TmpData import *
from Logger import *


cursor = sqlite3.connect("minecraftDatabase.db").cursor()

SQL.dropAllTables(cursor)  # delete current db
SQL.createAllTables(cursor)  # create all tables
SQL.fillAllTablesRand(cursor, 10_000)  # fill random data into the tables
# Start UI

table = "Block"
tmp = TMP()
tmp.setData(
    data=SQL.selectTable(cursor, table),
    columnNames=SQL.selectTableColumns(cursor, table),
    tableName=table,
)
print("original data length:", tmp.length())
print("original data 1?: ", tmp.getData()[0])
print("original data 2?: ", tmp.getData()[tmp.length()-1])

def Test(x):
  x = list(x)
  x[1] += 1
  return x

def Test2(x):
  x = list(x)
  return x[1] > 5

def Test3(x, y):
  x = list(x)
  y = list(y)
  return x[1] - y[1]

print("doing ops")

tmp.setData(tmp.mapData(Test))
print("start sorting")
tmp.setData(tmp.sortData(Test3))
print("finished sorting!")
tmp.setData(tmp.filterData(Test2))

print("")

print("still original data length?:", tmp.length())
print("still original 1?: ", tmp.getData()[0])
print("still original 2?: ", tmp.getData()[tmp.length()-1])

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
