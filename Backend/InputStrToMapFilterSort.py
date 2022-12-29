import re
from Logger import *
from typing import Union, Literal
import random
import numpy
import math


def getMode(string: str, mode: Literal["auto", "filter", "map", "sort"] = "auto") -> str:
    if mode == "auto":
        # try getting the current mode
        if re.search("^( *)?[A-Za-z_][A-Za-z0-9_]* *<-.+ *", string) is not None:
            # match identifier <= ANY
            mode = "map"
        elif re.search("^.*[a-zA-Z_][a-zA-Z0-9_]*(1|2)(.|\n)*$", string):
            # match ANY test1|2 ANY
            # TODO, could be "test1" inside the str
            mode = "sort"
        else:
            mode = "filter"
    return mode


# mode: ["auto", "filter", "map", "sort"], TODO add func return type
def executeUserStr(
    string: str, mode: Literal["auto", "filter", "map", "sort"] = "auto", columns: list[str] = [], data: list[any] = []
) -> Union[None, int, bool, any]:
    mode = getMode(string, mode)

    vals = {"random": random, "math": math, "numpy": numpy}
    if mode == "map":
        # create a lambda with the signature: Callable[[any], bool]
        code = re.split("<-", string, 1)  # split on first occurence
        if len(code) == 0 or len(code) == 1:
            Logger.error("couldn't parse the map expression", string)
            return None

        toUpdateColumn = code[0].strip()

        # get the index and then type of the to update column
        _i = None
        try:
            _i = columns.index(toUpdateColumn)
        except:
            Logger.error("none existent column in map expression:", toUpdateColumn)
            return None
        fixType = type(data[_i])
        if fixType is type(None):
            fixType = lambda x: x  # icon hardcoded to identity
            # because of None and Str

        code = code[1]  # get the pure code

        # replace all column names, with its current data value
        # TODO, what about id4 (id is a column, but it replaces it to (val)4
        for index, column in enumerate(columns):
            vals[column] = data[index]

        try:
            return [toUpdateColumn, fixType(eval(code, vals))]
        except:
            Logger.error("couldn't evaluate the following code:", code)
            return None
    elif mode == "filter":
        code = string
        for index, column in enumerate(columns):
            vals[column] = data[index]

        try:
            return bool(eval(code, vals))
        except:
            Logger.error("couldn't evaluate the filter code:", code)
            return None
    elif mode == "sort":
        code = string
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
