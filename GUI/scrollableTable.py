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

        self.x = pos[0]
        self.y = pos[1]
        self.widthFrame = pos[2]
        self.heightFrame = pos[3]

        #[tableTitle, tableHeader, tableBody]
        self.tableData=tableData
        # inkl. Mülleimer
        self.tableDataBodyWidgets = []
        self.tableDataHeaderWidgets = []

        self.place(x = self.x,y = self.y, width = self.widthFrame,height = self.heightFrame)
        self.setTableHeader(self.tableData[0])
        self.fill(self.tableData[1])

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
    def fill(self,tableBody,clearBefore = True):
        if(clearBefore): self.clearTableDataBodyWidgets()
        #tableData.append((1,2))
        #tableData.insert(0,(("","")))
        widthCurrentFrame = self.widthFrame-20
        numberColumns = len(tableBody[0])

        numberRows = len(tableBody)
        colorIndex = 0
        for row in range(numberRows):
            rowWidgets = []
            if(tableBody[row] == None):
                    print("is none")
                    continue
            for col in range(numberColumns+1):
                if(col < numberColumns):
                    myEntry = customtkinter.CTkEntry(self.scrollFrame.viewPort,corner_radius=0,width=(widthCurrentFrame - self.actionColumnWidth)/numberColumns,fg_color=self.colors[colorIndex % 2])
                    myEntry.grid(row=row, column=col)

                    rowWidgets.append(myEntry)
                    try:
                        myEntry.insert(0, tableBody[row][col])
                    except:
                        myEntry.insert(0, "Data not found")
                else:
                    deleteButton = customtkinter.CTkButton(self.scrollFrame.viewPort,text="🗑",command=lambda row=row: self.onRemove(row),  corner_radius=0,width=self.actionColumnWidth,fg_color=self.colors[colorIndex % 2])
                    deleteButton.grid(row=row, column=col)
                    rowWidgets.append(deleteButton)
            colorIndex += 1
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

        myLabel2 = customtkinter.CTkLabel(master=self.app, text="",fg_color="#2b2b2b",anchor="w")
        myLabel2.place(x = startX,y = y,width = acL)
        startX+=acL-3
        self.tableDataHeaderWidgets.append(myLabel2)

        myLabel3 = customtkinter.CTkLabel(master=self.app, text="",fg_color="#2b2b2b",anchor="w")
        myLabel3.place(x = startX,y = y,width = adding)
        self.tableDataHeaderWidgets.append(myLabel3)

        self.tableData[0] = arr


    def onRemove(self,rowNumber):
        print(rowNumber)
        for row in self.tableDataBodyWidgets[rowNumber]:
            row.destroy()
        self.tableData[1].pop(rowNumber)
        self.updateTableBody()


    def appendEmptyRowOnTop(self):
        self.tableData[1].insert(0,["" for i in self.tableData[0]])
        self.updateTableBody()
    def saveAllToTableData(self):
        # TODO YET
        return -1
