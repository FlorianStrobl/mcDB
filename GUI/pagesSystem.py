# Multiple Page system:
import copy
import math
import addImport
import Logger
import customtkinter


class PageSystem:
    def __init__(self, table, navigatorIndicator, tableBody):
        self.tableBody = [[i, "j", "b", "j"] for i in range(255)]
        self.currentPage = 0
        self.table = table
        self.navigatorIndicator = navigatorIndicator
        # Constant:
        self.tableBody = tableBody
        # can always be modified
        self.givenArray = copy.copy(tableBody)

        self.tableState = customtkinter.NORMAL

    @staticmethod
    def convert2dArrayBack(arr_2d):
        arr = []
        for sublist in arr_2d:
            arr.extend(sublist)
        return arr

    @staticmethod
    def convertToPages2dArray(arr, pagesRowsLength=50):
        arr_2d = []
        counter = 0
        while counter < len(arr):
            sublist = arr[counter : counter + pagesRowsLength]
            arr_2d.append(sublist)
            counter += pagesRowsLength
        return arr_2d

    def onAdd(self):
        if len(self.givenArray) == 0:
            self.__init__(
                self.table,
                self.navigatorIndicator,
                ["" for i in self.table.tableData[0]],
            )
        else:
            # ZIEL: alles in "givenArray" reintun in der richtiges stelle
            def insert_position(position, list1, list2):
                return list1[:position] + list2 + list1[position:]

            abschnitt = self.table.getTablesInputs()

            pageStart = self.currentPage * 50

            # Get the distance between pageStart and pageEnd
            pageEndDistance = 0
            if pageStart + 49 < len(self.givenArray):
                pageEndDistance = 50
            else:
                pageEndDistance = (len(self.givenArray) - pageStart) + 1
            pageEnd = pageStart + pageEndDistance

            # Remove all 50 (or the rest) elements from the main Array at specific page
            del self.givenArray[pageStart:pageEnd]

            # Insert the new Table Input Array
            # self.givenArray.insert(pageStart-1, abschnitt)
            self.givenArray = insert_position(pageStart, self.givenArray, abschnitt)

            # Fill the Array:

            # LE MIEU C DE PAS FAIRE DE FILL
            # 1. Une row au pif est deleted
            # 2. On remanage la given Array en deletant 50 elements de la page et en in insertant 49
            # 3. On obtient la nouvelle selection
            # 4. On ajoute tout en bas la nouvelle row du dernier element de la selection du givenArray
            # --> que si c possible bien sur
            # PAS FILL - IL FAUT AJOUTER UNE ROW EN BA SI IL EN EXISTE DES PROCHAINES
            self.table.textFill(self.givenArray[pageStart:pageEnd])

            self.navigatorIndicator.configure(
                text=str(self.currentPage + 1)
                + "/"
                + str(len(self.convertToPages2dArray(self.givenArray)))
            )

            self.table.setState(self.tableState)

    # self.navigatorIndicator.configure(text= str(self.currentPage+1) +  "/" + str(len(dArray)))

    def onDelete(self, possibleParamater=None):

        # ZIEL: alles in "givenArray" reintun in der richtiges stelle
        def insert_position(position, list1, list2):
            return list1[:position] + list2 + list1[position:]

        abschnitt = self.table.getTablesInputs()

        pageStart = self.currentPage * 50

        # Get the distance between pageStart and pageEnd
        pageEndDistance = 0
        if pageStart + 49 < len(self.givenArray):
            pageEndDistance = 50
        else:
            pageEndDistance = (len(self.givenArray) - pageStart) + 1

        pageEnd = pageStart + pageEndDistance

        # Remove all 50 (or the rest) elements from the main Array at specific page
        del self.givenArray[pageStart:pageEnd]

        # Insert the new Table Input Array
        # self.givenArray.insert(pageStart-1, abschnitt)
        self.givenArray = insert_position(pageStart, self.givenArray, abschnitt)

        # rint(self.givenArray)
        # Fill the Array:

        # 1. Une row au pif est deleted
        # 2. On remanage la given Array en deletant 50 elements de la page et en in insertant 49
        # 3. On obtient la nouvelle selection
        # 4. On ajoute tout en bas la nouvelle row du dernier element de la selection du givenArray
        # --> que si c possible bien sur
        # PAS FILL - IL FAUT AJOUTER UNE ROW EN BA SI IL EN EXISTE DES PROCHAINES

        # Automatisches ändern der pages wenn eine page leer ist wenn es noch andere pages gibt
        if len(self.givenArray[pageStart:pageEnd]) == 0 and len(self.givenArray) != 0:
            self.table.fill(self.givenArray[pageStart - 50 :])
            self.currentPage -= 1
            self.navigatorIndicator.configure(
                text=str(self.currentPage + 1)
                + "/"
                + str(len(self.convertToPages2dArray(self.givenArray)))
            )
            return
        self.table.fill(self.givenArray[pageStart:pageEnd])

        self.navigatorIndicator.configure(
            text=str(self.currentPage + 1)
            + "/"
            + str(
                len(self.convertToPages2dArray(self.givenArray))
                if len(self.givenArray) != 0
                else 1
            )
        )

        self.table.setState(self.tableState)

    def setTableState(self, _state):
        if(_state == self.tableState):
            return

        self.tableState = _state
        self.table.setState(_state)

    def changeTableBody(self, tableBody):
        self.table.setState(customtkinter.NORMAL)
        self.currentPage = 0
        self.tableBody = tableBody
        self.givenArray = copy.copy(tableBody)
        dArray = self.convertToPages2dArray(self.givenArray)

        if len(tableBody) == 0:
            self.table.fill([])
            self.givenArray = []
            self.navigatorIndicator.configure("1" + "/" + "1")

            return


        try:
            self.table.fill(dArray[self.currentPage])
            self.navigatorIndicator.configure(
                text=str(self.currentPage + 1) + "/" + str(len(dArray))
            )
        except:
            print("except case")
            self.table.fill(self.givenArray)
            self.navigatorIndicator.configure(
                text=str(self.currentPage + 1) + "/" + str(len(dArray))
            )
        self.table.setState(self.tableState)

    def onUIReady(self):
        dArray = self.convertToPages2dArray(self.givenArray)
        if len(dArray) != 0:
            self.table.fill(dArray[self.currentPage])

        self.table.addEventListener("onAddRow", self.onAdd)
        self.table.addEventListener("onDeleteRow", self.onDelete)
        self.navigatorIndicator.configure(
            text=str(self.currentPage + 1) + "/" + str(len(dArray))
        )

    def getInput(self):
        self.onDelete()
        return self.givenArray

    def onNavigateButtonClick(self, n):
        # Saving current page
        dArray = self.convertToPages2dArray(self.givenArray)
        dArray[self.currentPage] = self.table.getTablesInputs()
        self.givenArray = self.convert2dArrayBack(dArray)
        self.table.scrollFrame.canvas.yview_moveto(0)
        # self.table.scrollFrame.vsb.set(0.0,1.0)
        # self.table.scrollFrame.disableScroll()

        if n == 1:
            self.currentPage = 0
        elif n == 4:
            self.currentPage = len(dArray) - 1
        if n == 2:
            if self.currentPage == 0:
                Logger.Logger.warn("Du kannst nicht weiter nach hinten!")
            else:
                self.currentPage -= 1
        elif n == 3:
            if self.currentPage == len(dArray) - 1:
                Logger.Logger.warn("Du kannst nicht weiter nach vorne!")
            else:
                self.currentPage += 1

        #print(self.convertToPages2dArray(self.givenArray)[self.currentPage])
        #print(self.convertToPages2dArray(self.givenArray)[self.currentPage])

        tableStateBefore = self.tableState
        self.setTableState(customtkinter.NORMAL)

        self.table.textFill(
            self.convertToPages2dArray(self.givenArray)[self.currentPage]
        )


        print(self.currentPage)
        self.navigatorIndicator.configure(
            text=str(self.currentPage + 1) + "/" + str(len(dArray))
        )


        self.setTableState(tableStateBefore)
