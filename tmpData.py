import sys
sys.path.append('./Backend')

from typing import Optional, Callable, Union
from Logger import *
import SQL


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

    def getData(self) -> list:
        return self.data

    # get [tableName, columnNames]
    def getMetaData(self) -> list[str, list[str]]:
        return [self.tableName, self.columnNames]

    def deepCpyData(self):
        tmp = [v for v in self.data]
        return tmp

    # returns a deepCpy array of the data which got filtered with the lambda
    def filterData(self, _lambda: Callable[[any], bool]) -> list:
        tmp = self.deepCpyData()
        arr = []
        for i in range(len(tmp)):
            if _lambda(tmp[i]):
                arr.append(tmp[i])
        return arr

    # returns a deepCpy array of the data edited for each element with the lambda
    def mapData(self, _lambda: Callable[[any], any]) -> list:
        arr = [_lambda(v) for v in self.deepCpyData()]
        return arr

    # returns a deepCpy array of the data sorted by the lambda function, which gets (a,b) and swaps the data if the lambda evaluates to an integer bigger than 0
    def sortData(self, _lambda: Callable[[any, any], int]) -> list:
        def quickSort(
            arr: list, start: Optional[int] = None, end: Optional[int] = None
        ) -> None:
            def partition(arr: list, _start: int, _end: int) -> int:
                pivot = arr[_end]
                i = _start - 1
                for j in range(_start, _end):
                    if _lambda(arr[j], pivot) < 0:
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

        def bubbleSort(arr: list) -> None:
            for i in range(len(arr)):
                for y in range(i, len(arr)):
                    if _lambda(arr[i], arr[y]) > 0:
                        (arr[i], arr[y]) = (arr[y], arr[i])

        tmp = self.deepCpyData()
        quickSort(tmp)
        # bubbleSort(tmp)
        return tmp

    def printThis(self) -> None:
        Logger.log(self.getData())

# SQLite3: TMP -> Table
def updateDataInDB(cursor, data: TMP) -> None:
    if data.tableName is None:
        return # no data to save

    columns = data.columnNames

    # SQLite3 update and insert
    # get current data to check if it has to be updated or inserted new
    #curData = SQL.selectTable(cursor, data.tableName)
    #curDataColumns = SQL.selectTableColumns(cursor, data.tableName)
    SQL.insertIntoTable(cursor, data.tableName, data.data)