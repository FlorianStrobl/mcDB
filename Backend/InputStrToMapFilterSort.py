import re
import random
import numpy
import math
from typing import Union, Literal
import addImport
from Logger import *


def getMode(
    string: str, mode: Literal["auto", "filter", "map", "sort"] = "auto"
) -> str:
    string = string.strip()
    if mode == "auto":
        # try getting the current mode
        if (
            re.search("^( *)?[A-Za-z_][A-Za-z0-9_]* *<-.+ *", string) is not None
            or re.search("^( *)?\([A-Za-z_0-9, ]*\) *<-.+ *", string) is not None
        ):
            # match identifier <- ANY
            # or match (any symbol out of [A-Za-z_0-9, ]) <- Any
            mode = "map"
        elif re.search("^.*[a-zA-Z_][a-zA-Z0-9_]*(1|2)(.|\n)*$", string) is not None:
            # match ANY test1|2 ANY
            # TODO, could be "test1" inside the str
            mode = "sort"
        else:
            # couldn't find anything else so it must be filter
            mode = "filter"
    return mode


# mode: ["auto", "filter", "map", "sort"], TODO add func return type
def executeUserStr(
    string: str,
    mode: Literal["auto", "filter", "map", "sort"] = "auto",
    columns: list[str] = [],
    data: list[any] = [],
) -> Union[None, int, bool, any]:
    mode = getMode(string, mode)  # mode stays the same if it was already set

    vals = {"random": random, "math": math, "numpy": numpy}
    if mode == "map":
        # create a lambda with the signature: Callable[[any], bool]
        code = re.split("<-", string, 1)  # split on first occurence
        if len(code) == 0 or len(code) == 1:
            Logger.error("couldn't parse the map expression:", string)
            return None

        code[0] = code[0].strip()
        # TODO, what if (val,,,) <- 4
        mustStartWithIdentifier = code[0][0] != "("
        isWrappedIdentifier = [v.strip() for v in code[0][1:-1].split(",") if v.strip() != ""]
        isWrappedIdentifier = len(isWrappedIdentifier) == 1
        # if exactly one
        if mustStartWithIdentifier or isWrappedIdentifier:
            toUpdateColumn = code[0]  # get the current column to do
            code = code[1].strip()  # get the pure code
            if toUpdateColumn[0] == "(":
                # (columnName) <- value, remove the "()"
                toUpdateColumn = toUpdateColumn[1:-1].strip()
                # remove possible trailing ","
                toUpdateColumn = toUpdateColumn.replace(",", "", 9999999).strip()

            # get the index and then type of the to update column
            columnIndex = -1
            try:
                columnIndex = columns.index(toUpdateColumn)
            except:
                # wtf why can .index() error??
                Logger.error(
                    "column doesnt exist for the map expression:", toUpdateColumn
                )
                return None

            fixType = type(data[columnIndex])  # get the type of the column
            if fixType is type(None):
                fixType = lambda x: x  # icon hardcoded to identity
                # because of icon: None | Str

            # add all column names with its current data value
            for index, column in enumerate(columns):
                vals[column] = data[index]

            try:
                res = eval(code, vals)
            except:
                Logger.error("couldn't evaluate the following map code:", code)
                return None
            try:
                res = fixType(res)
            except:
                Logger.error(
                    "the following map code evaluated to the wrong type:",
                    code,
                    res,
                    type(res),
                    type(data[columnIndex]),
                )
                return None
            return [toUpdateColumn, res]
        else:  # case with mutliple columns
            toUpdateColumns = code[0][1:-1]  # remove leading "(" and trailing ")"
            toUpdateColumns = [v.strip() for v in toUpdateColumns.split(",")]
            code = code[1]  # get the pure code

            # get the indexes of the columns
            indexes = []
            for toUpdateColumn in toUpdateColumns:
                try:
                    indexes.append(columns.index(toUpdateColumn))
                except:
                    Logger.error(
                        "column doesnt exist for the map expression:",
                        toUpdateColumn,
                        toUpdateColumns,
                    )
                    return None

            fixTypes = []  # get the type of the columns respectively to their index
            for i in indexes:
                t = type(data[i])
                if t is type(None):
                    t = lambda x: x  # icon hardcoded to identity
                    # because of icon: None | Str, None shouldnt be forced to be parsed into None but can switch to Str, aswell as the other way around
                fixTypes.append(t)

            # add all column names with its current data value
            for index, column in enumerate(columns):
                vals[column] = data[index]

            try:
                res = eval(code, vals)
            except:
                Logger.error("couldn't evaluate the following map code:", code)
                return None
            try:
                if type(res) != type(("this is a tuple", 1)) and type(res) != type([]):
                    Logger.error(
                        "the map code for changing multiple columns at once, did not return a tuple or a list"
                    )
                    return None
                else:
                    res = list(res)
                for i in range(len(res)):
                    res[i] = fixTypes[i](res[i])
            except:
                Logger.error(
                    "the following map code evaluated to the wrong type:",
                    code,
                    res,
                    type(res),
                    type(data[columnIndex]),
                )
                return None
            return ["multi", toUpdateColumns, res]
    elif mode == "filter":
        code = string.strip()
        for index, column in enumerate(columns):
            vals[column] = data[index]

        try:
            return bool(eval(code, vals))
        except:
            Logger.error("couldn't evaluate the filter code:", code)
            return None
    elif mode == "sort":
        code = string.strip()
        for index, column in enumerate(columns):
            vals[str(column) + "1"] = data[0][index]
            vals[str(column) + "2"] = data[1][index]

        try:
            val = int(eval(code, vals))
            return val
        except:
            Logger.error("couldn't evaluate the sort code:", code)
            return None

    return None
