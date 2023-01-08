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
currentColumnNames = None

searchEntry = None
segemented_button_var = None

setButtonSelected = None

currentShowVar = None

showActivated = False
# originalData has the correct types for each row
# newDataThatNeedsToBeCasted has ONLY string types


checkbox = None


def castColumns(tableName, columnNames, newDataThatNeedsToBeCasted):
    typesOfColumns = {
        "serverworld_id": int,
        "name": str,
        "icon": str,
        "player_id": int,
        "username": str,
        "skin": str,
        # same with others...
        "m_entities_id": int,
        "entity_position": str,
        "birthday": int,
        "entity_type": int,
        "block_type": int,
        "absolute_position": str,
        "isOnFire": int,
        "hasGrass": int,
        "session_begin:": int,
        "player_position": str,
        "role": str,
    }

    for i in range(len(newDataThatNeedsToBeCasted)):
        for j in range(len(newDataThatNeedsToBeCasted[i])):
            caster = None
            try:
                if columnNames[j] in typesOfColumns:
                    caster = typesOfColumns[columnNames[j]]

                if newDataThatNeedsToBeCasted[i][j] == "null" and (
                    columnNames[j] == "icon"
                ):
                    newDataThatNeedsToBeCasted[i][j] = None
                else:
                    if caster is not None:
                        try:
                            newDataThatNeedsToBeCasted[i][j] = caster(
                                newDataThatNeedsToBeCasted[i][j]
                            )
                        except:
                            print("strange stuff")
                            return None # TODO really???
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
                    + str(i),
                    type(newDataThatNeedsToBeCasted[i][j]),
                    caster,
                )
                return None

    return newDataThatNeedsToBeCasted


tableUpdadedBefore = False
lastQuery = ""
justSwitchedTable = False

lastCheckBoxMode = 0
lastMode = "auto"


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
    global justSwitchedTable
    global lastMode

    query = searchEntry.get().strip()
    mode = segemented_button_var.get()

    if lastMode != "sql" and mode == "sql":
        Logger.Logger.warn(
            "Der Preview modus funktionniert nicht mit SQL Eingaben. \nWenn der OK Button gedrückt wird, der save button automatisch mitgedrückt"
        )

    # check if the preview mode is on
    if not checkbox.get():
        # The preview mode is off
        if lastCheckBoxMode != checkbox.get():
            tmp.setData(
                castColumns(
                    currentTableName, tmp.columnNames, pageSystem.getInput().copy()
                ),
                currentColumnNames,
            )
            # Preview Mode was toggled from on to off
            # When not in preview mode you can edit the data
            pageSystem.setTableState(customtkinter.NORMAL)

            updateUI(
                tmp
            )  # TODO doesnt work as intended: its like it was really updated by just the preview code
        elif query != "":
            # The preview is off BUT the user has written something
            pageSystem.setTableState(customtkinter.DISABLED)
        elif query == "":
            pageSystem.setTableState(customtkinter.NORMAL)

        lastCheckBoxMode = checkbox.get()
        lastMode = mode
        lastQuery = query
        # Recall this function to check if preview modes changed
        tk.after(delay, lambda: previewFunc(delay, count + 1))
        return
    else:
        # preview mode is on
        if lastCheckBoxMode != checkbox.get() or lastMode != mode:
            # preview mode was just toggeld from off to on
            # so save UI data to TMP
            if lastMode == mode:
                tmp.setData(
                    castColumns(
                        currentTableName, tmp.columnNames, pageSystem.getInput().copy()
                    ),
                    currentColumnNames,
                )
            previewTmp = tmp.editData(query, mode, False)
            if previewTmp is not None:
                updateUI(previewTmp)
            else:
                updateUI(tmp)
        pageSystem.setTableState(customtkinter.DISABLED)

    # Wenn was für das erste mal im Input Field steht:
    # wir sind im preview mode
    if lastQuery.strip() == "" and query.strip() != "":
        # TODO
        # we know the preview mode is on
        if not justSwitchedTable:
            tmp.setData(
                castColumns(
                    currentTableName, tmp.columnNames, pageSystem.getInput().copy()
                ),
                currentColumnNames,
            )
        justSwitchedTable = False

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

        if lastQuery != query:
            # Only update UI when user field was changed
            if currentShowVar is None:
                # - Table resetten
                updateUI(tmp)
                # Mach das nur einmal
            # -> Wenn "currentShowVar" ein Array ist bzw nicht None ist:
            else:
                # - "val" anzeigen
                updateUI(currentShowVar.deepCpy())
                # Mach das nur einmal
                # - alle Buttons AUF DISABLED machen mit der pagesystem.setState Funktion

    # Wenn auf save geklickt wird:
    # TMP in DB speichern (wenn gleiche columns names wird backend als error gemeldet sonst)

    lastQuery = query
    lastMode = mode
    lastCheckBoxMode = checkbox.get()
    # recall itself in a loop
    tk.after(delay, lambda: previewFunc(delay, count + 1))


