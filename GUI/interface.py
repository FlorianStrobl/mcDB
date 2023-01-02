import sqlite3
import addImport
from TmpData import *
import SQL

# TODO fix drawTableBody() for empty arrays

table = None
pageSystem = None

cursor = sqlite3.connect("minecraftDatabase.db").cursor()
tmp = TMP()
preview = None # the preview for tmp shall be drawn in the UI table IF it is not None

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
    #print(tmp.getData())
    pageSystem.changeTableBody(tmp.getData())
    table.setTableHeader(columnNames)

    currentTableName = tableName
    # pageSystem.changeTableBody([[i,"j","l","l","l"] for i in range(100)])


def onTableSave(table):
    global pageSystem
    global currentTableName
    global cursor

    # TODO, really? because if there is a preview
    # which was NOT confirmed by the "Ok" button
    # you may not want to save it/apply the changes
    tmp.setData(pageSystem.getInput()) # <--

    updateDataInDB(cursor, tmp)
    #print(table.getTablesInputs())


def onInputfieldChange(text, mode):
    if text.strip() == "":
        preview = None

    if mode != "sql" and text.strip() != "":
        vv = tmp.editData(text, mode)
        if vv is None:
            preview = None
        else:
            preview = TMP()
            preview.replaceTmp(vv)

    # TODO change the column names if it was a
    # "select columns" command
    if preview is not None:
        # TODO show in UI somewhere "UNSAVED preview mode, click the 'Ok' Button to apply changes"
        pageSystem.changeTableBody(preview.deepCpyData())
    else:
        # TODO remove the "preview mode" text
        pageSystem.changeTableBody(tmp.deepCpyData())

    print(f"[{mode}] inputfield: \"{text}\"; got a preview: {preview is not None}")
