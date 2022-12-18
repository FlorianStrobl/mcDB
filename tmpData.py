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

    def filterData(self, _lambda) -> list:
        tmp = array(self.data)
        # TODO, filter the data out
        return tmp

    def mapData(self, _lambda) -> list:
        tmp = array(self.data)
        # TODO, execute the lambda for each row
        return tmp

    def printThis(self) -> None:
        print(self.getData())
