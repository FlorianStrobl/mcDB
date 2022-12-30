import random
from typing import Optional, Callable, Union
from Logger import *
import sys

sys.path.append("./Backend")

import SQL
from InputStrToMapFilterSort import *

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
                Logger.error(
                    "couldn't apply a filter:", userStr, self.columnNames, tmp[i]
                )
                return None
            if ans:
                arr.append(tmp[i])
        return arr

    # map, filter or sort depending on the string
    def editData(
        self,
        userStr: str,
        mode: Optional[Literal["auto", "filter", "map", "sort"]] = None,
    ) -> Optional[list]:
        curVals = self.deepCpy()
        cmds = userStr.split("&&")  # get all the different cmds
        originalMode = mode
        for cmd in cmds:
            cmd = cmd.strip()
            if (
                originalMode is None or originalMode == "auto"
            ):  # a chain of xy should always be xy
                mode = getMode(cmd)
            if mode == "map":
                curVals.data = TMP.mapData(curVals, cmd)
            elif mode == "filter":
                curVals.data = TMP.filterData(curVals, cmd)
            elif mode == "sort":
                curVals.data = TMP.sortData(curVals, cmd)

        return curVals.data

    # returns a deepCpy array of the data edited for each element with the lambda
    def mapData(self, userStr: str) -> list:
        arr = []
        for v in self.deepCpyData():
            ans = executeUserStr(userStr, "map", self.columnNames, v)
            # TODO, ans could be multiple different columns!!
            if ans is None:
                Logger.error("couldn't apply map to:", userStr, self.columnNames, v)
                return None

            # check if there are multiple columns
            if ans[0] == "multi":
                print(ans[2])
                indexes = []
                for i,vv in enumerate(ans[1]):
                    try:
                        indexes.append(self.columnNames.index(ans[1][i]))
                    except:
                        Logger.error("map coudln't find the column:", ans[1][i], self.columnNames)
                        return None
                    tmpNewDataIndex = 0
                    for i in indexes:
                        v[i] = ans[2][tmpNewDataIndex]
                        tmpNewDataIndex += 1
                    arr.append(v)
            else:
                try:
                    i = self.columnNames.index(ans[0])
                except:
                    Logger.error("map coudln't find the column:", ans[0], self.columnNames)
                    return None
                v[i] = ans[1]
                arr.append(v)
        return arr

    def __quickSort__(self, arr: list, userStr: str) -> Optional[list]:
        # https://www.geeksforgeeks.org/stable-quicksort/
        if len(arr) <= 1:
            # Base case
            return arr
        else:
            mid = len(arr) // 2
            pivot = arr[mid]

            smaller, greater = [], []

            for index, value in enumerate(arr):
                if index != mid:
                    ans = executeUserStr(
                        userStr, "sort", self.columnNames, [value, pivot]
                    )
                    if ans is None:
                        Logger.error(
                            "sorting failed with values:",
                            ans,
                            userStr,
                            self.columnNames,
                            [value, pivot],
                        )
                        return None
                    if ans < 0:
                        smaller.append(value)
                    elif ans > 0:
                        greater.append(value)
                    else:  # consider position to decide the list
                        if index < mid:
                            smaller.append(value)
                        else:
                            greater.append(value)
            return (
                self.__quickSort__(smaller, userStr)
                + [pivot]
                + self.__quickSort__(greater, userStr)
            )

    # returns a deepCpy array of the data sorted by the lambda function, which gets (a,b) and swaps the data if the lambda evaluates to an integer bigger than 0
    def sortData(self, userStr: str) -> list:
        # unstable quicksort
        def quickSort(
            arr: list, start: Optional[int] = None, end: Optional[int] = None
        ) -> None:
            def partition(arr: list, _start: int, _end: int) -> int:
                pivot = arr[_end]
                i = _start - 1
                for j in range(_start, _end):
                    ans = executeUserStr(
                        userStr, "sort", self.columnNames, [arr[j], pivot]
                    )
                    if ans is None:
                        Logger.error(
                            "sorting failed with values:",
                            ans,
                            userStr,
                            self.columnNames,
                            [arr[j], pivot],
                        )
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

        # tmp = self.deepCpyData()
        # quickSort(tmp)
        # return tmp
        return self.__quickSort__(self.deepCpyData(), userStr)

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
    SQL.createAllTables(cursor)  # if not exists in SQLite exists
    SQL.insertIntoTable(cursor, data.tableName, data.data)

    return