def updateUI(data):
    global currentColumnNames
    currentColumnNames = data.columnNames
    data = data.deepCpy()
    pageSystem.changeTableBody(data.deepCpyData())
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
    global lastQuery
    global justSwitchedTable
    global currentColumnNames
    lastQuery = ""  # TODO will error if you toggle preview mode with already a query in the search field
    justSwitchedTable = True
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
    currentColumnNames = tmp.columnNames
    updateUI(tmp)

    currentTableName = tableName
    # pageSystem.changeTableBody([[i,"j","l","l","l"] for i in range(100)])

    setButtonSelected(tableName)


def onOkButtonClick():
    global searchEntry
    global segemented_button_var
    global tmp
    global currentTableName
    global cursor
    global currentColumnNames

    if searchEntry.get().strip() == "":
        return

    if segemented_button_var.get() == "sql":
        # TODO
        tmp.setData(
            castColumns(
                currentTableName, currentColumnNames, pageSystem.getInput().copy()
            ),
            currentColumnNames,
        )
        # Das SQL nicht auf tmp läuft, muss erst die DB geupdated werden
        updateDataInDB(cursor, tmp)
        sqlQuery = searchEntry.get().strip()
        # Logger.Logger.log(
        #     "SQL Querys will be applied immediately. This means that you can not undo them if they change something in the database."
        # )
        try:
            cursor.execute(sqlQuery)
            cursor.connection.commit()
        except:
            Logger.Logger.error("Could not execute the following query:", sqlQuery)
            return

        resultData = cursor.fetchall()
        if cursor.description is None:
            onTableButtonClick(currentTableName)
        else:
            columnNames = list(map(lambda x: x[0], cursor.description))

            # edit tmp data
            # do not update tmp.tableName itself
            tmp.data = resultData
            currentColumnNames = columnNames
            tmp.columnNames = columnNames
    else:
        t = tmp.editData(searchEntry.get(), segemented_button_var.get(), True)

        if t is None:
            Logger.Logger.error("could not execute the command!")
            return
        currentColumnNames = t.columnNames
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
    global searchEntry
    global checkbox
    # TODO, No! because if there is a preview
    # which was NOT confirmed by the "Ok" button
    # you may not want to save it/apply the changes
    # BUT what to do if there is a preview and then
    # the user changes a field of the previews
    # saving the preview and replacing TMP then?
    query = searchEntry.get().strip()
    # wenn

    # when the preview mode is not activated
    if query != "" or checkbox.get():
        Logger.Logger.warn("You are saving without the preview applied")

    if not showActivated:
        # Preview mode is off
        x = castColumns(currentTableName, tmp.columnNames, pageSystem.getInput())
        if x != None:
            tmp.setData(x, currentColumnNames)
        else:
            # UI data could not be casted => invalid data in gui
            # Return if invalid data in UI
            # TODO, no error message??
            Logger.Logger.error("Invalid data in UI")
            return
    updateDataInDB(cursor, tmp)
    onTableButtonClick(currentTableName)
    Logger.Logger.log("Saved changes to database")
    # update UI to the current DB to avoid any bugs
    # updateUI(tmp)


# this is only for the preview mode
def onInputfieldChange(text, mode):
    # do not need this lol
    return


def onResetButtonClick():
    global tmp
    global preview
    global searchEntry

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


def fillAllDataRand():
    global currentTableName

    dataNumber = customtkinter.CTkInputDialog(
        text="Wie viele Datensätze willst du pro Tabelle random generieren lassen?",
        title="Minecraft Database ",
    )
    result = 0
    try:
        result = int(dataNumber.get_input())
        if result < 0:
            Logger.Logger.error("Du hast keine negative zahlen eingegeben!")
            return
    except:
        Logger.Logger.error("Du hast keine valide zahl eingegeben!")
        return
    SQL.dropAllTables(cursor)  # reset the current db
    SQL.createAllTables(cursor)  # create all tables
    SQL.fillAllTablesRand(cursor, result)

    onTableButtonClick(currentTableName)


def deleteAllData():
    global currentTableName
    SQL.dropAllTables(cursor)  # reset the current db
    SQL.createAllTables(cursor)  # create all tables

    onTableButtonClick(currentTableName)


def loadDefaultValues():
    global currentTableName
    shutil.copy("defaultDatabase.db", "minecraftDatabase.db")
    onTableButtonClick(currentTableName)
