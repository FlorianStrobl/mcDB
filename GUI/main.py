import tkinter
import customtkinter
import random
import time
import addImport
from scrollableTable import scrollableTable
from interface import *
from pagesSystem import *


xStart = 127
logLabel = None
table = None
navigatorIndicator = None
tableButtons = []

tableNamesButtons = []
buttonNames = [
    "Serverworld",
    "Player",
    "MEntities",
    "Block",
    "Wood",
    "Dirt",
    "plays",
    "populatedBy",
    "buildOf",
]
currentSelectedButtonId = None

arrow = None

def setArrowToPos(heightIndex):
    arrow.place(x=10, y=14 + heightIndex * 35)
    # start 14 difference de 34

# Setzet einen bestimmten button auf "selected" (also der button bekommt (als einziger) eine dunkelblaue Farbe )
# --> Pfeil wird auch auf "button" name verschoben
def setButtonSelected(buttonName):
    # Reset Old button

    global currentSelectedButtonId
    global tableNamesButtons
    global buttonNames
    if currentSelectedButtonId is not None:
        tableNamesButtons[currentSelectedButtonId].configure(
            fg_color="#343638", bg_color="#302c2c"
        )
    # Update Current Button Variable
    currentSelectedButtonId = buttonNames.index(buttonName)
    tableNamesButtons[currentSelectedButtonId].configure(
        fg_color=["#325882", "#14375e"]
    )

    setArrowToPos(currentSelectedButtonId)

