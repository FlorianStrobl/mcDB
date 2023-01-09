import customtkinter
import tkinter
import platform

# Fast der ganze Inhalt von "ScrollFrame"
# kommt von diesem Code: https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
# Ein ScrollFrame ist einfach WIE ein Frame, außer dass man scrollen wenn dieser zu voll ist
class ScrollFrame(customtkinter.CTkFrame):

    def __init__(self, parent):

        # Ctk Frame in self erstellen
        super().__init__(parent)  # create a frame (self)

        self.canvas = customtkinter.CTkCanvas(
            self, borderwidth=0, highlightthickness=0, bg="#2b2b2b"
        )

        # Canvas erstellen
        self.viewPort = tkinter.Frame(self.canvas, bg="#2b2b2b")

        # Scrollbar erstellen
        self.vsb = customtkinter.CTkScrollbar(self, command=self.canvas.yview)

        # Sagen dass, man den canvas horizontal mit der scrollbar "vbs" kontrollieren kann
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window(
            (4, 4), window=self.viewPort, anchor="nw", tags="self.viewPort"
        )


        # Andere events setzen
        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        self.viewPort.bind("<Enter>", self.onEnter)
        self.viewPort.bind("<Leave>", self.onLeave)

        self.onFrameConfigure(None)

        self.widthh = None

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        """Reset the canvas window to encompass inner frame when required"""
        canvas_width = event.width
        self.width = canvas_width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    # diese 2 Funktionen wurden selber hinzugefügt
    def disableScroll(self):
        self.canvas.configure(yscrollcommand=lambda x, y: None)

    def enableScroll(self):
        self.canvas.configure(yscrollcommand=self.vsb.set)

    def onMouseWheel(self, event):

        if platform.system() == "Windows":
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == "Darwin":
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

    def onEnter(self, event):
        if platform.system() == "Linux":
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):
        if platform.system() == "Linux":
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")

    def getPos(self):
        self.update()
        return self["width"]


