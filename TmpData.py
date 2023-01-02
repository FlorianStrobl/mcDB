from __future__ import annotations
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

    def replaceTmp(self, newTmp: Optional[TMP]) -> None:
        if newTmp is None:
            Logger.error(
                "Couldn't update temporary data. probably because a command failed before."
            )
            return
        self.data = newTmp.deepCpyData()
        self.columnNames = newTmp.columnNames[:]
        self.tableName = newTmp.tableName

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
        return [self.tableName, self.columnNames[:]]

    def deepCpyData(self) -> list[any]:
        d = []
        for v in self.data:
            d.append(v[:])
        return d

    # return a deep cpy of all the current object
    def deepCpy(self):
        t = TMP()
        t.data = self.deepCpyData()
        t.columnNames = self.columnNames[:]
        t.tableName = "".join([v for v in self.tableName])
        return t

    # map, filter, sort, slice or columns depending on the string
    def editData(
        self,
        userStr: str,
        mode: Optional[
            Literal["auto", "filter", "map", "sort", "slice", "columns"]
        ] = None,
    ) -> Optional[TMP]:
        curVals = self.deepCpy()
        # TODO what about "&&"
        cmds = userStr.split("&&")  # get all the different cmds
        originalMode = mode
        for cmd in cmds:
            cmd = cmd.strip()
            if (
                originalMode is None or originalMode == "auto"
            ):  # a chain of xy should always be xy
                mode = getMode(cmd)
            if mode == "map":
                v = TMP.mapData(curVals, cmd)
                if v is None:
                    return None
                curVals.data = v
            elif mode == "filter":
                v = TMP.filterData(curVals, cmd)
                if v is None:
                    return None
                curVals.data = v
            elif mode == "sort":
                v = TMP.sortData(curVals, cmd)
                if v is None:
                    return None
                curVals.data = v
            elif mode == "slice":
                v = TMP.sliceData(curVals, cmd)
                if v is None:
                    # no error message because it is handled before
                    return None
                curVals.data = v
            elif mode == "columns":
                v = TMP.selectColumns(curVals, cmd)
                if v is None:
                    Logger.error(
                        "couldn't execute the select column with the command:", cmd
                    )  # error message because it isnt handled before
                    return None
                curVals.columnNames = v[0]  # change also the column names
                curVals.data = [[] for _ in v[1][0]]
                for i in range(len(v[1])):
                    for idx, val in enumerate(v[1][i]):
                        curVals.data[idx].append(val)  # add them in correct order
        return curVals

    # returns a deepCpy array of the data which got filtered with the lambda
    def filterData(self, userStr: str) -> Optional[list]:
        tmp = self.deepCpyData()
        arr = []
        for i in range(len(tmp)):
            ans = executeUserStr(userStr, "filter", self.columnNames, tmp[i], i)
            if ans is None:
                Logger.error(
                    "couldn't apply a filter:", userStr, self.columnNames, tmp[i]
                )
                return None
            if ans:
                arr.append(tmp[i])
        return arr

    # returns a deepCpy array of the data edited for each element with the lambda
    def mapData(self, userStr: str) -> Optional[list]:
        arr = []
        for i, v in enumerate(self.deepCpyData()):
            ans = executeUserStr(userStr, "map", self.columnNames, v, i)
            # TODO, ans could be multiple different columns!!
            if ans is None:
                Logger.error("couldn't apply map to:", userStr, self.columnNames, v)
                return None

            # check if there are multiple columns
            if ans[0] == "multi":
                indexes = []
                for i, vv in enumerate(ans[1]):
                    try:
                        indexes.append(self.columnNames.index(ans[1][i]))
                    except:
                        Logger.error(
                            "map coudln't find the column:", ans[1][i], self.columnNames
                        )
                        return None

                for i, vv in enumerate(indexes):
                    v[vv] = ans[2][i]
                arr.append(v)
            else:
                try:
                    i = self.columnNames.index(ans[0])
                except:
                    Logger.error(
                        "map coudln't find the column:", ans[0], self.columnNames
                    )
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
                        userStr, "sort", self.columnNames, [value, pivot], mid, index
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
    def sortData(self, userStr: str) -> Optional[list]:
        # def bubbleSort(arr: list) -> None:
        #     for i in range(len(arr)):
        #         for y in range(i, len(arr)):
        #             if _lambda(arr[i], arr[y]) > 0:
        #                 (arr[i], arr[y]) = (arr[y], arr[i])

        # tmp = self.deepCpyData()
        # quickSort(tmp)
        # return tmp

        return self.__quickSort__(self.deepCpyData(), userStr)

    # returns the columns of the current data in the order provided by the userStr. e.g.: "columnName2,columnName1"
    def selectColumns(self, userStr: str) -> Optional[list[list[str], list[any]]]:
        def _2DArrayGetColumn(idx: int, arr: list[list]) -> list:
            return [v[idx] for v in arr]

        oldData = self.deepCpyData()

        MAX_INT = 9007199254740991
        toSaveColumns = [
            x
            for x in userStr.strip()  # format str for simpler use
            .replace(" ", "", MAX_INT)
            .replace("\t", "", MAX_INT)
            .replace("\n", "", MAX_INT)
            .split(",")
            if x != ""
        ]

        # check if some column doesnt exist
        for cn in toSaveColumns:
            try:
                _ = self.columnNames.index(cn)
            except:
                Logger.error(
                    f"select columns failed because the column {cn} does not exist in:",
                    self.columnNames,
                )
                return None

        # get indexes to keep
        newColumnIndexes = []
        for c in toSaveColumns:
            newColumnIndexes.append(self.columnNames.index(c))

        # save them in order into the newDataInOrder var
        newDataInOrder = [_2DArrayGetColumn(c, oldData) for c in newColumnIndexes]

        return [toSaveColumns, newDataInOrder]

    def sliceData(self, userStr: str) -> Optional[list]:
        return executeUserStr(userStr, "slice", self.columnNames, self.deepCpyData(), 0)

    def printThis(self) -> None:
        Logger.log("print tmp", self.getData())


