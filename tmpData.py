import sys
sys.path.append("./Backend")
from typing import Optional, Callable, Union
from Logger import *
import SQL
from InputStrToMapFilterSort import *
import random

class TMP:
    data: list[any] = []
    tableName: str = ""
    columnNames: list[str] = []

    # return the length of data
    def length(self) -> int:
        return len(self.data)

    # return the amount of columns of the data set
    def columnLen(self) -> int:
        return len(self.columnNames)

    # None values will be replaced by the current saved value
    def setData(
        self,
        data: Optional[list],
        columnNames: Optional[list[str]] = None,
        tableName: Optional[str] = None,
    ) -> None:
        if not data is None:
            self.data = data
        else:
            self.data = []
        if not tableName is None:
            self.tableName = tableName
        if not columnNames is None:
            self.columnNames = columnNames

    def getData(self) -> list[any]:
        return self.data

    # get [tableName, columnNames]
    def getMetaData(self) -> list[str, list[str]]:
        return [self.tableName, self.columnNames]

    def deepCpyData(self) -> list[any]:
        tmp = [v for v in self.data]
        return tmp

    # return a deep cpy of all the current object
    def deepCpy(self):
        tmp = TMP()
        tmp.data = self.deepCpyData()
        tmp.columnNames = [v for v in self.columnNames]
        tmp.tableName = "".join([v for v in self.tableName])
        return tmp

    # returns a deepCpy array of the data which got filtered with the lambda
    def filterData(self, userStr: str) -> list:
        tmp = self.deepCpyData()
        arr = []
        for i in range(len(tmp)):
            ans = executeUserStr(userStr, "filter", self.columnNames, tmp[i])
            if ans is None:
                Logger.error("couldn't apply a filter:", userStr, self.columnNames, tmp[i])
                return None
            if ans:
                arr.append(tmp[i])
        return arr

    # map, filter or sort depending on the string
    def editData(self, userStr: str, mode: str = "auto") -> Union[list, None]:
        mode = getMode(userStr, mode)
        if mode == "map":
            return self.mapData(userStr)
        elif mode == "filter":
            return self.filterData(userStr)
        elif mode == "sort":
            return self.sortData(userStr)
        return None

    # returns a deepCpy array of the data edited for each element with the lambda
    def mapData(self, userStr: str) -> list:
        arr = []
        for v in self.deepCpyData():
            ans = executeUserStr(userStr, "map", self.columnNames, v)
            if ans is None:
                Logger.error("couldn't apply map to:", userStr, self.columnNames, v)
                return None
            i = self.columnNames.index(ans[0])
            # TEST: i = -1
            if i == -1:
                Logger.error("map coudln't find the column:", ans[0], self.columnNames)
                return None
            v[i] = ans[1]
            arr.append(v)
        return arr

    # returns a deepCpy array of the data sorted by the lambda function, which gets (a,b) and swaps the data if the lambda evaluates to an integer bigger than 0
    def sortData(self, userStr: str) -> list:
        def quickSort(
            arr: list, start: Optional[int] = None, end: Optional[int] = None
        ) -> None:
            def partition(arr: list, _start: int, _end: int) -> int:
                pivot = arr[_end]
                i = _start - 1
                for j in range(_start, _end):
                    ans = executeUserStr(userStr, "sort", self.columnNames, [arr[j], pivot])
                    if ans is None:
                        Logger.error("sorting failed with values:", ans, userStr, self.columnNames, [arr[j], pivot])
                        return None
                    if ans < 0:
                        i += 1
                        (arr[i], arr[j]) = (arr[j], arr[i])  # swap
                (arr[i + 1], arr[_end]) = (arr[_end], arr[i + 1])  # swap
                return i + 1

            if start is None:
                start = 0
            if end is None:
                end = len(arr) - 1

            if start < end:
                pi = partition(arr, start, end)
                quickSort(arr, start, pi - 1)
                quickSort(arr, pi + 1, end)

        # def bubbleSort(arr: list) -> None:
        #     for i in range(len(arr)):
        #         for y in range(i, len(arr)):
        #             if _lambda(arr[i], arr[y]) > 0:
        #                 (arr[i], arr[y]) = (arr[y], arr[i])

        tmp = self.deepCpyData()
        quickSort(tmp)
        # bubbleSort(tmp)
        return tmp

    def printThis(self) -> None:
        Logger.log("print tmp", self.getData())


# SQLite3: TMP -> Table
def updateDataInDB(cursor, data: TMP) -> None:
    if data.tableName is None:
        return  # no data to save

    def samePrimaryKey(
        newData: list[any],
        newDataColumns: list[str],
        realData: list[any],
        tableName: str,
    ):
        return False

    SQL.dropTable(cursor, data.tableName)
    SQL.createAllTables(cursor)
    SQL.insertIntoTable(cursor, data.tableName, data.data)

    # the current colums
    #columns = data.columnNames
    # the usuall colums of the table
    #curTableColumns = SQL.selectTableColumns(cursor, data.tableName)

    # get current data to check for each value, if it has
    # to be just updated (only the changes) or it is a new primary key => insert into
    #curTableData = SQL.selectTable(cursor, data.tableName)

    return
    # SQLite3 update or insert for each data
    for curData in curTableData:
        thisDataWasUpdated = False
        for d in data.data:
            if samePrimaryKey(d, columns, curData, data.tableName):
                # update the CHANGES (aka if there are missing columns
                # check the "columns" and

                # TODO, not ACTUALLY update the data, but delete the current row
                # (and save before removed columns) and save it completetly
                # because of the ordering
                thisDataWasUpdate = True
        if thisDataWasUpdate == False:
            # could error because of missing or added columns
            SQL.insertIntoTable(cursor, data.tableName, data.data)
