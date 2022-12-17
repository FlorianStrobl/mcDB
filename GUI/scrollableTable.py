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


class scrollableTable(customtkinter.CTkFrame):
    def __init__(self, app,widthFrame):
        customtkinter.CTkFrame.__init__(self, app)
        self.scrollFrame = ScrollFrame(self)
        self.widthFrame = widthFrame
        self.scrollFrame.pack(side="top", fill="both", expand=True)
        self.currentEntrys = []
        self.app = app

    def fill(self,tableData):
        widthCurrentFrame = self.widthFrame-20
        numberColumns = len(tableData[0])
        numberRows = len(tableData)
        for row in range(numberRows):
            for col in range(numberColumns):
                myEntry = customtkinter.CTkEntry(self.scrollFrame.viewPort,corner_radius=0,width=widthCurrentFrame/numberColumns)
                myEntry.grid(row=row, column=col)
                myEntry.insert(0, tableData[row][col])


    def printMsg(self, msg):
        print(msg)