# Erstellt einen Hilfe Popup und erklärt den aktuellen Modus der an ist
def createHelperPopup():
    # bei mode == "auto", join() alle Messages mit \n\n und jeweils welcher Befehl das ist
    helpMessagesLanguage = {
        "sql": "Voller SQLite3 Support",
        "columns": "Zeige nur die Spalten der aktuellen Tabelle an die angegeben werden mit folgender Syntax:\ncolumnName1, columnName2, ..., columnNameN\nBeispiel-Code für Tabelle Serverworld: `serverworld_id, icon`",
        "slice": "Slice die aktuellen Daten wie bei einem Python slice arr[idx1:idx2] mit folgender Syntax:\nslice n; m\n'n' und 'm' sind hierbei Python expressions und Sie haben eine 'data' Variable die alle aktuellen Daten aus dem UI gespeichert hat, eine 'length' Variable die die Länge von 'data' speichert, und Sie haben zugriff auf folgende Python Bibliotheken: ['random', 'math', 'numpy', 'time']\nBeispiel-Code: `slice 0; length`\n\nTLDR: 'slice n; m', mit n, m als PythonExpressions mit folgenden Variablen: ['data', 'length', 'random', 'math', 'numpy', 'time']",
        "filter": "Beim filtern wird der eingegebene String für alle Zeilen als Python expression ausgewertet und wenn die Expression True returnt, so wird diese Zeile behalten. Ansonsten wird diese heraus gefiltert.\nDie Namen der aktuellen Spalten in der DB sind Variablen die Sie nutzen können. Desweiteren speichert die 'data' Variable alle aktuellen Daten der DB als Liste und die 'length' Variable speichert die Länge dieser. Mit der 'index' Variable, ist der Index der aktuell zu filternden Zeile gespeichert. Sie haben zugriff auf folgende Python Bibliotheken: ['random', 'math', 'numpy', 'time']\nBeispiel-Code für die Tabelle Serverworld: `icon != None`\n\nTLDR: 'PythonExpressionWhichEvaluatesToBoolean', mit folgenden Variablen: [currentColumns, 'data', 'length', 'index', 'random', 'math', 'numpy', 'time']",
        "map": "Beim mappen werden die Werte jeder Zeilen mithilfe einer Python expression bearbeitet. Dabei nutzt man eine der folgenden Syntaxen:\ncolumnName <- PythonExpression\n(columnName1, columnName2, ..., columnNameN) <- PythonExpression\nBei der Python expression sind die aktuellen Spaltennamen in der DB als Variablen verwendbar. Die aktuellen Daten der DB sind mit der 'data' Variable als Liste gespeichert und 'length' speichert die Länge dieser. Mit der 'index' Variable, ist der Index der aktuell zu bearbeitende Zeile gespeichert. Sie haben zugriff auf folgende Python Bibliotheken: ['random', 'math', 'numpy', 'time']\nBeispiel-Code für die Tabelle Serverworld: `(icon, name) <- (icon if icon is not None else \"The icon is not set for this row.\", name + \"s\")`\n\nTLDR: 'columnName <- PythonExpression' oder 'columnName <- PythonExpression\n(columnName1, columnName2, ..., columnNameN) <- PythonExpression', mit folgenden Variablen: [currentColumns, 'data', 'length', 'index', 'random', 'math', 'numpy', 'time']",
        "sort": "Die Daten der DB werden mithilfe von einem Stable-Quicksort sortiert. Sie geben mit einer Python expression die Komparator Funktion an, welche zwei verschiedenen Zeilen vergleicht und ein Integer returniert. Falls beide Zeilen gleichwertig sind soll 0 returniert werden, <0 wird returniert falls getauscht werden muss und >0 falls es bereits die richtige Reihenfolge hat. Die Spaltennamen der aktuellen DB sind als Variablen verwendbar, mit der Besonderheit, dass am Ende der Identifier eine '1' oder eine '2' steht, die die erste bzw. zweite Zeile die gerade verglichen werden angiebt. 'index1' und 'index2' sind verwendbare Variablen die die Zeilen Nummer der beiden Zeilen speichern. Die 'data' Variable hat alle aktuellen Daten in der DB gespeichert und die 'length' Variable die Länge dieser Liste. Sie haben zugriff auf folgende Python Bibliotheken: ['random', 'math', 'numpy', 'time']\nBeispiel-Code für die Tabelle Serverworld: `serverworld_id1 - serverworld_id2`\n\nTLDR: 'PythonExpressionWhichReturnsInt', mit folgenden Variablen: [currentColumns1, currentColumns2, 'index1', 'index2', 'data', 'length', 'random', 'math', 'numpy', 'time']",
    }

    global segemented_button_var
    mode = str(segemented_button_var.get())

    window = customtkinter.CTkToplevel()
    window.geometry("500x400")
    window.title("User Manual📖 | mode:" + mode)

    title = customtkinter.CTkLabel(
        window, text="Erklärung von " + mode + ":", font=("Helvetica bold", 20)
    )
    title.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

    textbox = customtkinter.CTkTextbox(window)
    textbox.place(relx=0.05, rely=0.22, relwidth=0.9, relheight=0.7)
    # textbox.insert("0.0", "new text to insert\ntest"*600)
    result = ""
    if mode == "auto":
        result = "Der Auto Befehl kann automatisch herausfinden, welchen Modus er anwenden soll. Mit && können Sie desweiteren mehrere Befehle hintereinander ausführen"
        result += "\n\nErklärung von columns:\n\n"
        result += helpMessagesLanguage["columns"]

        result += "\n\nErklärung von slice:\n\n"
        result += helpMessagesLanguage["slice"]

        result += "\n\nErklärung von filter:\n\n"
        result += helpMessagesLanguage["filter"]

        result += "\n\nErklärung von map:\n\n"
        result += helpMessagesLanguage["map"]

        result += "\n\nErklärung von sort:\n\n"
        result += helpMessagesLanguage["sort"]
    else:
        result = helpMessagesLanguage[mode]

    textbox.insert("0.0", result)
    textbox.configure(state="disabled")
    # label = customtkinter.CTkLabel(window, text=helpMessagesLanguage[mode],font=('Helvetica bold', 15))
    # label.place(relx=0.05, rely=0.25)

