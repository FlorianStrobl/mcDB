import tkinter
import customtkinter
from scrollableTable import scrollableTable
from interface import *

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


def onTableButtonClick(buttonName):
    # Backend Code
    print(buttonName)


# Title needs to be in "tables names"
xStart = 60


def placeTableButton(title, event):
    global xStart
    customtkinter.CTkButton(master=app, text=title, command=event).place(x=40, y=xStart)

    xStart += 35


def spawnTableButtons():
    for name in tablesNames.keys():
        print(name)
        placeTableButton(name, tablesNames[name])


spawnTableButtons()








scrollableTable(app).place(x=250,y=75, width=515, height=300)

app.mainloop()
