import tkinter
import customtkinter
from scrollableTable import scrollableTable
from interface import *
from pagesSystem import *
import random
import time


xStart = 127
logLabel = None
table = None
navigatorIndicator = None



def setLogLabel(logText, color):
    logsLabel.configure(text=logText, text_color=color)

def loadGUI():
    global logsLabel
    global table
    global navigatorIndicator

    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry("800x500")

    navigateBackground = customtkinter.CTkFrame(
        master=app, width=200, height=333, corner_radius=5
    )
    navigateBackground.place(x=20, y=115)
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


    def placeTableButton(title, event):
        global xStart
        customtkinter.CTkButton(
            master=app, text=title, command=event, fg_color="#343638"
        ).place(x=45, y=xStart)

        xStart += 35


    def spawnTableButtons():
        for name in tablesNames.keys():
            placeTableButton(name, tablesNames[name])


    spawnTableButtons()


    table = scrollableTable(
        app,
        tableData=[
            ["Welt", "tsdsddds"],
            [[random.randint(0, 50), "t"] for i in range(100)],
        ],
        pos=(235, 145, 515, 300)
    )
    table.setTableHeader([random.randint(0, 1000), "t", "j", "j","x"])

    #table.fill([[random.randint(0, 1000), "t", "j", "j", "j"] for i in range(50)])

    #table.pagesFillInit([[i, "t", "j", "j", "j"] for i in range(160)])
    #table.showPage(0)

    #print(
    #    "textfill was "
    #    + table.textFill([[random.randint(0, 100), "x", "x", "x", "x"] for i in range(20)])
    #)
    # table.appendEmptyRowOnTop()

    # print(table.tableData)

    # button = customtkinter.CTkButton(master=app,text="+",command=table.appendEmptyRowOnTop,  corner_radius=0,fg_color="#343638")
    # button.place(x = 500, y = 420, width=25, height=25)

    searchFrame = customtkinter.CTkFrame(master=app, corner_radius=7)
    searchFrame.place(x=235, y=20, width=515, height=75)

    segemented_button_var = customtkinter.StringVar(value="auto")
    segemented_button = customtkinter.CTkSegmentedButton(
        master=app,
        values=["auto", "sql", "filter", "map", "sort"],
        variable=segemented_button_var,
    )
    segemented_button.place(x=350, y=10, width=300)

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
        master=searchFrame, text="⟳", fg_color="#343638"
    )
    previewButton.place(x=10, y=30, width=30, height=33)

    okButton = customtkinter.CTkButton(master=searchFrame, text="Ok", fg_color="#343638")
    okButton.place(x=460, y=30, width=30, height=33)

    SaveButton = customtkinter.CTkButton(
        master=app,
        text="✓ Save",
        fg_color="#343638",
        bg_color="#282424",
        command=lambda: onTableSave(table),
        corner_radius=7
    )
    SaveButton.place(x=680, y=457, width=70, height=33)

    logsDisplayFrame = customtkinter.CTkFrame(master=app, corner_radius=7)
    logsDisplayFrame.place(x=20, y=458, width=500, height=30)

    logsLabel = customtkinter.CTkLabel(
        master=app, bg_color="#302c2c", font=("Helvetica bold", 13)
    )
    logsLabel.place(x=25, y=460)

    navigatorFrame = customtkinter.CTkFrame(master=app, corner_radius=7, fg_color="#343638",)
    navigatorFrame.place(x=530, y=458, width=135, height=30)

    navigatorIndicator = customtkinter.CTkLabel(
        master=navigatorFrame, bg_color="#343638",text="17/23",corner_radius=7
    )
    navigatorIndicator.place(x=45, y=0,width=50,height=30 )

    pageSystem= PageSystem(table,navigatorIndicator,[[i,"j","h","j","J"] for i in range(347)])

    navigatorNavLeft = customtkinter.CTkButton(
        master=navigatorFrame,
        text="<",
        fg_color="#343638",
        command=lambda: pageSystem.onNavigateButtonClick(2)
       # command=onTableSave
    )
    navigatorNavLeft.place(x=25, y=2,width=20,height=25 )
    navigatorNavLeftEnd = customtkinter.CTkButton(
        master=navigatorFrame,
        text="<<",
        fg_color="#343638",
        #bg_color="gray",
        font=("Helvetica", 11),
        command=lambda: pageSystem.onNavigateButtonClick(1)
       # command=onTableSave
    )
    navigatorNavLeftEnd.place(x=5, y=2,width=23,height=25 )


    navigatorNavRight = customtkinter.CTkButton(
        master=navigatorFrame,
        text=">",
        fg_color="#343638",
        command=lambda: pageSystem.onNavigateButtonClick(3)
       # command=onTableSave
    )
    navigatorNavRight.place(x=90, y=2,width=20,height=25 )
    navigatorNavRightEnd = customtkinter.CTkButton(
        master=navigatorFrame,
        text=">>",
        fg_color="#343638",
        #bg_color="gray",
        font=("Helvetica", 11),
        command=lambda: pageSystem.onNavigateButtonClick(4)
       # command=onTableSave
    )
    navigatorNavRightEnd.place(x=110, y=2,width=23,height=25 )



    setLogLabel(
        "Warning: Hola que pasa das ist der log (noch nicht mit logger verbunden)", "orange"
    )

    pageSystem.onUIReady()
    onGuiReady2(table, pageSystem)

    app.mainloop()

#loadGUI()