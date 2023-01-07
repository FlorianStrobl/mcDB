import re
import random
import numpy
import math
from typing import Union, Literal
import addImport
import Logger
from TmpData import *

MAX_INT = 9007199254740991

# return for a given string which of the following modes it represents: ("map", "sort", "slice", "columns", "filter")
# with the default value of "filter" mode
def getMode(
    string: str,
    mode: Literal["auto", "filter", "map", "sort", "slice", "columns"] = "auto",
) -> Literal["map", "sort", "slice", "columns", "filter"]:
    # TODO not perfect, but good enough for now.
    # "player_id1 - player_id2"
    # would be parsed to sort even tho it is a filter

    string = string.strip()
    if mode == "auto":
        # try getting the current mode
        if (
            re.search("^( *)?[A-Za-z_][A-Za-z0-9_]* *<-.*", string) is not None
            or re.search("^( *)?\([A-Za-z_0-9, ]*\) *<-.*", string) is not None
        ):
            # match identifier <- ANY
            # or match (any symbol out of [A-Za-z_0-9, ]) <- Any
            mode = "map"
        elif re.search("^.*[a-zA-Z_][a-zA-Z0-9_]*(1|2)(.|\n)*$", string) is not None:
            # match ANY test1|2 ANY
            mode = "sort"
        elif string.lower().startswith("slice"):
            mode = "slice"
        elif (
            re.search(
                "^[a-zA-Z0-9_, ]+$",
                string.replace(" ", "", MAX_INT)
                .replace("\t", "", MAX_INT)
                .replace("\n", "", MAX_INT)
                .lower()
                .strip(),
            )
            is not None
            and string != "True"
            and string != "False"
        ):
            mode = "columns"
        else:
            # couldn't find anything else so it must be filter
            mode = "filter"
    return mode


