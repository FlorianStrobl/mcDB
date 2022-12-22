# Schnittestelle von GUI
"""
Funktionen:
setTables(columnsNames, tables[])
...

"""

def onTableButtonClick(tableName):
    print(tableName)

# changes: [[row,column,newText]]
def onTableSave(tableName, changes):
    print(tableName, changes)
