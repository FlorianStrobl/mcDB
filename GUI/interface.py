# Schnittestelle von GUI
"""
Mitgegeben:

Klasse Table:
    self.tableData : ([tableHeader, tableBody])
    self.updateTable() (applys tableData on Table)

"""


def onGuiReady(table):
    return -1


def onTableButtonClick(tableName):
    print(tableName)


def onTableSave():
    print("Save Table")


def onInputfieldChange(text, mode):
    print("New Change:" + text + " on " + mode)