# executes the given user string and returns the result
# with the given data
# this function does not include the "columns" mode
def executeUserStr(
    string: str,
    mode: Literal["auto", "filter", "map", "sort", "slice"] = "auto",
    columns: list[str] = [],
    data: list[any] = [],
    workingOnIdx1: Optional[int] = None,
    workingOnIdx2: Optional[int] = None,
    showLogs: bool = True,
) -> Union[None, int, bool, any]:
    mode = getMode(string, mode)  # mode stays the same if it was already set
    if mode == "columns":
        if showLogs:
            Logger.Logger.error(
                "Internal error, executeUserStr cannot be called with mode=columns"
            )
        return None

    # libraries and data to use in the eval
    evalVars = {
        "random": random,
        "math": math,
        "numpy": numpy,
        "data": (data or [])[:],
        "length": len(data or []),
    }
    # the index for the current row
    # and for sort mode the index of both rows
    if workingOnIdx2 is None:
        # not sort mode
        evalVars["index"] = workingOnIdx1
    else:
        # sort mode, could do an if with error
        evalVars["index1"] = workingOnIdx1
        evalVars["index2"] = workingOnIdx2

    if mode == "map":
        # create a lambda with the signature: Callable[[any], bool]
        code = re.split("<-", string, 1)  # split on first occurence
        if len(code) == 0 or len(code) == 1:
            if showLogs:
                Logger.Logger.error("couldn't parse the map expression:", string)
            return None

        code[0] = code[0].strip()
        mustStartWithIdentifier = code[0][0] != "("
        isWrappedIdentifier = [
            v.strip() for v in code[0][1:-1].split(",") if v.strip() != ""
        ]
        isWrappedIdentifier = len(isWrappedIdentifier) == 1
        # if exactly one
        if mustStartWithIdentifier or isWrappedIdentifier:
            toUpdateColumn = code[0]  # get the current column to do
            code = code[1].strip()  # get the pure code
            if toUpdateColumn[0] == "(":
                # (columnName) <- value, remove the "()"
                toUpdateColumn = toUpdateColumn[1:-1].strip()
                # remove possible trailing ","
                toUpdateColumn = toUpdateColumn.replace(",", "", MAX_INT).strip()

            # get the index and then type of the to update column
            columnIndex = -1
            try:
                columnIndex = columns.index(toUpdateColumn)
            except:
                # wtf why can .index() error??
                if showLogs:
                    Logger.Logger.error(
                        "column doesnt exist for the map expression:", toUpdateColumn
                    )
                return None

            fixType = type(data[columnIndex])  # get the type of the column
            if fixType is type(None):
                fixType = lambda x: x  # icon hardcoded to identity
                # because icon is of type: None | Str

            # add all column names with its current data value
            for index, column in enumerate(columns):
                evalVars[column] = data[index]

            try:
                res = eval(code, evalVars)
            except:
                if showLogs:
                    Logger.Logger.error(
                        "couldn't evaluate the following map code:", code
                    )
                return None
            try:
                res = fixType(res) if res is not None else None
            except:
                if showLogs:
                    Logger.Logger.error(
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
            toUpdateColumns = [
                v.strip() for v in toUpdateColumns.split(",") if v.strip() != ""
            ]
            code = code[1]  # get the pure code

            # get the indexes of the columns
            indexes = []
            for toUpdateColumn in toUpdateColumns:
                try:
                    indexes.append(columns.index(toUpdateColumn))
                except:
                    if showLogs:
                        Logger.Logger.error(
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
                evalVars[column] = data[index]

            try:
                res = eval(code, evalVars)
            except:
                if showLogs:
                    Logger.Logger.error(
                        "couldn't evaluate the following map code:", code
                    )
                return None
            try:
                if type(res) != type(("this is a tuple", 1)) and type(res) != type([]):
                    if showLogs:
                        Logger.Logger.error(
                            "the map code for changing multiple columns at once, did not return a tuple or a list"
                        )
                    return None
                else:
                    res = list(res)
                for i in range(len(res)):
                    res[i] = fixTypes[i](res[i]) if res[i] is not None else None
            except:
                if showLogs:
                    Logger.Logger.error(
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
            # add all column names with its current data value to the eval vars
            evalVars[column] = data[index]

        ans = None
        try:
            # the code must evaluate
            ans = eval(code, evalVars)
        except:
            if showLogs:
                Logger.Logger.error("couldn't evaluate the filter code:", code)
            return None

        try:
            # and the code must evaluate to a boolean
            return bool(ans)
        except:
            if showLogs:
                Logger.Logger.error("couldn't cast the filter code to a boolean:", code)
            return None

    elif mode == "sort":
        code = string.strip()
        for index, column in enumerate(columns):
            evalVars[str(column) + "1"] = data[0][index]
            evalVars[str(column) + "2"] = data[1][index]

        val = None
        try:
            val = eval(code, evalVars)
        except:
            if showLogs:
                Logger.Logger.error("couldn't evaluate the sort code:", code)
            return None
        try:
            return int(val)
        except:
            if showLogs:
                Logger.Logger.error("couldn't cast the sort code to an integer:", code)
            return None

    elif mode == "slice":
        string = string.strip()
        if not string.lower().startswith("slice"):
            if showLogs:
                Logger.Logger.error(
                    "slice command didn't work because it doesnt start correctly:",
                    string,
                )
            return None
        string = string[len("slice") :].strip()  # remove the "slice"
        nm = string.split(";")
        if len(nm) == 0 or len(nm) > 2:
            if showLogs:
                Logger.Logger.error(
                    "slice command didn't work because it didnt get 1 to 2 integers as values:",
                    string,
                )
            return None
        if len(nm) == 1:
            try:
                return data[int(eval(nm[0].strip(), evalVars)) :]
            except:
                if showLogs:
                    Logger.Logger.error(
                        "slice command couldn't parse code to integer:", string, nm[0]
                    )
                return None
        else:
            try:
                return data[
                    int(eval(nm[0].strip(), evalVars)) : int(
                        eval(nm[1].strip(), evalVars)
                    )
                ]
            except:
                if showLogs:
                    Logger.Logger.error(
                        "slice command couldn't evaluate the code or parse code to an integer:",
                        nm[0],
                        nm[1],
                    )
                return None

    return None  # nothing matched