# Benutzt die Klasse ScrollFrame:
# Kann eine bestimme tabelle mit deren columns anzeigen
class scrollableTable(customtkinter.CTkFrame):
    # pos ist ein [x,y] array
    def __init__(self, app, tableData, pos):
        customtkinter.CTkFrame.__init__(self, app)
        self.scrollFrame = ScrollFrame(self)
        self.oldColumns = None
        self.scrollFrame.pack(side="top", fill="both", expand=True)
        self.currentEntrys = []
        self.app = app
        # verschiedene mögliche Farben von rows
        self.colors = ["#343638", "#2d2f31"]
        self.actionColumnWidth = 25

        # Wie die table am Anfang ist -> in diesem Fall: AUS
        self.currentState = customtkinter.DISABLED
        self.createButton = None

        self.numberCreatedRows = 0

        self.x = pos[0]
        self.y = pos[1]
        self.widthFrame = pos[2]
        self.heightFrame = pos[3]

        #Speichert die Daten die in der Tabelle gespeichert sind in diesem Format [tableTitle, tableHeader, tableBody]
        self.tableData = tableData

        # inkl. Mülleimer
        # Speichert alle Widgets: Body sind ein 2D Array mit jeweils pro Stelle ein Array mit den Input Fields und am Ende die Delete Buttons
        self.tableDataBodyWidgets = []

        # Speichert alle widgets die in dem Header sind (also alle Header die mach für die Columns Anzeige braucht)
        self.tableDataHeaderWidgets = []

        # Datensätze haben in der visuellen Ausgabe immer eine von 2 Farben. (2 grautöne)
        # colorIndex wird pro neuen Datensatz insert immer incrementet
        # --> ist color index even, so wird einn bestimmtes dem datensatz zugewiese, wenn nicht dann wird ein anderes Grauton
        self.colorIndex = 0

        self.place(x=self.x, y=self.y, width=self.widthFrame, height=self.heightFrame)

        # Es werden die Daten die bei der Erstellung von dieser Klasser gegeben werden müssen angezeigt
        # Setzt die columns names
        self.setTableHeader(self.tableData[0])
        # Setzt alle inout fiels values bzw. zeigt die datensätze an
        self.fill(self.tableData[1])

        # Event Listener: 0:Delete  1: Add

        #Speichern der EventListener: wird untern bei der eventLister funktion erklärt
        self.eventListenerFunctions = [[], []]

    # Aktualisiert die Table: die gespeicherten Columsn names und datensätze (im tableData Array) werden visual aktualisiert
    def updateTable(self):
        self.place(x=self.x, y=self.y, width=self.widthFrame, height=self.heightFrame)
        self.setTableHeader(self.tableData[0])
        self.fill(self.tableData[1])

    # Aktualisiert nur Visual die Datensätze
    def updateTableBody(self):
        self.fill(self.tableData[1])

    # Löscht alle visual angezeigte Datensätze und deren Delete Button und löscht sie auch in den tableDataBodyWidgets Array (allerdings nicht in tableData)
    def clearTableDataBodyWidgets(self):
        # Alle rows werden durchgegangen
        for row in self.tableDataBodyWidgets:
            for element in row:
                # Die row wird jeweils durchgegangen
                try:
                    # Sie wird destroyt wenns kein Error gibt
                    element.destroy()
                except:
                    pass
        # löschtlköscht nicht den jeweilen Eintrag in den Array, deswegen muss man diesen clearen
        self.tableDataBodyWidgets = []

    # löscht alle angezeigten columns widgets indem so vorgegengen wird wie in der obigen Funktion
    def clearTableDataHeaderWidgets(self):
        for element in self.tableDataHeaderWidgets:
            element.destroy()
        self.tableDataHeaderWidgets = []

    # aka draw function - geht nur wenn gleiche Anzahl an Columns
    # Vorallem für bessere performance da

    # Für leicheteren Acces auf events in der Table function

    # Mann kann bestimmte Event Lister functions erstellen;
    # --> diese nimmt als parameter die action (entweder "onAddRow " oder "onDeleteRow")
    # ---> Auch muss man den parameter beim Aufruf einer functon zuweisen, die danach jedes mal jeweils nach der action: "action" (also add oder delete) ausgeführt wird
    def addEventListener(self, action, function):
        if action == "onDeleteRow":
            self.eventListenerFunctions[0].append(function)
        elif action == "onAddRow":
            self.eventListenerFunctions[1].append(function)

    # Erklärung über der Funktion namens "fill"
    def textFill(self, tableBody):

        tableBody = tableBody.copy()

        # "-1" wegen den Mülleimer object

        # Wenn self.tableDataBodyWidgets leer ist müsste diese Funktion nicht ausgeführt werden
        if self.tableDataBodyWidgets == []:
            return "none"

        # Wenn table body was behinhaltet aber die länge der columns von tableDataBodyWidgets ungleich die länge der columns von tableBody ist,
        # dann müsste diese Funktion nicht ausgeführt werden - also return "none"
        if tableBody != [] and len(self.tableDataBodyWidgets[0]) - 1 != len(
            tableBody[0]
        ):
            return "none"

        #  Hier werden mehr rows hinzugefügt oder rows entfernt wenn die vorherige Tabelle mehr oder weniger rowas hatte als aktuell
        # -1 because there is always a müllemer
        rowsLengthOld = len(self.tableDataBodyWidgets)
        rowsLength = len(tableBody)


        # Ausrechnen der Differenz um zu wissen ob datensätze hinzugefügt / deleted werden müssen
        rowsDifference = (rowsLengthOld - rowsLength) * -1
        if rowsDifference > 0:
            for i in range(rowsDifference):

                self.appendEmptyRowOnTop(fromAutoScript=True)
        elif rowsDifference < 0:
            # -1 weil es da IMMER negativ ist
            for i in range(rowsDifference * -1):
                self.onRemove(0, fromAutoScript=True)

        self.tableData[1] = tableBody

        # Einsetzen aller Texte von TABLEBODY in die Tabellen Widgets
        for widgetsRowCounter in range(len(self.tableDataBodyWidgets)):
            widgetsRow = self.tableDataBodyWidgets[widgetsRowCounter]
            # -1 weil wie nicht den mülleimer editieren wollen
            for widgetCounter in range(len(widgetsRow) - 1):
                inputField = widgetsRow[widgetCounter]
                # Editieren des Input Fields
                inputField.delete(0, customtkinter.END)
                inputField.insert(
                    0,
                    tableBody[widgetsRowCounter][widgetCounter]
                    if tableBody[widgetsRowCounter][widgetCounter] != None
                    else "null",
                )

        self.updateEvents()
        return "succes"

    # Buttons haben immer ein Command, der eine Funkction aufruft mit einen Parameter der beschreibt welcher Datensatz gelöscht werden muss
    # Wenn man da z.B Button nummer 3 löscht in z.B in 1,2,3,4
    # dann haben wir als lösch buttons nur noch 1,2,4
    # natürlich gibt es den Datensatz nummer 4 nicht mehr, es würde also  zu nen error führen wenn man versucht diesen zu löschen
    # Aber diese Funktion ist die Rettung
    # Diese geht durch alle deleteButton durch, und numeriert den Parameter von self.onRemove(i) neu
    # Der array in dem obiegen Beispiel wäre also dann 1,2,3
    # Diese function wird also nach jeder hinzufügung eines Buttons oder nach jedem dete des Buttons ausgeführt,
    # um deren Events auf dem neusten Stand zu halten
    def updateEvents(self):
        for i in range(len(self.tableDataBodyWidgets)):
            row = self.tableDataBodyWidgets[i]
            deleteButton = row[len(self.tableDataBodyWidgets[0]) - 1]
            deleteButton.configure(command=lambda i=i: self.onRemove(i))

    # Wird aufgerufen, wenn die table neu gefillt werden muss - "tableBody" ist hier ein 2D Array der alle Datensätze beinhaltet
    # Um an performance zu sparen, wird natürlich nicht jedes mal die tabelle gecleer und neue datensätze hinzugefüht,
    # sondern WENN es die gleiche anzahl an colunmns wie in der vorherigen tabelle die angezeigt wurde gibt
    #       -->  müssen die table widgets  nicht gecleart werden, sondern deren text kann ersatzt werden
    #            -> Die Function textFill wird aufgerufen.
    # Und wenn dort "tableBody" weniger/mehr visuelle Datensätze hat als die die von die vorherig erstelle Tabelle hat,
    # werden dann so auch welche dementsprechend welche gelöscht, hinzugefüht
    # SONST WENN es nicht die gleiche Anzahl an columns wie in der vorherigen Tabelle gibt:
        # Dann werden alle widgets geclear und mit der richtigen columns anzehal neu gesetzt
    def fill(self, tableBody):
        self.updateEvents()

        self.tableBody = []

        if len(tableBody) == 0:
            self.clearTableDataBodyWidgets()
            self.tableData[1] = []
            return

        # Wenn die gleichen Anzahl and columns vorhanden ist wie bei der vorherigen Tabelle,
        # ist es nicht nötig, die Tabelle komplett neu zu erstellen.
        # --> Mann kann so die fehlenden/zu vielen rows hinzufügen/entfernen und so die Tabelle schneller generieren

        # Wenn textFill erfolgreich ist, dann kann returnt werden da alles schon ge"textfilled" ist
        if self.textFill(tableBody) == "succes":
            return


        self.clearTableDataBodyWidgets()
        # Wichtig damit, wenn man die table breiter macht dass es auch bei den rows widgets angepasst wird
        widthCurrentFrame = self.widthFrame - 20
        numberColumns = len(tableBody[0])

        numberRows = len(tableBody)
        for row in range(numberRows):
            rowWidgets = []
            if tableBody[row] == None:
                continue
            for col in range(numberColumns + 1):
                if col < numberColumns:
                    myEntry = customtkinter.CTkEntry(
                        self.scrollFrame.viewPort,
                        corner_radius=0,
                        width=(widthCurrentFrame - self.actionColumnWidth)
                        / numberColumns,
                        fg_color=self.colors[self.colorIndex % 2],
                    )
                    myEntry.grid(row=row, column=col)

                    rowWidgets.append(myEntry)
                    try:
                        myEntry.insert(
                            0,
                            tableBody[row][col]
                            if tableBody[row][col] != None
                            else "null",
                        )
                    except:
                        myEntry.insert(0, "Data not found")
                else:
                    deleteButton = customtkinter.CTkButton(
                        self.scrollFrame.viewPort,
                        text="🗑",
                        command=lambda row=row: self.onRemove(row),
                        corner_radius=0,
                        width=self.actionColumnWidth,
                        fg_color=self.colors[self.colorIndex % 2],
                    )
                    deleteButton["state"] = customtkinter.DISABLED
                    deleteButton.grid(row=row, column=col)
                    rowWidgets.append(deleteButton)

            self.colorIndex += 1
            self.tableDataBodyWidgets.append(rowWidgets)
            self.tableData[1] = tableBody
            self.updateEvents()

    #Ändert die visuellen columsn beschrifften auf "array"
    def setTableHeader(self, arr):
        # Ein bisschen gehardcoded damit die headers bei ner bestimmten tabelle kleiner werden
        isTheTablePlays = arr[0] == "player_id" and arr[len(arr) - 1] == "role"

        # Sonst wird alles nochmal erstellt obwohl es vorher schonmal erstellt wurde
        if self.oldColumns == arr:
            return
        self.oldColumns = arr.copy()

        self.clearTableDataHeaderWidgets()
        startX = self.x + 5
        y = self.y - 30
        fillstartLength = 10
        fillstart = self.x
        adding = 19

        self.tableDataHeaderWidgets = []

        acL = self.actionColumnWidth
        if fillstart != None and fillstartLength != None:
            myLabel = customtkinter.CTkLabel(
                master=self.app,
                text="",
                font=("Helvetica", 15, "bold"),
                fg_color="#2b2b2b",
                anchor="w",
            )
            myLabel.place(x=fillstart, y=y, width=fillstartLength)
            self.tableDataHeaderWidgets.append(myLabel)

        self.scrollFrame.update()
        for i in range(len(arr)):
            subWidth = (self.widthFrame - 20 - acL) / len(arr)
            myLabel1 = customtkinter.CTkLabel(
                master=self.app,
                text=arr[i],
                font=("Helvetica", 12 if isTheTablePlays else 15, "bold"),
                fg_color="#2b2b2b",
                anchor="w",
            )
            myLabel1.place(x=startX, y=y, width=subWidth)
            self.tableDataHeaderWidgets.append(myLabel1)
            startX += subWidth

        # myLabel2 = customtkinter.CTkLabel(master=self.app, text="d",fg_color="#2b2b2b",anchor="w")

        self.createButton = customtkinter.CTkButton(
            master=self.app,
            text="+",
            command=self.appendEmptyRowOnTop,
            corner_radius=0,
            fg_color="#343638",
            state=self.currentState,
        )
        self.createButton.place(
            x=startX - 5,
            y=y,
            width=acL,
        )

        # myLabel2.place(x = startX,y = y,width = acL)
        startX += acL - 3
        self.tableDataHeaderWidgets.append(self.createButton)

        myLabel3 = customtkinter.CTkLabel(
            master=self.app, text="", fg_color="#2b2b2b", anchor="w"
        )
        myLabel3.place(x=startX, y=y, width=adding)
        self.tableDataHeaderWidgets.append(myLabel3)

        self.tableData[0] = arr

    # Ändern des status der tabelle - ist state customtkinter.disabled, dann kann der user nicht mehr mit der tabelle interagieren
    def setState(self, _state):

        self.currentState = _state
        try:
            self.createButton.configure(state=_state)
        except:
            x = 0
        try:
            for widgetRow in self.tableDataBodyWidgets:
                for widget in range(len(widgetRow)):
                    widgetRow[widget].configure(state=_state)
        except:
            # Error
            x = 0

    # Sender erwähnt,default fase, ob diese Funktion direkt vom user aufgerufen wird (über button klick) oder ob die funktion von einer for schleife oder sowas aufgerufen wurde
    def onRemove(self, rowNumber, fromAutoScript=False):

        self.tableData[1].pop(rowNumber)

        for row in self.tableDataBodyWidgets[rowNumber]:
            row.destroy()

        self.tableDataBodyWidgets.pop(rowNumber)
        self.updateEvents()
        # pass
        if not fromAutoScript:
            for deleteEvent in self.eventListenerFunctions[0]:
                deleteEvent(rowNumber)

    # Returnt direkt die Inputs von der Table.
    def getTablesInputs(self):
        result = []
        # Es wird jede row durchgegangen
        for widgetRow in self.tableDataBodyWidgets:
            subresult = []
            # Es wird jedes element durchgegangen bis auf das letzte und ui subresult appended -> weil das letzte das Mülleimer objekt ist
            for widget in range(len(widgetRow) - 1):
                subresult.append(widgetRow[widget].get())
            # Dieser row input wird result appended
            result.append(subresult)
        return result

   # Fügt eine Leer zeile in der datenbase oben hinzu
    def appendEmptyRowOnTop(self, fromAutoScript=False):
        numberColumns = len(self.tableData[0])

        #Alle widgets auf der grid um eins nach unten verschieben um platz für die topRow zu erstellen
        def moveAllRowsHorizontalyDownOne():
            for y in range(len(self.tableDataBodyWidgets)):
                widgetRow = self.tableDataBodyWidgets[y]
                for widget in widgetRow:
                    widget.grid(row=y + 1)

        moveAllRowsHorizontalyDownOne()

        self.numberCreatedRows += 1
        # Wichtig damit, wenn man die table breiter macht dass es auch bei den rows widgets angepasst wird
        widthCurrentFrame = self.widthFrame - 20
        rowWidget = []
        gridRow = 0
        for col in range(numberColumns + 1):
            if col < numberColumns:
                myEntry = customtkinter.CTkEntry(
                    self.scrollFrame.viewPort,
                    corner_radius=0,
                    width=(widthCurrentFrame - self.actionColumnWidth) / numberColumns,
                    # nächste Farbe wird gesetzt
                    fg_color=self.colors[self.colorIndex % 2],
                )
                myEntry.grid(row=gridRow, column=col)

                rowWidget.append(myEntry)

                myEntry.insert(0, "")
            else:
                deleteButton = customtkinter.CTkButton(
                    self.scrollFrame.viewPort,
                    text="🗑",
                    command=lambda row=gridRow, createdRows=self.numberCreatedRows: self.onRemove(
                        -1
                    ),
                    corner_radius=0,
                    width=self.actionColumnWidth,
                    fg_color=self.colors[self.colorIndex % 2],
                )

                deleteButton.grid(row=gridRow, column=col)
                rowWidget.append(deleteButton)

        # colorIdex wird
        self.colorIndex += 1
        self.tableDataBodyWidgets.insert(0, rowWidget)
        self.tableData[1].insert(0, ["" for i in range(numberColumns)])

        # Sehr wichtig damit delete events funktionnieren (wie oben gesagt bei "updateEvents")
        self.updateEvents()
        if not fromAutoScript:
            for addEventRow in self.eventListenerFunctions[1]:
                addEventRow()
