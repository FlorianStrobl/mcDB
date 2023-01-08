import sqlite3
import threading
import shutil
import customtkinter
import time
import addImport
import Logger
from TmpData import *
import SQL

# TODO fix drawTableBody() for empty arrays
# TODO sql klappt net bei z.b. UPDATE mit dem draw()

tk = None

table = None
pageSystem = None

cursor = sqlite3.connect("minecraftDatabase.db").cursor()
tmp: TMP = TMP()
preview: TMP = (
    None  # the preview for tmp shall be drawn in the UI table IF it is not None
)
lastInputFieldChangeTime: int = (
    -1
)  # the last time the inputfield changed its value by the user

currentTableName = None
searchEntry = None
segemented_button_var = None

setButtonSelected = None

currentShowVar = None

showActivated = False
# originalData has the correct types for each row
# newDataThatNeedsToBeCasted has ONLY string types


checkbox = None


def castColumns2(tableName, columnNames, newDataThatNeedsToBeCasted):
    typesOfTables = {
        "Serverworld": {"serverworld_id": int, "name": str, "icon": str},
        "Player": {"player_id": int, "username": str, "skin": str},
        # same with others...
        "MEntities": {
            "m_entities_id": int,
            "entity_position": str,
            "birthday": int,
            "entity_type": int,
        },
        "Block": {"absolute_position": str, "block_type": int},
        "Wood": {"absolute_position": str, "isOnFire": int},
        "Dirt": {"absolute_position": str, "hasGrass": int},
        "plays": {
            "player_id": int,
            "serverworld_id": int,
            "session_begin:": int,
            "player_position": str,
            "role": str,
        },
        "populatedBy": {"m_entities_id": int, "serverworld_id": int},
        "buildOf": {"absolute_position": str, "serverworld_id": int},
    }

    tableTypes = typesOfTables[tableName]

    for i in range(len(newDataThatNeedsToBeCasted)):
        for j in range(len(newDataThatNeedsToBeCasted[i])):
            try:
                caster = None
                if columnNames[j] in tableTypes:
                    caster = tableTypes[columnNames[j]]

                if newDataThatNeedsToBeCasted[i][j] == "null" and (
                    columnNames[j] == "icon"
                ):
                    newDataThatNeedsToBeCasted[i][j] = None
                else:
                    if caster is not None:
                        newDataThatNeedsToBeCasted[i][j] = caster(
                            newDataThatNeedsToBeCasted[i][j]
                        )
                    else:
                        # no casting if the type unknown
                        newDataThatNeedsToBeCasted[i][j] = newDataThatNeedsToBeCasted[
                            i
                        ][j]
            except:
                Logger.Logger.error(
                    "Could not cast the following data to the correct type: '"
                    + str(newDataThatNeedsToBeCasted[i][j])
                    + "' at row "
                    + str(i)
                )
                return None

    return newDataThatNeedsToBeCasted


tableUpdadedBefore = False
lastQuery = ""

lastCheckBoxMode = 0


