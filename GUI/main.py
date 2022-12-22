import tkinter
import customtkinter
from scrollableTable import scrollableTable
from interface import *
import random
import time

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("800x500")

frame = customtkinter.CTkFrame(master=app, width=200, height=390, corner_radius=10)
frame.place(x=20, y=10)

label = customtkinter.CTkLabel(
    master=frame, text="Minecraft Datenbank", font=("Courier", 15)
)
label.place(x=17, y=1)

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


# GUI SPAWN FUNCTIONS
xStart = 60
def placeTableButton(title, event):
    global xStart
    customtkinter.CTkButton(master=app, text=title, command=event, fg_color="#343638").place(x=45, y=xStart)

    xStart += 35

def spawnTableButtons():
    for name in tablesNames.keys():
        print(name)
        placeTableButton(name, tablesNames[name])

spawnTableButtons()


table = scrollableTable(app,tableData=[["Welt","tsdsddds"],[[random.randint(0,1000),"t"] for i in range(100)]],pos=(250,100,500,300))
table.setTableHeader(["bebe","bebe"])
table.fill([[random.randint(0,1000),"t"] for i in range(100)])
table.appendEmptyRowOnTop()

button = customtkinter.CTkButton(master=app,text="Add Row",command=table.appendEmptyRowOnTop)
button.place(x = 250, y = 420, width=75, height=50)



app.mainloop()
