import tkinter
import customtkinter
from scrollableTable import scrollableTable
from interface import *
import random

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("800x450")

frame = customtkinter.CTkFrame(master=app, width=200, height=420, corner_radius=10)
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


table = scrollableTable(app,x=250,y=75,width=500,height=300)
table.fill([[random.randint(0,1000),"t"] for i in range(20)])

table.setTableHeader(["Welt","tsdsddds"],255,45,250,10,adding=19)
app.mainloop()
