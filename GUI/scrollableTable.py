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
    def __init__(self, app,x,y,width,height):
        customtkinter.CTkFrame.__init__(self, app)
        self.scrollFrame = ScrollFrame(self)

        self.scrollFrame.pack(side="top", fill="both", expand=True)
        self.currentEntrys = []
        self.app = app
        self.colors = ["#343638","#2d2f31"]
        self.actionColumnWidth = 25

        self.x = x
        self.y = y
        self.widthFrame = width
        self.heightFrame = height

        #h:300; w:500 200 75
        self.place(x = self.x,y = self.y, width = self.widthFrame,height = self.heightFrame)

    def fill(self,tableData):
        #tableData.append((1,2))
        #tableData.insert(0,(("","")))
        widthCurrentFrame = self.widthFrame-20
        numberColumns = len(tableData[0])

        numberRows = len(tableData)
        colorIndex = 0
        for row in range(numberRows):
            for col in range(numberColumns+1):
                if(col < numberColumns):
                    myEntry = customtkinter.CTkEntry(self.scrollFrame.viewPort,corner_radius=0,width=(widthCurrentFrame - self.actionColumnWidth)/numberColumns,fg_color=self.colors[colorIndex % 2])
                    myEntry.grid(row=row, column=col)
                    try:
                        myEntry.insert(0, tableData[row][col])
                    except:
                        myEntry.insert(0, "Data not found")
                else:
                    myEntry = customtkinter.CTkButton(self.scrollFrame.viewPort,text="🗑",  corner_radius=0,width=self.actionColumnWidth,fg_color=self.colors[colorIndex % 2])
                    myEntry.grid(row=row, column=col)

            colorIndex += 1

    def setTableHeader(self,arr,startX,y,fillstart=None,fillstartLength = None,adding = 0):
        acL = self.actionColumnWidth
        if(fillstart != None and fillstartLength != None):
            customtkinter.CTkLabel(master=self.app, text="",font=("Helvetica",15,"bold"),fg_color="#2b2b2b",anchor="w").place(x = fillstart,y = y,width = fillstartLength)



        self.scrollFrame.update()
        print(self.scrollFrame.getPos())
        for i in range(len(arr)):
            subWidth = (self.widthFrame-20 -acL)/len(arr)
            customtkinter.CTkLabel(master=self.app, text=arr[i],font=("Helvetica",15,"bold"),fg_color="#2b2b2b",anchor="w").place(x = startX,y = y,width = subWidth)
            startX += subWidth
        customtkinter.CTkLabel(master=self.app, text="",fg_color="#2b2b2b",anchor="w").place(x = startX,y = y,width = acL)
        startX+=acL-3
        customtkinter.CTkLabel(master=self.app, text="",fg_color="#2b2b2b",anchor="w").place(x = startX,y = y,width = adding)
    def printMsg(self, msg):
        print(msg)