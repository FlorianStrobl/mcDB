
# Einpflegen
import sqlite3
# 1. Holt alle Daten aus Tabelle
# 2. Macht sie in die Datenbank rein

# Gegebene Variablen:
#  - tableDataBodyWidgets -> Enthält alle Input Fields als Widget in einem Table 2d Array
#  - insertIntoTable: Funktion die Daten in einer Table insertet

cursor: sqlite3.Connection.cursor = sqlite3.connect("minecraftDatabase.db").cursor()
def einpflegen(tableName):
  def getTablesInputs():
      result = []
      # Es wird jede row durchgegangen
      for widgetRow in tableDataBodyWidgets:
          subresult = []
          # Es wird jedes element durchgegangen bis auf das letzte und ui subresult appended -> weil das letzte das Mülleimer Objekt ist
          for widget in range(len(widgetRow) - 1):
              subresult.append(widgetRow[widget].get())
          # Dieser row input wird dem result array appended
          result.append(subresult)
      return result
  # Daten werden von den inputs in einer BeispielTable hinzugefügt
  insertIntoTable(cursor, getTablesInputs(), "BeispielTable")