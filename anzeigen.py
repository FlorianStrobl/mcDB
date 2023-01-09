import customtkinter
import sqlite3

# Variablen die gegeben sind:
# - widthCurrentFrame
# - WidthforEntry
# - WidthforColumn
# - scrollFrame.viewPort -> ist wie "Frame" aber mit scrollBar
# - onRemove -> Eine Row löschen
# - clearTableDataHeaderWidgets() -> Alles wird gecleert
# - x - X Koordinate von dem table frame

def anzeigen_columns(columns):

        # Die alten columns werden geleert
        clearTableDataHeaderWidgets()

        # Jedes Element vom gegebenen Array wird durchgegangen und ein Label wird
        # über der Tabelle erstellt für die dementsprechende Columns
        startX = x + 5
        for i in range(len(arr)):
            subWidth = WidthforColumn
            myLabel1 = customtkinter.CTkLabel(
                master=app,
                text=columns[i],
                font=("Helvetica", 12, "bold"),
                fg_color="#2b2b2b",
                anchor="w",
            )
            myLabel1.place(x=startX, y=y, width=subWidth)

            tableDataHeaderWidgets.append(myLabel1)
            startX += subWidth


def anzeigen_body(tableBody):
    # Erstellung des cursors

    for row in range(len(tableBody)):
        # Jede columns von der row wird durchgegangen
        lastCol = 0
        for col in range(len(row)):
                lastCol = col
                # Erstellt ein Entry mit spitzen ecken, plaziere den auf den ViewFrame und gebe den die width widthForEntry
                # (die immer in Function von der Anzahl der Columns ausgerechnet wird)
                myEntry = customtkinter.CTkEntry(
                    scrollFrame.viewPort,
                    corner_radius=0,
                    width=widthForEntry
                )
                # Plaziere die Entry auf einer Grid auf dem View Port
                myEntry.grid(row=row, column=col)

                # Versuche wenn dies kein Error gibt, in dem Entry den dementsprechnenden Text von tableBody reinzuplazieren
                # Wenn dies nicht klappt, setze in dem Input Field "Data not found" ein
                try:
                    myEntry.insert(
                        0,
                        tableBody[row][col]
                    )
                except:
                    myEntry.insert(0, "Data not found")

        # Wenn alle colummns von meiner row erstellt wurden, erstelle bitte auch ein deleteButton
        # der für das löschen der jeweiligen row verantwortlich ist
        deleteButton = customtkinter.CTkButton(
            scrollFrame.viewPort,
            text="🗑",
            command=lambda row=row: self.onRemove(row),
            corner_radius=0,
            width=self.actionColumnWidth,
        )
        # Setze den delete button eine column weiter als das letzte input field das auf der row platziert wurde
        deleteButton.grid(row=row, column=lastCol + 1)

# Hier werden Daten z.B aus der Tabelle Block gefetcht
cursor: sqlite3.Connection.cursor = sqlite3.connect("minecraftDatabase.db").cursor()

cursor.execute("SELECT * FROM Block")
resultData = cursor.fetchall()
anzeigen_body(resultData)
columnNames= list(map(lambda x: x[0], cursor.description))
anzeigen_columns(columnNames)
