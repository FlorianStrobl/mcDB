import customtkinter
import tkinter
import platform

class ScrollFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        self.canvas = customtkinter.CTkCanvas(self, borderwidth=0,highlightthickness=0,bg="#2b2b2b")
        self.viewPort = tkinter.Frame(self.canvas,bg="#2b2b2b")
        self.vsb = customtkinter.CTkScrollbar(self, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        self.viewPort.bind('<Enter>', self.onEnter)
        self.viewPort.bind('<Leave>', self.onLeave)

        self.onFrameConfigure(None)
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)
    def onMouseWheel(self, event):
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )
    def onEnter(self, event):
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)
    def onLeave(self, event):
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")
    def getPos(self):
        self.update()
        return self["width"]

class scrollableTable(customtkinter.CTkFrame):
    def __init__(self,app,tableData,pos):
        customtkinter.CTkFrame.__init__(self, app)
        self.scrollFrame = ScrollFrame(self)

        self.scrollFrame.pack(side="top", fill="both", expand=True)
        self.currentEntrys = []
        self.app = app
        self.colors = ["#343638","#2d2f31"]
        self.actionColumnWidth = 25

        self.numberCreatedRows = 0

        self.x = pos[0]
        self.y = pos[1]
        self.widthFrame = pos[2]
        self.heightFrame = pos[3]

        #[tableTitle, tableHeader, tableBody]
        self.tableData=tableData
        # inkl. Mülleimer
        self.tableDataBodyWidgets = []
        self.tableDataHeaderWidgets = []
        self.colorIndex = 0
        self.place(x = self.x,y = self.y, width = self.widthFrame,height = self.heightFrame)
        self.setTableHeader(self.tableData[0])
        self.fill(self.tableData[1])


        # Verlauf damit wenn bei änderungen der Tabelle die Rows trotzdem immer wiedergefunden werden können
        # BEISPIEL:
        # [["add"],["delete",3]]
        # Zeichnet den Verlauf von actions auf -> SUPER Wichtig für events
        self.steps = []

    def calculateStepsFromStart(self,row):
        # Berechnet wie die Rows ID's sein sollen relativ zu den vom Anfang also "row" hier im parameter(für den delete Event)
        newRow = row
        for step in self.steps:
            if(step[0] == "add"):
                newRow += 1
            elif(step[0] == "delete"):
                if(newRow > step[1]):
                    newRow -= 1
        return newRow
    def updateTable(self):
        self.place(x = self.x,y = self.y, width = self.widthFrame,height = self.heightFrame)
        self.setTableHeader(self.tableData[0])
        self.fill(self.tableData[1])
    def updateTableBody(self):
        self.fill(self.tableData[1])
    def clearTableDataBodyWidgets(self):
        for row in self.tableDataBodyWidgets:
            for element in row:
                try: element.destroy()
                except: pass
        self.tableDataBodyWidgets = []
    def clearTableDataHeaderWidgets(self):
        for element in self.tableDataHeaderWidgets:
            element.destroy()
        self.tableDataHeaderWidgets = []
    #aka draw function - geht nur wenn gleiche Anzahl an Columns
    #Vorallem für bessere performance da
    def textFill(self,tableBody):
        # "-1" wegen den Mülleimer object
        if(self.tableDataBodyWidgets == []):
            return "none"

        if(len(self.tableDataBodyWidgets[0])-1 != len(tableBody[0])):
            return "none"

        # -1 because there is always a müllemer
        rowsLengthOld = len(self.tableDataBodyWidgets)
        rowsLength = len(tableBody)

        #AUSGLEICHEN DER ROWS AUF DER TABELLE:
        rowsDifference = (rowsLengthOld - rowsLength) * -1
       # print(rowsDifference)
        if(rowsDifference > 0):
            for i in range(rowsDifference):
                self.appendEmptyRowOnTop()
        elif(rowsDifference < 0):
            #-1 weil es da IMMER negativ ist
            for i in range(rowsDifference * -1):
                self.onRemove(0)

        self.tableData[1] = tableBody

        # Einsetzen aller Texte von TABLEBODY in die Tabelle
        #print(len(self.tableDataBodyWidgets))

        for widgetsRowCounter in range(len(self.tableDataBodyWidgets)):
            widgetsRow = self.tableDataBodyWidgets[widgetsRowCounter]
            # -1 Because we want to ignore the Mülleimer
            for widgetCounter in range(len(widgetsRow)-1):
                inputField = widgetsRow[widgetCounter]
                inputField.delete(0,customtkinter.END)
                #print(widgetsRowCounter, widgetCounter)
                inputField.insert(0,tableBody[widgetsRowCounter][widgetCounter])
        return "succes"

    def fill(self,tableBody):
        self.steps = []
        # Wenn die gleichen Anzahl and columns vorhanden ist wie bei der vorherigen Tabelle,
        # ist es nicht nötig, die Tabelle komplett neu zu erstellen.
        # --> Mann kann so die fehlenden/zu vielen rows hinzufügen/entfernen und so die Tabelle schneller generieren
        if(self.textFill(tableBody) == "succes"):
            return

        self.clearTableDataBodyWidgets()
        #tableData.append((1,2))
        #tableData.insert(0,(("","")))
        widthCurrentFrame = self.widthFrame-20
        numberColumns = len(tableBody[0])

        numberRows = len(tableBody)
        for row in range(numberRows):
            rowWidgets = []
            if(tableBody[row] == None):
                    #print("is none")
                    continue
            for col in range(numberColumns+1):
                if(col < numberColumns):
                    myEntry = customtkinter.CTkEntry(self.scrollFrame.viewPort,corner_radius=0,width=(widthCurrentFrame - self.actionColumnWidth)/numberColumns,fg_color=self.colors[self.colorIndex % 2])
                    myEntry.grid(row=row, column=col)

                    rowWidgets.append(myEntry)
                    try:
                        myEntry.insert(0, tableBody[row][col])
                    except:
                        myEntry.insert(0, "Data not found")
                else:
                    deleteButton = customtkinter.CTkButton(self.scrollFrame.viewPort,text="🗑",command=lambda row=row: self.onRemove(self.calculateStepsFromStart(row)),  corner_radius=0,width=self.actionColumnWidth,fg_color=self.colors[self.colorIndex % 2])
                    deleteButton.grid(row=row, column=col)
                    rowWidgets.append(deleteButton)
            self.colorIndex += 1
            self.tableDataBodyWidgets.append(rowWidgets)

            self.tableData[1] = tableBody
    def setTableHeader(self,arr):
        self.clearTableDataHeaderWidgets()
        startX = self.x + 5
        y = self.y - 30
        fillstartLength = 10
        fillstart = self.x
        adding = 19

        acL = self.actionColumnWidth
        if(fillstart != None and fillstartLength != None):
            myLabel = customtkinter.CTkLabel(master=self.app, text="",font=("Helvetica",15,"bold"),fg_color="#2b2b2b",anchor="w")
            myLabel.place(x = fillstart,y = y,width = fillstartLength)
            self.tableDataHeaderWidgets.append(myLabel)

        self.scrollFrame.update()
        for i in range(len(arr)):
            subWidth = (self.widthFrame-20 -acL)/len(arr)
            myLabel1 = customtkinter.CTkLabel(master=self.app, text=arr[i],font=("Helvetica",15,"bold"),fg_color="#2b2b2b",anchor="w")
            myLabel1.place(x = startX,y = y,width = subWidth)
            self.tableDataHeaderWidgets.append(myLabel1)
            startX += subWidth

        #myLabel2 = customtkinter.CTkLabel(master=self.app, text="d",fg_color="#2b2b2b",anchor="w")

        button2 = customtkinter.CTkButton(master=self.app,text="+",command=self.appendEmptyRowOnTop,  corner_radius=0,fg_color="#343638")
        button2.place(x = startX-5, y = y, width=acL,)

        #myLabel2.place(x = startX,y = y,width = acL)
        startX+=acL-3
        self.tableDataHeaderWidgets.append(button2)



        myLabel3 = customtkinter.CTkLabel(master=self.app, text="",fg_color="#2b2b2b",anchor="w")
        myLabel3.place(x = startX,y = y,width = adding)
        self.tableDataHeaderWidgets.append(myLabel3)

        self.tableData[0] = arr
    def onRemove(self,rowNumber):
        self.steps.append(["delete", rowNumber])
        self.tableData[1].pop(rowNumber)
        for row in self.tableDataBodyWidgets[rowNumber]:
            row.destroy()
        self.tableDataBodyWidgets.pop(rowNumber)
    def appendEmptyRowOnTop(self):
        def moveAllRowsHorizontalyDownOne():
            for y in range(len(self.tableDataBodyWidgets)):
                widgetRow = self.tableDataBodyWidgets[y]
                for widget in widgetRow:
                    widget.grid(row = y + 1)
        moveAllRowsHorizontalyDownOne()

        self.numberCreatedRows +=1
        self.steps.append(["add"])
        numberColumns = len(self.tableData[0])
        widthCurrentFrame = self.widthFrame-20
        rowWidget = []
        gridRow = 0
        for col in range(numberColumns+1):
                if(col < numberColumns):
                    myEntry = customtkinter.CTkEntry(self.scrollFrame.viewPort,corner_radius=0,width=(widthCurrentFrame - self.actionColumnWidth)/numberColumns,fg_color=self.colors[self.colorIndex % 2])
                    myEntry.grid(row=gridRow, column=col)

                    rowWidget.append(myEntry)

                    myEntry.insert(0, "")
                else:
                    deleteButton = customtkinter.CTkButton(self.scrollFrame.viewPort,text="🗑",command=lambda row=gridRow, createdRows=self.numberCreatedRows: self.onRemove(self.calculateStepsFromStart(row-createdRows)),corner_radius=0,width=self.actionColumnWidth,fg_color=self.colors[self.colorIndex % 2])
                    deleteButton.grid(row=gridRow, column=col)
                    rowWidget.append(deleteButton)
        self.colorIndex += 1
        self.tableDataBodyWidgets.insert(0, rowWidget)
        self.tableData[1].insert(0, ["" for i in range(numberColumns)])
       #self.tableData[1].insert(0,["" for i in self.tableData[0]])
       #self.updateTableBody()
    def saveAllToTableData(self):
        # TODO YET
        return -1
