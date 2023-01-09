# Multiple Page system:
import copy
import math
import addImport
import Logger
import customtkinter

# Klasse mit der man kommunizieren kann, wenn man eine Table anzeigen will die mit Seiten funktionniert
class PageSystem:

    # Gegeben muss folgendes sein: eine Instanz der table "Klasse", das Widget mit dem man die "currentSeite"
    # anzeigen kann kann und die Datensätze der Table
    # Die columns names natürlich nicht weil sie nichts mit einem pagesystem zu tun haben
    def __init__(self, table, navigatorIndicator, tableBody):
        # Default daten:
        self.tableBody = [[i, "j", "b", "j"] for i in range(1)]
        # Aktuelle Seite
        self.currentPage = 0

        self.table = table
        self.navigatorIndicator = navigatorIndicator
        self.tableBody = tableBody
        # can always be modified
        self.givenArray = copy.copy(tableBody)

        self.tableState = customtkinter.NORMAL

    # Static methode weil sie ohne save funktionniert
    @staticmethod
    # Konvertiert den page array zurück indem alle inhalte von den jeweiligen subarrays von "arr_2d" in einem Array zusammengsetzt werden.
    # z.B: [a,b][c]-> [a,b,c]
    def convert2dArrayBack(arr_2d):
        arr = []
        for sublist in arr_2d:
            arr.extend(sublist)
        return arr

    # Static methode weil sie ohne save funktionniert
    @staticmethod
    # Konvertiert einen Array zu einen Array mit mehreren unterArrays die jeweils die länge "pagesRowsLength" (oder an der letzten stelle der unterArray's weniger) haben.
    # beispiel mit pagesRowsLength=2    input: [a,b,c,d,e] output: [a,b][c,d][e]
    def convertToPages2dArray(arr, pagesRowsLength=50):
        arr_2d = []
        counter = 0
        while counter < len(arr):
            sublist = arr[counter : counter + pagesRowsLength]
            arr_2d.append(sublist)
            counter += pagesRowsLength
        return arr_2d

    # wird ausgeführt wenn was in der table etwas hinzugefügt wurde
    def onAdd(self):
        # Was ist das Ziel?
        # Das Ziel ist hier, den Datensatz der hinzugefügt wurde richtig in dem ""givenArray" zu kopieren


        if len(self.givenArray) == 0:
            self.__init__(
                self.table,
                self.navigatorIndicator,
                ["" for i in self.table.tableData[0]],
            )
        else:

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


            self.table.textFill(self.givenArray[pageStart:pageEnd])

            self.navigatorIndicator.configure(
                text=str(self.currentPage + 1)
                + "/"
                + str(len(self.convertToPages2dArray(self.givenArray)))
            )

            self.table.setState(self.tableState)

    # self.navigatorIndicator.configure(text= str(self.currentPage+1) +  "/" + str(len(dArray)))

    # wird ausgeführt wenn was in der table gelöscht wurde
    def onDelete(self, possibleParamater=None):
        # Was ist das Ziel?
        # Das Ziel ist hier, den Datensatz der hinzugefügt wurde richtig in dem ""givenArray" zu kopieren

        # Insertet list2 ab der stelle: "position" in list1 und returnt dies
        def insert_position(position, list1, list2):
            return list1[:position] + list2 + list1[position:]

        abschnitt = self.table.getTablesInputs()

        pageStart = self.currentPage * 50

        # Abstand zwischen pageStart und pageEnd zu bekommen
        pageEndDistance = 0
        if pageStart + 49 < len(self.givenArray):
            pageEndDistance = 50
        else:
            pageEndDistance = (len(self.givenArray) - pageStart) + 1

        pageEnd = pageStart + pageEndDistance

        # Alle Datensätze von der aktuellen page löschen
        del self.givenArray[pageStart:pageEnd]

        # Insert the new Table Input Array
        # self.givenArray.insert(pageStart-1, abschnitt)
        self.givenArray = insert_position(pageStart, self.givenArray, abschnitt)

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

        # Aktuelle page visualisierung wird geupdated
        self.navigatorIndicator.configure(
            text=str(self.currentPage + 1)
            + "/"
            + str(
                len(self.convertToPages2dArray(self.givenArray))
                if len(self.givenArray) != 0
                else 1
            )
        )

        # Aktualisiert den tableState status auf die table
        self.table.setState(self.tableState)

    # Setzt einen tableState (wurde in "scrollableTable" erklärt ) für alle Seiten
    def setTableState(self, _state):
        if _state == self.tableState:
            return

        self.tableState = _state
        self.table.setState(_state)

    #Ändert den Inhalt des tableAnzeige
    def changeTableBody(self, tableBody):
        for i in range(len(tableBody)):
            for y in range(len(tableBody[i])):
                # Wenn ein Wert in der tableBody None ist, wird er zu "null" geändert
                # damit auf ALLEN Seiten der tableBody den Wert "null" haben
                # und nicht nur die erste durch einmalige ausführung
                if tableBody[i][y] == None:
                    tableBody[i][y] = "null"

        # Leider kann man nicht mit eine table interagieren, wenn der tableState auf DISABLED ist
        # --> Deswegen muss man diesen hier sicherheitshalber aktualisieren
        self.table.setState(customtkinter.NORMAL)


        self.currentPage = 0
        self.tableBody = tableBody
        self.givenArray = copy.copy(tableBody)

        # Array mit subarrys die jeweils die Seiten Datensätze beinhalten
        dArray = self.convertToPages2dArray(self.givenArray)

        if len(tableBody) == 0:
            self.table.fill([])
            self.givenArray = []
            self.navigatorIndicator.configure("1" + "/" + "1")

            return

        # Aktualisieren der pages labels
        try:
            self.table.fill(dArray[self.currentPage])
            self.navigatorIndicator.configure(
                text=str(self.currentPage + 1) + "/" + str(len(dArray))
            )
        except:
            self.table.fill(self.givenArray)
            self.navigatorIndicator.configure(
                text=str(self.currentPage + 1) + "/" + str(len(dArray))
            )

        # State wird aktualisiert
        self.table.setState(self.tableState)

    # Wird aufgerunfen wenn die GUI bereit ist
    def onUIReady(self):
        dArray = self.convertToPages2dArray(self.givenArray)
        if len(dArray) != 0:
            self.table.fill(dArray[self.currentPage])

        # OnAdd wird jetzt ausgeführt wenn eine row appended wird
        self.table.addEventListener("onAddRow", self.onAdd)

        # OnAdd wird jetzt ausgeführt wenn eine row appended wird
        self.table.addEventListener("onDeleteRow", self.onDelete)
        self.navigatorIndicator.configure(
            text=str(self.currentPage + 1) + "/" + str(len(dArray))
        )

    # Liefert einen Array mit allen Daten von der dementsprechenen Tabelle
    def getInput(self):
        # Damit nochmal alles richtig aktualisiert wird bevor was returnt wird
        self.onDelete()
        return self.givenArray

    # Wird ausgeführt wenn auf einer Pfeiltaste geklickt wurde
    def onNavigateButtonClick(self, n):
        # Saving current page
        dArray = self.convertToPages2dArray(self.givenArray)
        dArray[self.currentPage] = self.table.getTablesInputs()
        self.givenArray = self.convert2dArrayBack(dArray)

        # Ganz nach oben scollen
        self.table.scrollFrame.canvas.yview_moveto(0)

        # << wenn n 1 ist
        # < wenn n 2 ist
        # > wenn n 3 ist
        # >> wenn n 4 ist

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

        tableStateBefore = self.tableState
        self.setTableState(customtkinter.NORMAL)

        # Text wird auf der dementsprechenden Seite gefillt
        self.table.textFill(
            self.convertToPages2dArray(self.givenArray)[self.currentPage]
        )

        # Seiten Label wird aktualisiert
        self.navigatorIndicator.configure(
            text=str(self.currentPage + 1) + "/" + str(len(dArray))
        )

        self.setTableState(tableStateBefore)