def previewFunc(delay=500, count=0):
    global searchEntry
    global segemented_button_var
    global lastQuery
    global currentShowVar
    global tableUpdadedBefore
    global currentTableName
    global showActivated
    global checkbox
    global lastCheckBoxMode

    query = searchEntry.get().strip()
    mode = segemented_button_var.get()

    # check if the preview mode is on
    if not checkbox.get():
        # The preview mode is off
        # Recall this function to check if preview modes changed
        tk.after(delay, lambda: previewFunc(delay, count + 1))


        if lastCheckBoxMode != checkbox.get():
            # Preview Mode was toggled from on to off
            # When not in preview mode you can edit the data
            pageSystem.setTableState(customtkinter.NORMAL)
            # tmp.setData(pageSystem.getInput())

            updateUI(tmp)
        elif(query != ""):
            # The preview is off BUT the user has written something

            pageSystem.setTableState(customtkinter.DISABLED)
        elif(query == ""):
            pageSystem.setTableState(customtkinter.NORMAL)
        lastCheckBoxMode = checkbox.get()
        return
    else:
        # preview mode is on
        if lastCheckBoxMode != checkbox.get():
            # preview mode was just toggeld
            # from off to on
            # so save UI data to TMP
            tmp.setData(castColumns2(currentTableName, tmp.columnNames, pageSystem.getInput().copy()))
            #print()
            updateUI(tmp)
            #print(castColumns2(currentTableName, tmp.columnNames, pageSystem.getInput().copy()))
        pageSystem.setTableState(customtkinter.DISABLED)

        lastCheckBoxMode = checkbox.get()




    # DIE NÄCHSTEN 3 ABSCHNITTE GEHEN NUR WENN

    # Wenn was für das erste mal im Input Field steht:
    if lastQuery.strip() == "" and query.strip() != "":
        # TODO
        # tmp.setData(castColumns(tmp.deepCpyData(),pageSystem.getInput().copy() ))
        tmp.setData(
            castColumns2(
                currentTableName, tmp.columnNames, pageSystem.getInput().copy()
            )
        )

        pageSystem.setTableState(customtkinter.DISABLED)
        updateUI(tmp)
        # Table in TMP saven

    # Wenn plötzlich letztlich alles gelöscht wird (z.B mit strg a delete ) dann wird der UP  geupdaded
    if lastQuery.strip() != "" and query.strip() == "":
        pageSystem.setTableState(customtkinter.DISABLED)
        updateUI(tmp)
        showActivated = False
        # tableUpdadedBefore = True

    # Wenn was im Input field steht:
    if query.strip() != "":
        # - Editierte Datenbank bekommen als "currentShowVar"
        showActivated = True
        currentShowVar = tmp.editData(query, mode, False)

        # -> Wenn "currentShowVar" None ist bzw. der Command Invalid ist dann:
        pageSystem.setTableState(customtkinter.DISABLED)
        if(lastQuery != query):
            #Only update UI when user field was changed
            if currentShowVar is None:
                # - Table resetten
                updateUI(tmp)
                #Mach das nur einmal
            # -> Wenn "currentShowVar" ein Array ist bzw nicht None ist:
            else:
                # - "val" anzeigen
                updateUI(currentShowVar.deepCpy())
                #Mach das nur einmal
                # - alle Buttons AUF DISABLED machen mit der pagesystem.setState Funktion

    # Wenn auf save geklickt wird:
    # TMP in DB speichern (wenn gleiche columns names wird backend als error gemeldet sonst)

    #print(pageSystem.getInput())

    lastQuery = query
    tk.after(delay, lambda: previewFunc(delay, count + 1))


def updateUI(data):
    data = data.deepCpy()

    pageSystem.changeTableBody(data.deepCpyData())
    #print(data.deepCpyData())
    table.setTableHeader(data.columnNames)


def onGuiReady2(
    _table,
    _pageSystem,
    _searchEntry,
    _setButtonSelected,
    _segemented_button_var,
    _tk,
    _checkbox,
):
    global table
    global pageSystem
    global searchEntry
    global setButtonSelected
    global segemented_button_var
    global tk
    global checkbox

    checkbox = _checkbox

    table = _table
    pageSystem = _pageSystem
    searchEntry = _searchEntry
    segemented_button_var = _segemented_button_var
    tk = _tk

    setButtonSelected = _setButtonSelected


    onTableButtonClick("Serverworld")

    previewFunc()


def onTableButtonClick(tableName):
    global table
    global pageSystem
    global cursor
    global currentTableName
    global setButtonSelected
    # names = list(cursor.description)
    table.scrollFrame.canvas.yview_moveto(0)
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

    #print(tmp.getData())
    pageSystem.changeTableBody(tmp.getData().copy())
    table.setTableHeader(columnNames)

    currentTableName = tableName
    # pageSystem.changeTableBody([[i,"j","l","l","l"] for i in range(100)])

    setButtonSelected(tableName)