# Lädt die ganze GUI und erstellt die ganzen Widgets
def loadGUI():
    global logsLabel
    global table
    global navigatorIndicator
    global tableButtons
    global tableNamesButtons
    global setButtonSelected
    global arrow
    global segemented_button_var

    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry("800x500")
    app.title("Minecraft Datenbank")
    titleFrame = customtkinter.CTkFrame(master=app, corner_radius=7)
    titleFrame.place(x=20, y=20, width=200, height=75)

    exportButton = customtkinter.CTkButton(
        master=titleFrame,
        text="export",
        command=onExport,
        fg_color=["#3a7ebf", "#1f538d"],
    )
    exportButton.place(x=10, y=40, width=90)
    exportButton.configure(fg_color="#343638", bg_color="#302c2c")

    importButton = customtkinter.CTkButton(
        master=titleFrame,
        text="import",
        command=onImport,
        fg_color=["#3a7ebf", "#1f538d"],
    )
    importButton.place(x=105, y=40, width=90)
    importButton.configure(fg_color="#343638", bg_color="#302c2c", command=onImport)

    emptyButton = customtkinter.CTkButton(
        master=app,
        text="db leeren",
        fg_color=["#3a7ebf", "#1f538d"],
        command=deleteAllData,
    )
    emptyButton.place(x=20, y=459, width=100)
    emptyButton.configure(fg_color="#343638", bg_color="#282424")

    fillRand = customtkinter.CTkButton(
        master=app,
        text="zufällig füllen",
        fg_color=["#3a7ebf", "#1f538d"],
        command=fillAllDataRand,
    )
    fillRand.place(x=127, y=459, width=120)
    fillRand.configure(fg_color="#343638", bg_color="#282424")

    loadDefault = customtkinter.CTkButton(
        master=app,
        text="standartwerde laden",
        fg_color=["#3a7ebf", "#1f538d"],
        command=loadDefaultValues,
    )
    loadDefault.place(x=254, y=459, width=130)
    loadDefault.configure(fg_color="#343638", bg_color="#282424")

    helpDefault = customtkinter.CTkButton(
        master=app,
        text="hilfe zu dem modus",
        fg_color=["#3a7ebf", "#1f538d"],
        command=createHelperPopup,
    )
    helpDefault.place(x=392, y=459, width=130)
    helpDefault.configure(fg_color="#343638", bg_color="#282424")

    label = customtkinter.CTkLabel(master=titleFrame, text="Minecraft Database")
    label.place(x=40, y=5)

    navigateBackground = customtkinter.CTkFrame(
        master=app, width=200, height=333, corner_radius=5
    )
    navigateBackground.place(x=20, y=115)

    arrow = customtkinter.CTkLabel(master=navigateBackground, text="➜")
    arrow.place(x=10, y=48)

    tablesNames = {
        "Serverworld": lambda: onTableButtonClick("Serverworld"),
        "Player": lambda: onTableButtonClick("Player"),
        "MEntities": lambda: onTableButtonClick("MEntities"),
        "Block": lambda: onTableButtonClick("Block"),
        "Wood": lambda: onTableButtonClick("Wood"),
        "Dirt": lambda: onTableButtonClick("Dirt"),
        "plays": lambda: onTableButtonClick("plays"),
        "populatedBy": lambda: onTableButtonClick("populatedBy"),
        "buildOf": lambda: onTableButtonClick("buildOf"),
    }
    tableNamesButtons = []

    def placeTableButton(title, event):
        global xStart
        myButton = customtkinter.CTkButton(master=app, text=title, command=event)
        myButton.place(x=55, y=xStart)
        myButton.configure(fg_color="#343638", bg_color="#302c2c")
        tableNamesButtons.append(myButton)

        xStart += 35

    def spawnTableButtons():
        for name in tablesNames.keys():
            tableButtons.append(placeTableButton(name, tablesNames[name]))

    spawnTableButtons()

    table = scrollableTable(
        app,
        tableData=[[""], []],
        pos=(235, 145, 515, 300),
    )

    searchFrame = customtkinter.CTkFrame(master=app, corner_radius=7)
    searchFrame.place(x=235, y=20, width=515, height=75)

    checkbox = customtkinter.CTkCheckBox(
        master=searchFrame,
        text="preview aktiviert",
        checkbox_width=20,
        checkbox_height=20,
    )
    checkbox.place(x=14, y=3)

    segemented_button_var = customtkinter.StringVar(value="auto")
    segemented_button = customtkinter.CTkSegmentedButton(
        master=app,
        values=["sql", "auto", "columns", "slice", "filter", "sort", "map"],
        variable=segemented_button_var,
    )
    segemented_button.place(x=400, y=10, width=300)

    searchEntryStringVar = customtkinter.StringVar()
    searchEntryStringVar.trace(
        "w",
        lambda name, index, mode, sv=searchEntryStringVar: onInputfieldChange(
            sv.get(), segemented_button_var.get()
        ),
    )
    searchEntry = customtkinter.CTkEntry(
        master=searchFrame,
        placeholder_text="Gebe deine Funktion ein",
        textvariable=searchEntryStringVar,
    )
    searchEntry.place(x=50, y=30, width=400, height=35)

    previewButton = customtkinter.CTkButton(
        master=searchFrame, text="⟳", fg_color="#343638", command=onResetButtonClick
    )
    previewButton.place(x=10, y=30, width=30, height=33)

    okButton = customtkinter.CTkButton(
        master=searchFrame, text="Ok", fg_color="#343638", command=onOkButtonClick
    )
    okButton.place(x=460, y=30, width=30, height=33)

    SaveButton = customtkinter.CTkButton(
        master=app,
        text="✓ Save",
        fg_color="#343638",
        bg_color="#282424",
        command=lambda: onTableSave(table),
        corner_radius=7,
    )
    SaveButton.place(x=680, y=457, width=70, height=33)

    navigatorFrame = customtkinter.CTkFrame(
        master=app,
        corner_radius=7,
        fg_color="#343638",
    )
    navigatorFrame.place(x=530, y=458, width=135, height=30)

    navigatorIndicator = customtkinter.CTkLabel(
        master=navigatorFrame, bg_color="#343638", text="17/23", corner_radius=7
    )
    navigatorIndicator.place(x=45, y=0, width=50, height=30)

    pageSystem = PageSystem(table, navigatorIndicator, [[i] for i in range(0)])
    table.setTableHeader([""])

    navigatorNavLeft = customtkinter.CTkButton(
        master=navigatorFrame,
        text="<",
        fg_color="#343638",
        command=lambda: pageSystem.onNavigateButtonClick(2)
    )
    navigatorNavLeft.place(x=25, y=2, width=20, height=25)
    navigatorNavLeftEnd = customtkinter.CTkButton(
        master=navigatorFrame,
        text="<<",
        fg_color="#343638",
        font=("Helvetica", 11),
        command=lambda: pageSystem.onNavigateButtonClick(1)
    )
    navigatorNavLeftEnd.place(x=5, y=2, width=23, height=25)

    navigatorNavRight = customtkinter.CTkButton(
        master=navigatorFrame,
        text=">",
        fg_color="#343638",
        command=lambda: pageSystem.onNavigateButtonClick(3)
    )
    navigatorNavRight.place(x=90, y=2, width=20, height=25)
    navigatorNavRightEnd = customtkinter.CTkButton(
        master=navigatorFrame,
        text=">>",
        fg_color="#343638",
        font=("Helvetica", 11),
        command=lambda: pageSystem.onNavigateButtonClick(4)
    )
    navigatorNavRightEnd.place(x=110, y=2, width=23, height=25)

    pageSystem.onUIReady()
    onGuiReady2(
        table,
        pageSystem,
        searchEntry,
        setButtonSelected,
        segemented_button_var,
        app,
        checkbox,
    )

    app.mainloop()