# SQLite3: TMP -> Table
def updateDataInDB(cursor, data: TMP) -> None:
    def reorderArr(array, orderArray):
        array = array[:]
        newArray = [None for x in orderArray]
        for i in orderArray:
            newArray[i] = array.pop(0)
        return newArray

    if data.tableName is None:
        return  # no table for data to save

    if data.columnNames is None:
        Logger.error(
            f"No column names provided to save table {data.tableName} to database"
        )
        return

    if data.data is None:
        Logger.error(f"No data provided to save table {data.tableName} to database")
        return

    # check if column names are like the original ones
    originalColumns = SQL.selectTableColumns(cursor, data.tableName)

    errStr = (
        "Couldn't save data to database because the columns are not the ones expected:"
    )

    # check if they have the same length
    if len(data.columnNames) != len(originalColumns):
        Logger.error(errStr, data.columnNames, originalColumns)
        return

    # check if they have the same exact values
    for c in originalColumns:
        if not c in data.columnNames:
            Logger.error(errStr, data.columnNames, originalColumns)
            return

    # TODO, it could be that the vars are in swapped order
    if data.columnNames != originalColumns:
        # TODO swap, should it also swap it in the UI, or just in the database?
        print("SWAP TODO (in: TmpData.py)")
        # get order
        orderArr = []
        for i in range(len(data.columnNames)):
            orderArr.append(originalColumns.index(data.columnNames[i]))
        # reorder the data
        for i in range(len(data.data)):
            data.data[i] = reorderArr(data.data[i], orderArr)
        data.columnNames = reorderArr(data.columnNames, orderArr)

    # backup in case the saving of new data fails => invalid new data
    backupOldData = SQL.selectTable(cursor, data.tableName)

    SQL.dropTable(cursor, data.tableName)  # delete all existing datas
    SQL.createAllTables(cursor)  # if not exists in SQLite exists

    try:
        SQL.insertIntoTable(cursor, data.tableName, data.data)  # save all the new datas
    except:
        # revert to the old, known good, values
        SQL.dropTable(cursor, data.tableName)
        SQL.createAllTables(cursor)
        SQL.insertIntoTable(cursor, data.tableName, backupOldData)
    return
