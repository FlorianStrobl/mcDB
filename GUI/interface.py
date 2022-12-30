import addImport
import sqlite3
import sys
from TmpData import *
import SQL


table = None
pageSystem = None

cursor = sqlite3.connect("minecraftDatabase.db").cursor()
tmp = TMP()

currentTableName = None


def onGuiReady2(_table, _pageSystem):
    global table
    global pageSystem

    table = _table
    pageSystem = _pageSystem


def onTableButtonClick(tableName):
    global table
    global pageSystem
    global cursor
    global currentTableName
    # names = list(cursor.description)

    tmp.setData(
        data=SQL.selectTable(cursor, tableName),
        columnNames=SQL.selectTableColumns(cursor, tableName),
        tableName=tableName,
    )
    columnNames = list(map(lambda x: x[0], cursor.description))

    # print(columnNames)
    print(tmp.getData())
    pageSystem.changeTableBody(tmp.getData())
    table.setTableHeader(columnNames)

    currentTableName = tableName
    # pageSystem.changeTableBody([[i,"j","l","l","l"] for i in range(100)])


def onTableSave(table):
    global pageSystem
    global currentTableName
    global cursor

    tmp.setData(pageSystem.getInput())
    updateDataInDB(cursor, tmp)
    print(table.getTablesInputs())


def onInputfieldChange(text, mode):
    print("New Change:" + text + " on " + mode)
