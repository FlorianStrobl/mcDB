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

# preview mode
showActivated = False
# originalData has the correct types for each row
# newDataThatNeedsToBeCasted has ONLY string types


checkbox = None


def castColumns(columnNames, newDataThatNeedsToBeCasted):
    typesOfColumns = {
        "serverworld_id": int,
        "name": str,
        "icon": str,
        "player_id": int,
        "username": str,
        "skin": str,
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
                # if newDataThatNeedsToBeCasted[i][j].strip().lower() == "null":
                # print("got a UI none", columnNames[j])
                if newDataThatNeedsToBeCasted[i][j] == "null" and (
                    columnNames[j] == "icon"
                ):
                    # print("and correct column!")
                    newDataThatNeedsToBeCasted[i][j] = None
                else:
                    if caster is not None:
                        try:
                            newDataThatNeedsToBeCasted[i][j] = caster(
                                newDataThatNeedsToBeCasted[i][j]
                            )
                        except:
                            print(
                                f"strange stuff '{caster}', '{newDataThatNeedsToBeCasted[i][j]}', '{columnNames}'"
                            )
                            # return None # TODO really???
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
                # return None

    return newDataThatNeedsToBeCasted


lastQuery = ""
justSwitchedTable = False

lastCheckBoxMode = 0
lastMode = "auto"


def previewFunc(delay=500, count=0):
    # the user input
    global searchEntry
    global lastQuery

    # the current mode [auto, filter, ...]
    global segemented_button_var
    global lastMode

    # what is currently shown at the screen
    global currentShowVar

    # the currently drawn (or at least was drawn) table
    global currentTableName
    # the CURRENTLY drawn column names which dont have to be the one in TMP
    global currentColumnNames

    # the preview mode toggle
    global checkbox
    global lastCheckBoxMode
    # shows also if preview mode is activated
    global showActivated

    # if the currentTableName swiched or was reclicked
    global justSwitchedTable

    userQuery = searchEntry.get().strip()
    mode = segemented_button_var.get()
    previewMode = checkbox.get()
    lastPreviewMode = lastCheckBoxMode

    def runAQueryOrNot(query):
        if query == "" or mode == "sql":
            # maybe the query is now empty but maybe wasnt before
            # so reset the UI to TMP
            updateUI(tmp)
            return

        # execute the user query on tmp and save it in a temporary preview var
        previewTmp = tmp.editData(userQuery, mode, False)

        if previewTmp is None:
            # the user input is invalid
            # show the current state then
            updateUI(tmp)
        else:
            # the user input is valid, show the preview
            updateUI(previewTmp)

    # possible reasons the code has to be callen:
    # - preview mode was toggled
    # - user changed the query
    # - user changed the mode
    # - user switched to another table (or the same one)

    if lastMode != "sql" and mode == "sql":
        Logger.Logger.warn(
            "Der Preview modus funktionniert nicht mit SQL Eingaben.\nWenn der OK Button gedrückt wird, wird der save-Button automatisch mitgedrückt"
        )

    if userQuery != "" and lastQuery == "":
        # the user just wrote something in the query field
        # so make sure that all the change by bin-button and co are saved in tmp
        tmp.setData(
            castColumns(
                currentColumnNames, pageSystem.getInput().copy()
            ),
            currentColumnNames,
        )
        updateUI(tmp)

    if not previewMode:
        # the preview mode is disabled

        # - the switching from one mode to another does not matter to a disabled preview
        # - the switching from one table to another does not matter to a disabled preview

        justSwitchedTable = False  # we finished the complete switch by not applying the query since we dont want that

        # save performance by just reset the UI after a toggle
        if lastPreviewMode != previewMode:
            # the preview mode was toggled
            updateUI(tmp)  # reset UI back to normal

        if userQuery == "":
            # if the user has no query (and the preview mode is off) then activate the buttons (like bin and add button)
            pageSystem.setTableState(customtkinter.NORMAL)
        else:
            # the preview mode is not active
            # but the user has written something so disable the UI
            pageSystem.setTableState(customtkinter.DISABLED)

    elif previewMode:
        # the preview mode is enabled

        # if the preview mode is enabled
        # NEVER allow any buttons like trash and add
        pageSystem.setTableState(customtkinter.DISABLED)

        # check if preview mode was toggled
        if lastPreviewMode != previewMode:
            # the preview mode was toggled

            # save the UI to tmp because of
            # bin button, add button etc
            tmp.setData(
                castColumns(
                    currentColumnNames, pageSystem.getInput().copy()
                ),
                currentColumnNames,
            )

            # since the query itself has not changed but we are now in active mode, we need to rerun the query and update the UI accordingly
            runAQueryOrNot(userQuery)

        # check if the query has changed
        if lastQuery != userQuery:
            # the user query has changed
            runAQueryOrNot(userQuery)

        if lastMode != mode:
            # the mode has changed, so rerun the query
            runAQueryOrNot(userQuery)

        if justSwitchedTable:
            # the user switched to another table
            runAQueryOrNot(userQuery)
            justSwitchedTable = (
                False  # we finished the complete switch by just applying the query
            )

    lastCheckBoxMode = previewMode
    lastQuery = userQuery
    lastMode = mode

    tk.after(delay, lambda: previewFunc(delay, count + 1))


def updateUI(data):
    global currentColumnNames

    data = data.deepCpy()

    currentColumnNames = data.columnNames
    table.setTableHeader(data.columnNames)
    pageSystem.changeTableBody(data.deepCpyData())


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
        # TODO what if the user query was invalid, then we tried to save something without it even beging valid
        # TODO no need to save since if something was written in the search entry, it had to be saved before that since all the buttons are disabled else
        # tmp.setData(
        #     castColumns(
        #         currentColumnNames, pageSystem.getInput().copy()
        #     ),
        #     currentColumnNames,
        # )
        # Da SQL nicht auf tmp läuft, muss erst die DB geupdated werden
        print("need to update the DB now")
        # TODO error, what if this is the second select * from other table, then the tables will be wrong anyways
        # TODO hacky, it just does not show if an error happens and recovers from it
        updateDataInDB(cursor, tmp, False)
        sqlQuery = searchEntry.get().strip()
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
        # TODO
        x = castColumns(tmp.columnNames, pageSystem.getInput())
        if x != None:
            tmp.setData(x, currentColumnNames)
        else:
            # UI data could not be casted => invalid data in gui
            # Return if invalid data in UI
            # TODO, no error message??
            Logger.Logger.error("Invalid data in UI")
            return
    ans = updateDataInDB(cursor, tmp)
    if ans == False:
        Logger.Logger.error(
            "Could not save change to database so reverted to last valid values"
        )
    else:
        Logger.Logger.log("Saved changes to database")
        onTableButtonClick(currentTableName)
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
