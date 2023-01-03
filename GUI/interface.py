import sqlite3
import threading
import time
import addImport
from TmpData import *
import SQL

# TODO fix drawTableBody() for empty arrays

table = None
pageSystem = None

cursor = sqlite3.connect("minecraftDatabase.db").cursor()
tmp: TMP = TMP()
preview: TMP = (
    None  # the preview for tmp shall be drawn in the UI table IF it is not None
)
lastInputFieldChangeTime: int = -1 # the last time the inputfield changed its value by the user


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

    data = SQL.selectTable(cursor, tableName)
    if data is None:
        # ERROR
        return
    tmp.setData(
        data=data,
        columnNames=SQL.selectTableColumns(cursor, tableName),
        tableName=tableName,
    )
    columnNames = list(map(lambda x: x[0], cursor.description))

    # print(columnNames)
    # print(tmp.getData())
    pageSystem.changeTableBody(tmp.getData())
    table.setTableHeader(columnNames)

    currentTableName = tableName
    # pageSystem.changeTableBody([[i,"j","l","l","l"] for i in range(100)])


def onTableSave(table):
    global pageSystem
    global currentTableName
    global cursor

    # TODO, No! because if there is a preview
    # which was NOT confirmed by the "Ok" button
    # you may not want to save it/apply the changes
    # BUT what to do if there is a preview and then
    # the user changes a field of the previews
    # saving the preview and replacing TMP then?
    tmp.setData(
        pageSystem.getInput(), None if preview is None else preview.columnNames
    )  # <--

    updateDataInDB(cursor, tmp)
    # print(table.getTablesInputs())


def onInputfieldChange(text, mode):
    # def do():
    #     global lastInputFieldChangeTime

    #     delay = 1000
    #     if lastInputFieldChangeTime + delay > round(time.time() * 1000):
    #         # the text was NOT changed by the user in the last delay time, and the code errored
    #         pageSystem.changeTableBody(tmp.deepCpyData())
    #         table.setTableHeader(tmp.columnNames)
    #         return

    global preview

    # TODO add a delay before ACTUALLY doing the preview to reduce lag of fast text inputs
    global lastInputFieldChangeTime
    curTime = round(time.time() * 1000)
    delay = 1000 # 1s
    if tmp.editData(text, mode) is None and lastInputFieldChangeTime + delay > curTime:
        # but what if tmp.editData(text, mode) STAYS None
        # because if there was a preview before that set
        # this preview is not the one from the inputfield anymore
        # this means preview has to be set to None and TMP needs to be reshown again

        #threading.Timer(1000, do()) # text errored anyway, so do not show preview anymore but TMP
        return
    else:
        lastInputFieldChangeTime = curTime
        # continue execution

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
        table.setTableHeader(preview.columnNames)
    else:
        # TODO remove the "preview mode" text described above
        pageSystem.changeTableBody(tmp.deepCpyData())
        table.setTableHeader(tmp.columnNames)

    # print(f"[{mode}] inputfield: \"{text}\"; got a preview: {preview is not None}")
