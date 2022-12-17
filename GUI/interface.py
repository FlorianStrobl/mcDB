# Schnittestelle von GUI
"""
Funktionen:
setTables(tables[])
...

"""


def onNewTableShow(tableName):
    print(tableName)

# Wird mehrmals aufgerufen
# changes: [x (from 0),y (from 0),newText]
def onTableSave(tableName, changes):
    print(tableName, changes)