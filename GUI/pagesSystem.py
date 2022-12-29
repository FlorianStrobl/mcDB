# Multiple Page system:
import copy
import math

class PageSystem():
    def __init__(self,table,navigatorIndicator, tableBody):
        self.tableBody = [[i,"j","b","j"] for i in range(255)]
        self.currentPage = 0
        self.table = table
        self.navigatorIndicator = navigatorIndicator
        #Constant:
        self.tableBody = tableBody
        #can always be modified
        self.givenArray = copy.copy(tableBody)


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
            sublist = arr[counter:counter+pagesRowsLength]
            arr_2d.append(sublist)
            counter += pagesRowsLength
        return arr_2d


    def onAdd(self):
        # ZIEL: alles in "givenArray" reintun in der richtiges stelle
        def insert_position(position, list1, list2):
            return list1[:position] + list2 + list1[position:]


        print("running on deleteORAd")
        abschnitt = self.table.getTablesInputs()

        pageStart = self.currentPage * 50


        #Get the distance between pageStart and pageEnd
        pageEndDistance = 0
        if(pageStart + 49 < len(self.givenArray)):
            pageEndDistance = 50
        else:
            print("be")
            pageEndDistance = len(self.givenArray) - pageStart

        pageEnd = pageStart + pageEndDistance

        #print(pageStart)
        #print("p" ,pageEnd)

        #print(len( self.givenArray))
        # Remove all 50 (or the rest) elements from the main Array at specific page
        del self.givenArray[pageStart: pageEnd]

        # Insert the new Table Input Array
        #self.givenArray.insert(pageStart-1, abschnitt)
        self.givenArray = insert_position(pageStart, self.givenArray,abschnitt )

        #rint(self.givenArray)
        # Fill the Array:



        # 1. Une row au pif est deleted
        # 2. On remanage la given Array en deletant 50 elements de la page et en in insertant 49
        # 3. On obtient la nouvelle selection
        # 4. On ajoute tout en bas la nouvelle row du dernier element de la selection du givenArray
             # --> que si c possible bien sur
        # PAS FILL - IL FAUT AJOUTER UNE ROW EN BA SI IL EN EXISTE DES PROCHAINES
        self.table.textFill(self.givenArray[pageStart:pageEnd])

        self.navigatorIndicator.configure(text= str(self.currentPage+1) +  "/" + str(math.floor(len(self.givenArray)/50)))


       # self.navigatorIndicator.configure(text= str(self.currentPage+1) +  "/" + str(len(dArray)))

    def onDelete(self, possibleParamater = None):


        print("bebe")
        # ZIEL: alles in "givenArray" reintun in der richtiges stelle
        def insert_position(position, list1, list2):
            return list1[:position] + list2 + list1[position:]


        print("running on deleteORAd")
        abschnitt = self.table.tableData[1]

        pageStart = self.currentPage * 50


        #Get the distance between pageStart and pageEnd
        pageEndDistance = 0
        if(pageStart + 49 < len(self.givenArray)):
            pageEndDistance = 50
        else:
            print("be")
            pageEndDistance = len(self.givenArray) - pageStart

        pageEnd = pageStart + pageEndDistance

        #print(pageStart)
        #print("p" ,pageEnd)

        #print(len( self.givenArray))
        # Remove all 50 (or the rest) elements from the main Array at specific page
        del self.givenArray[pageStart: pageEnd]

        # Insert the new Table Input Array
        #self.givenArray.insert(pageStart-1, abschnitt)
        self.givenArray = insert_position(pageStart, self.givenArray,abschnitt )

        #rint(self.givenArray)
        # Fill the Array:



        # 1. Une row au pif est deleted
        # 2. On remanage la given Array en deletant 50 elements de la page et en in insertant 49
        # 3. On obtient la nouvelle selection
        # 4. On ajoute tout en bas la nouvelle row du dernier element de la selection du givenArray
             # --> que si c possible bien sur
        # PAS FILL - IL FAUT AJOUTER UNE ROW EN BA SI IL EN EXISTE DES PROCHAINES
        self.table.fill(self.givenArray[pageStart:pageEnd])

        self.navigatorIndicator.configure(text= str(self.currentPage+1) +  "/" + str(len(self.convertToPages2dArray(self.givenArray))))


    def onUIReady(self):
        dArray = self.convertToPages2dArray(self.givenArray)
        self.table.fill(dArray[self.currentPage])
        self.table.addEventListener("onAddRow",self.onAdd )
        self.table.addEventListener("onDeleteRow", self.onDelete)
        self.navigatorIndicator.configure(text= str(self.currentPage+1) +  "/" + str(len(dArray)))

    def onNavigateButtonClick(self,n):
        #Saving current page
        dArray = self.convertToPages2dArray(self.givenArray)
        dArray[self.currentPage] = self.table.getTablesInputs()
        self.givenArray = self.convert2dArrayBack(dArray)

        if(n==1):
            self.currentPage = 0
        elif(n==4):
            self.currentPage = len(dArray) -1
        if(n == 2):
            if(self.currentPage == 0):
                print("Du kannst nicht weiter nach hinten!")
            else:
                self.currentPage -= 1
        elif(n==3):
            if(self.currentPage == len(dArray) -1):
                print("Du kannst nicht weiter nach vorne!")
            else:
                self.currentPage += 1
        self.table.textFill(self.convertToPages2dArray(self.givenArray)[self.currentPage])
        self.navigatorIndicator.configure(text= str(self.currentPage+1) +  "/" + str(len(dArray)))