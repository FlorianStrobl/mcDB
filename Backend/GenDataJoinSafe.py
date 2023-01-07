# return existing (!!) IDs from a certain table INSTEAD of random ones
import sqlite3
import random
from typing import Optional
import addImport
import Logger

# get the block positions in order from the database
def getRealFirstAbsolute_positions(cursor) -> Optional[list[int]]:
    try:
        cursor.execute("SELECT absolute_position FROM Block")
        poses = cursor.fetchall()
    except:
        Logger.Logger.error(
            "Error while getting absolute positions from database while generating data"
        )
        return None

    arr = [pos[0] for pos in poses]
    return arr


# get the block positions in random order (and with doubles) from the database
def getRealAbsolute_positions(cursor, n: int = 1) -> Optional[list[int]]:
    try:
        cursor.execute("SELECT absolute_position FROM Block")
        poses = cursor.fetchall()
    except:
        Logger.Logger.error(
            "Error while getting absolute positions from database while generating data"
        )
        return None

    ans = []
    for i in range(n):
        ans.append(random.choice(list(poses))[0])

    return ans


# get the entities ids in random order (and with doubles) from the database
def getRealMEntityIds(cursor, n: int = 1) -> Optional[list[int]]:
    try:
        cursor.execute("SELECT m_entities_id FROM MEntities")
        ids = cursor.fetchall()
    except:
        Logger.Logger.error(
            "Error while getting entity ids from database while generating data"
        )
        return None

    ans = []
    for i in range(n):
        ans.append(random.choice(list(ids))[0])

    return ans


# get the player ids in random order (and with doubles) from the database
def getRealPlayerIds(cursor, n: int = 1) -> Optional[list[int]]:
    try:
        cursor.execute("SELECT player_id FROM Player")
        ids = cursor.fetchall()
    except:
        Logger.Logger.error(
            "Error while getting player ids from database while generating data"
        )
        return None

    ans = []
    for i in range(n):
        ans.append(random.choice(list(ids))[0])

    return ans


# get the serverworld ids in random order (and with doubles) from the database
def getRealServerworldIds(cursor, n: int = 1) -> Optional[list[int]]:
    try:
        cursor.execute("SELECT serverworld_id FROM Serverworld")
        ids = cursor.fetchall()
    except:
        Logger.Logger.error(
            "Error while getting serverworld ids from database while generating data"
        )
        return None

    ans = []
    for i in range(n):
        ans.append(random.choice(list(ids))[0])

    return ans