def onOkButtonClick():
    global searchEntry
    global segemented_button_var
    global tmp

    if searchEntry.get().strip() == "":
        return

    if segemented_button_var.get() == "sql":
        # TODO
        sqlQuery = searchEntry.get()
        Logger.Logger.log(
            "SQL Querys will be applied immediately. This means that you can not undo them if they change something in the database."
        )
        try:
            cursor.execute(sqlQuery)
            cursor.connection.commit()
        except:
            Logger.Logger.error("Could not execute the following query:", sqlQuery)
            return

        resultData = cursor.fetchall()
        columnNames = list(map(lambda x: x[0], cursor.description))

        # edit tmp data
        # do not update tmp.tableName itself
        tmp.data = resultData
        tmp.columnNames = columnNames
    else:
        t = tmp.editData(searchEntry.get(), segemented_button_var.get(), True)
        if t is None:
            Logger.Logger.error("could not execute the command!")
            return
        tmp.replaceTmp(t)

    # clear the entry field
    searchEntry.delete(0, customtkinter.END)

    # reload UI with new tmp
    updateUI(tmp)

    return

    # global preview
    # global searchEntry
    if preview is not None:
        tmp.replaceTmp(preview)
    # preview = None

    searchEntry.delete(0, customtkinter.END)
    return


def onTableSave(table):
    global pageSystem
    global currentTableName
    global cursor
    global tmp
    global showActivated
    # TODO, No! because if there is a preview
    # which was NOT confirmed by the "Ok" button
    # you may not want to save it/apply the changes
    # BUT what to do if there is a preview and then
    # the user changes a field of the previews
    # saving the preview and replacing TMP then?

    # tmp.setData(pageSystem.getInput())
    # tmp.tableName = currentTableName

    # wenn

    if not showActivated:
        x = castColumns2(currentTableName, tmp.columnNames, pageSystem.getInput())
        if x != None:
            tmp.setData(x)
        else:
            # Return if invalid data in UI
            return
    updateDataInDB(cursor, tmp)
    # update UI to the current DB to avoid any bugs
    onInputfieldChange("", "auto")
    updateUI(tmp)


# this is only for the preview mode
def onInputfieldChange(text, mode):
    # do not need this lol
    return

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
    if preview is None:
        tmp.setData(pageSystem.getInput())

    # TODO delay bugs
    global lastInputFieldChangeTime
    curTime = round(time.time() * 1000)
    delay = 1000  # 1s

    # if tmp.editData(text, mode) is None and lastInputFieldChangeTime + delay > curTime:
    #     # but what if tmp.editData(text, mode) STAYS None
    #     # because if there was a preview before that set
    #     # this preview is not the one from the inputfield anymore
    #     # this means preview has to be set to None and TMP needs to be reshown again

    #     #threading.Timer(1000, do()) # text errored anyway, so do not show preview anymore but TMP
    #     return
    # else:
    #     lastInputFieldChangeTime = curTime
    #     # continue execution

    if mode == "sql":
        # do the sql cmd and show the result
        if text.strip() == "":
            preview = None
        if preview is not None:
            Logger.Logger.warn(
                "UNSAVED preview mode, click the 'Ok' Button to apply changes"
            )
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
            # return
        return

    if text.strip() == "":
        preview = None
        return

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
        Logger.Logger.warn(
            "UNSAVED preview mode, click the 'Ok' Button to apply changes"
        )
        pageSystem.changeTableBody(preview.deepCpyData())
        table.setTableHeader(preview.columnNames)
    else:
        # TODO remove the "preview mode" text described above
        Logger.Logger.warn("")
        pageSystem.changeTableBody(tmp.deepCpyData())
        table.setTableHeader(tmp.columnNames)


def onResetButtonClick():
    global tmp
    global preview
    global searchEntry

    if preview is not None:
        onInputfieldChange("", "auto")
    searchEntry.delete(0, customtkinter.END)


def onImport():
    filepath = customtkinter.filedialog.askopenfilename(
        filetypes=[
            ("Minecraft DB-Datei", "*.mcdb"),
            ("Default DB-Datei", "*.db"),
            ("Anderer Datentyp", "*.*"),
        ]
    )
    if filepath:
        # Kopiere die ausgewählte Datei an den Speicherort von "test.db"
        shutil.copy(filepath, "minecraftDatabase.db")
    onTableButtonClick("Serverworld")


def onExport():
    filepath = customtkinter.filedialog.asksaveasfilename(
        defaultextension=".mcdb",
        filetypes=[
            ("Minecraft DB-Datei", "*.mcdb"),
            ("Default DB-Datei", "*.db"),
            ("Anderer Datentyp", "*.*"),
        ],
    )
    if filepath:
        # Kopiere die Datei "test.db" an den von der Benutzer ausgewählten Speicherort
        shutil.copy("minecraftDatabase.db", filepath)
