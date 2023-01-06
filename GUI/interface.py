import sqlite3
import threading
import customtkinter
import time
import addImport
import Logger
from TmpData import *
import SQL
import shutil

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
searchEntry = None

setButtonSelected = None

def onGuiReady2(_table, _pageSystem,_searchEntry, _setButtonSelected):
    global table
    global pageSystem
    global searchEntry
    global setButtonSelected

    table = _table
    pageSystem = _pageSystem
    searchEntry = _searchEntry

    setButtonSelected = _setButtonSelected

    Logger.Logger.log("")

    onTableButtonClick("Serverworld")

def onTableButtonClick(tableName):
    global table
    global pageSystem
    global cursor
    global currentTableName
    global setButtonSelected
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

    setButtonSelected(tableName)


def onTableSave(table):
    global pageSystem
    global currentTableName
    global cursor
    global tmp
    # TODO, No! because if there is a preview
    # which was NOT confirmed by the "Ok" button
    # you may not want to save it/apply the changes
    # BUT what to do if there is a preview and then
    # the user changes a field of the previews
    # saving the preview and replacing TMP then?

    # ist gemacht

    #onInputfieldChange("","auto")
    previewOn = preview is not None
    ##print("preview enabled:",previewOn)

    if(preview is None):
        tmp.setData(pageSystem.getInput())
    #tmp.setData(
    #    pageSystem.getInput(), None if preview is None else preview.columnNames
    #)  # <--

    tmp.tableName = currentTableName

    updateDataInDB(cursor, tmp)
    # print(table.getTablesInputs())

# this is only for the preview mode
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
    global cursor
    global tmp

    # TODO add a delay before ACTUALLY doing the preview to reduce lag of fast text inputs

    # 1. Get timestamp for everytimne he writes
    # 2.

    # Before preview showed, backup all tmp
    if(preview is None):
        tmp.setData(pageSystem.getInput())

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

    if mode == "sql":
        # do the sql cmd and show the result
        if text.strip() == "":
            preview = None
        if preview is not None:
            Logger.Logger.warn("UNSAVED preview mode, click the 'Ok' Button to apply changes")
            pageSystem.changeTableBody(preview.deepCpyData())
            table.setTableHeader(preview.columnNames)
        else:
            # TODO remove the "preview mode" text described above
            Logger.Logger.warn("")
            pageSystem.changeTableBody(tmp.deepCpyData())
            table.setTableHeader(tmp.columnNames)



        try:
            cursor.execute(text)
            columnNames = list(map(lambda x: x[0], cursor.description))
            resultData = cursor.fetchall()

            preview = TMP()
            preview.data = resultData
            preview.columnNames = columnNames

            pageSystem.changeTableBody(preview.data)
            table.setTableHeader(preview.columnNames)

        except:
            pass
            #return
        return

    if text.strip() == "":
        preview = None

    if mode != "sql" and text.strip() != "":
        vv = tmp.editData(text, mode)
        #print(vv.data)
        if vv is None:
            preview = None
        else:
            preview = TMP()
            preview.replaceTmp(vv)

    # TODO change the column names if it was a
    # "select columns" command
    if preview is not None:
        Logger.Logger.warn("UNSAVED preview mode, click the 'Ok' Button to apply changes")
        pageSystem.changeTableBody(preview.deepCpyData())
        table.setTableHeader(preview.columnNames)
        #print("preview yet")
    else:
        # TODO remove the "preview mode" text described above
        Logger.Logger.warn("")
        pageSystem.changeTableBody(tmp.deepCpyData())
        table.setTableHeader(tmp.columnNames)
    # print(f"[{mode}] inputfield: \"{text}\"; got a preview: {preview is not None}")

def onResetButtonClick():
    global tmp
    global preview
    global searchEntry

    if (preview is not None):
        onInputfieldChange("","auto")
    searchEntry.delete(0,  customtkinter.END)

def onOkButtonClick():
    global preview
    global searchEntry
    if(preview is not None):
        tmp.replaceTmp(preview)
    #preview = None

    searchEntry.delete(0,  customtkinter.END)
    return

def onImport():
    filepath = customtkinter.filedialog.askopenfilename(filetypes=[("Minecraft DB-Datei", "*.mcdb")])
    if filepath:
        # Kopiere die ausgewählte Datei an den Speicherort von "test.db"
        shutil.copy(filepath, "minecraftDatabase.db")
    onTableButtonClick("Serverworld")

def onExport():
    filepath = customtkinter.filedialog.asksaveasfilename(defaultextension=".mcdb", filetypes=[("Minecraft DB-Datei", "*.mcdb")])
    if filepath:
        # Kopiere die Datei "test.db" an den von der Benutzer ausgewählten Speicherort
        shutil.copy("minecraftDatabase.db", filepath)
