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
    customtkinter.CTkButton(master=app, text=title, command=event).place(x=40, y=xStart)

    xStart += 35

def spawnTableButtons():
    for name in tablesNames.keys():
        print(name)
        placeTableButton(name, tablesNames[name])

spawnTableButtons()



def setTableHeader(arr,startX,y,width):
    for i in range(len(arr)):
        subWidth = width/len(arr)
        customtkinter.CTkLabel(master=app, text=arr[i],font=("Helvetica",15,"bold"),fg_color="#2b2b2b",anchor="w").place(x = startX,y = y,width = subWidth)
        startX += subWidth


table = scrollableTable(app,500)
table.place(x=250,y=75, width=500, height=300)
table.fill([[random.randint(0,1000)," hi"," Hello"," test"," miau"," be"] for i in range(20)])
print("spawned")

setTableHeader(["Welt","Player","Items","Days","Time","hola"],250,45,500-20)

app.mainloop()