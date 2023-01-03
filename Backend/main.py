import sqlite3
import random
import addImport
from Logger import *
import SQL
from TmpData import *
from InputStrToMapFilterSort import *
from GUI.main import loadGUI

cursor: sqlite3.Connection.cursor = sqlite3.connect("minecraftDatabase.db").cursor()

SQL.dropAllTables(cursor)  # delete current db
SQL.createAllTables(cursor)  # create all tables
SQL.fillAllTablesRand(cursor, 100)  # fill random data into the tables

loadGUI()

# v = tmp.editData("""session_begin <- 0 && session_begin, player_id, serverworld_id, role, player_position""") # TODO, if i swap, should i swap the order of the columns in the UI too?
