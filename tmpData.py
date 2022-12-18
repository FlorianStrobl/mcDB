from numpy import *
from typing import Union, Optional


class TMP:
    data: list = []
    tableName: str = ""
    columnNames: list[str] = []

    def length(self) -> int:
        return len(self.data)

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
        if not tableName is None:
            self.tableName = tableName
        if not columnNames is None:
            self.columnNames = columnNames

    def getData(self) -> list:
        return self.data

    def getMetaData(self) -> list[str, list[str]]:
        return [self.tableName, self.columnNames]

    def deepCpyData(self):
        tmp = []
        for v in self.data:
            tmp.append(v)
        return tmp

    def filterData(self, _lambda) -> list:
        tmp = self.deepCpyData()
        arr = []
        for i in range(len(tmp)):
            if _lambda(tmp[i]):
                arr.append(tmp[i])
        return arr

    def mapData(self, _lambda) -> list:
        arr = self.deepCpyData()
        for i in range(len(arr)):
            arr[i] = _lambda(arr[i])
        return arr

    def sortData(self, _lambda) -> list:
        def quickSort(arr: list, start: Optional[int] = None, end: Optional[int] = None) -> None:
            def partition(arr: list, _start: int, _end: int) -> int:
                pivot = arr[_end]
                i = _start-1
                for j in range(_start, _end):
                    if _lambda(arr[j], pivot) < 0:
                        i += 1
                        (arr[i], arr[j]) = (arr[j], arr[i]) # swap
                (arr[i+1], arr[_end]) = (arr[_end], arr[i+1]) # swap
                return i+1

            if start is None:
                start = 0
            if end is None:
                end = len(arr)-1

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
        #bubbleSort(tmp)
        return tmp

    def printThis(self) -> None:
        print(self.getData())
