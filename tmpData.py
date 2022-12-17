class TMP:
  data: [] = []

  def setData(self, data):
    self.data = data

  def getData(self):
    return self.data

  def printThis(self):
    print(self.getData())