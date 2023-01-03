# return existing (!!) IDs from a certain table INSTEAD of random ones
import sqlite3
import random
from typing import Optional
import addImport
from Logger import *

def getRealFirstAbsolute_positions(cursor) -> Optional[list[int]]:
    try:
        cursor.execute("SELECT absolute_position FROM Block")
        poses = cursor.fetchall()
    except:
        Logger.error(
            "Error while getting absolute positions from database while generating data"
        )
        return None

    arr = [pos[0] for pos in poses]
    random.shuffle(arr)
    return arr


def getRealAbsolute_positions(cursor, n: int = 1) -> Optional[list[int]]:
    try:
        cursor.execute("SELECT absolute_position FROM Block")
        poses = cursor.fetchall()
    except:
        Logger.error(
            "Error while getting absolute positions from database while generating data"
        )
        return None

    ans = []
    for i in range(n):
        ans.append(random.choice(list(poses))[0])

    return ans


def getRealMEntityIds(cursor, n: int = 1) -> Optional[list[int]]:
    try:
        cursor.execute("SELECT m_entities_id FROM MEntities")
        ids = cursor.fetchall()
    except:
        Logger.error(
            "Error while getting entity ids from database while generating data"
        )
        return None

    ans = []
    for i in range(n):
        ans.append(random.choice(list(ids))[0])

    return ans


def getRealPlayerIds(cursor, n: int = 1) -> Optional[list[int]]:
    try:
        cursor.execute("SELECT player_id FROM Player")
        ids = cursor.fetchall()
    except:
        Logger.error(
            "Error while getting player ids from database while generating data"
        )
        return None

    ans = []
    for i in range(n):
        ans.append(random.choice(list(ids))[0])

    return ans


def getRealServerworldIds(cursor, n: int = 1) -> Optional[list[int]]:
    try:
        cursor.execute("SELECT serverworld_id FROM Serverworld")
        ids = cursor.fetchall()
    except:
        Logger.error(
            "Error while getting serverworld ids from database while generating data"
        )
        return None

    ans = []
    for i in range(n):
        ans.append(random.choice(list(ids))[0])

    return ans
