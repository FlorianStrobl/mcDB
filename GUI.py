import tkinter
import customtkinter
from tkscrolledframe import ScrolledFrame

COLORS = [
    ("black", "white"),
    ("#0000AA", "white"),
    ("#00AA00", "white"),
    ("#00AAAA", "white"),
    ("#AA0000", "white"),
    ("#AA00AA", "white"),
    ("#AA5500", "white"),
    ("#AAAAAA", "black"),
    ("#555555", "white"),
    ("#5555FF", "black"),
    ("#55FF55", "black"),
    ("#55FFFF", "black"),
    ("#FF5555", "black"),
    ("#FF55FF", "black"),
    ("#FFFF55", "black"),
    ("white", "black"),
]

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("800x450")


def button_function():
    print("button pressed")


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


def demo():
    """Display a demonstration of the ScrolledFrame widget."""

    # Plenty of ways to close the window
    for seq in "<Escape>", "<Control-w>", "<Control-q>":
        app.bind(seq, lambda event: app.destroy())

    # ScrolledFrame widget
    sf = ScrolledFrame(app, width=640, height=480)
    sf.pack(side="top", expand=1, fill="both")

    customTkinter.frame  # Bind the arrow keys and scroll whee
    sf.bind_arrow_keys(app)
    sf.bind_scroll_wheel(app)
    # Create a frame within the ScrolledFrame
    inner_frame = sf.display_widget(tkinter.Frame)

    # Add a bunch of widgets to fill some space
    num_rows = 16
    num_cols = 16
    for row in range(num_rows):
        for column in range(num_cols):
            # Offset the palette each row to create a diagonal pattern
            background, foreground = COLORS[(column + row) % len(COLORS)]

            w = customtkinter.Label(
                inner_frame,
                width=15,
                height=5,
                background=background,
                foreground=foreground,
                borderwidth=2,
                relief="groove",
                anchor="center",
                justify="center",
                text=str(row * num_cols + column),
            )

            w.grid(row=row, column=column, padx=4, pady=4)


demo()
app.mainloop()
