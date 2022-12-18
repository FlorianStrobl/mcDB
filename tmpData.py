class TMP:
  data: [] = []

  def length(self) -> int:
    return len(self.data)

  def setData(self, data: []) -> None:
    self.data = data

  def getData(self) -> []:
    return self.data

  def filterData(self, _lambda) -> []:
    # TODO
    return self.data

  def printThis(self) -> None:
    print(self.getData())