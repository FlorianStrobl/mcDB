import re
from Logger import *
from typing import Union

# mode: ["auto", "filter", "map", "sort"], TODO add func return type
def userStrToLambda(string: str, mode: str = "auto", columns: list[str] = [], data: list[any] = []) -> Union[None, int, bool, any]:
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


  if mode == "map":
    # create a lambda with the signature: Callable[[any], bool]
    code = re.split("<-", string, 1) # split on first occurence
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


    code = code[1] # get the pure code

    # replace all column names, with its current data value
    # TODO, what about id4 (id is a column, but it replaces it to (val)4
    for index,column in enumerate(columns):
      code = code.replace(column, f"({str(data[index])})")


    try:
      return [toUpdateColumn, fixType(eval(code))]
    except:
      Logger.error("couldn't evaluate the following code:", code)
      return None
  elif mode == "filter":
    code = string
    for index,column in enumerate(columns):
      code = code.replace(column, f"({str(data[index])})")

    try:
      return bool(eval(code))
    except:
      Logger.error("couldn't evaluate the filter code:", code)
      return None
  elif mode == "sort":
    code = string
    for index,column in enumerate(columns):
      code = code.replace(str(column) + "1", f"({str(data[0][index])})")
      code = code.replace(str(column) + "2", f"({str(data[1][index])})")

    try:
      return int(eval(code))
    except:
      Logger.error("couldn't evaluate the sort code:", code)
      return None

  return None