import random
import uuid
import time
from typing import Union, Optional, Literal
import addImport
import Logger
from Names import *
from GenDataJoinSafe import *

TRIM: int = 2**52 - 1  # max 52 bit integers for IDs

# for two given lists, return the index of the first pair of elements that are equal
def searchForFirstDoublePair(arr1: list, arr2: list) -> int:
    arr = list(zip(arr1, arr2))  # combine the two lists into a list of tuples
    theSet = set([])
    for i in range(len(arr)):
        oldLen = len(theSet)
        theSet.add(arr[i])
        # keep adding the next element to the set and check if it got replaced
        if oldLen + 1 != len(theSet):
            return i
    return -1


# Helper functions for generating random data
class HelperFuncs:
    # generate UIDs in hex format
    def generateUID(n: int = 1) -> list[str]:
        UIDs = []
        for i in range(n):
            UIDs.append(uuid.uuid4().hex)
        return UIDs

    # generate icons in the format: "https://mc-icons/" + uid
    def generateIcons(n: int = 1) -> list[Optional[str]]:
        icons = []
        for i in range(n):
            if random.random() < 0.2:
                icons.append(None)  # 20% of the time the server icon is null
            else:
                icons.append("https://mc-icons/" + uuid.uuid4().hex)
        return icons

    # generate skins in the format: "https://mc-skin/" + uid
    def generateSkins(n: int = 1) -> list[str]:
        icons = []
        for i in range(n):
            icons.append("https://mc-skin/" + uuid.uuid4().hex)
        return icons

    # generate integers between 0 and 1
    def generateBoolean(n: int = 1) -> list[int]:
        bools = []
        for i in range(n):
            bools.append(int(random.random() < 0.5))
        return bools

    # uses current time as timestamp and adds/subtracts 0 to 10000000 (about 115 days)
    def generateTimestamp(n: int = 1) -> list[int]:
        timestamps = []
        for i in range(n):
            timestamps.append(
                int(time.time())
                + (int(random.random() * 10000000))
                * ((-1) ** (int(random.random() > 0.5)))
            )
        return timestamps

    # generate enum values between 0 and maxVal
    def generateDecodedEnumValue(n: int = 1, maxVal: int = 10) -> list[int]:
        values = []
        for i in range(n):
            values.append(int(random.random() * maxVal))
        return values

    # generate positions with the format (int, int, int) from 0 to MAX_VAL
    def generateAbsolutePosition(n: int = 1, maxVal: int = 30_000_000) -> list[str]:
        positions = []
        for i in range(n):
            positions.append(
                str(
                    (
                        int(random.random() * maxVal),
                        int(random.random() * maxVal),
                        int(random.random() * maxVal),
                    )
                )
            )
        return positions

    # generate names
    def generateServernames(n: int = 1, namePool: list[str] = names1) -> list[str]:
        possibleNames = namePool.splitlines()
        names = []
        while len(names) < n:
            names.append(random.choice(possibleNames))
        return names

    # generate names
    def generateUsernames(n: int = 1, namePool: list[str] = names2) -> list[str]:
        possibleNames = namePool.splitlines()

        names = []
        while len(names) < n:
            names.append(random.choice(possibleNames))
        return names

    # generate roles which can be one of those: ("Admin", "Moderator", "Player")
    def generateRoles(n: int = 1) -> Literal["Admin", "Moderator", "Player"]:
        possibleRoles: list[str] = ["Admin", "Moderator", "Player"]
        roles = []
        while len(roles) < n:
            roles.append(random.choice(possibleRoles))
        return roles

    # takes a hex UID str and converts it to an int
    def convertUIDStrToInt(uid: str) -> int:
        return int(uid, 16)

    # takes a list of hex UID strs and converts them to ints
    def convertUIDsStrToInts(uids: list[str]) -> list[int]:
        for i in range(len(uids)):
            uids[i] = HelperFuncs.convertUIDStrToInt(uids[i])
        return uids


class GenerateTableData:
    # [serverworld_id, name, icon]
    def generateServerworlds(n: int = 1) -> list[(int, str, Optional[str])]:
        serverworlds = []

        serverworld_ids = HelperFuncs.convertUIDsStrToInts(HelperFuncs.generateUID(n))
        names = HelperFuncs.generateServernames(n)
        icons = HelperFuncs.generateIcons(n)

        # add data to array
        for i in range(n):
            serverworlds.append((serverworld_ids[i] & TRIM, names[i], icons[i]))

        return serverworlds

    # [player_id, username, skin]
    def generatePlayers(n: int = 1) -> list[(int, str, str)]:
        players = []

        player_ids = HelperFuncs.convertUIDsStrToInts(HelperFuncs.generateUID(n))
        usernames = HelperFuncs.generateUsernames(n)
        skins = HelperFuncs.generateSkins(n)

        # add data to array
        for i in range(n):
            players.append((player_ids[i] & TRIM, usernames[i], skins[i]))

        return players

    # [m_entities_id, entity_position, birthday, entity_type]
    def generateMEntities(n: int = 1) -> list[(int, str, int, int)]:
        entities = []

        m_entities_ids = HelperFuncs.convertUIDsStrToInts(HelperFuncs.generateUID(n))
        entity_positions = HelperFuncs.generateAbsolutePosition(n)
        birthdays = HelperFuncs.generateTimestamp(n)
        entity_types = HelperFuncs.generateDecodedEnumValue(n)

        # add data to array
        for i in range(n):
            entities.append(
                (
                    m_entities_ids[i] & TRIM,
                    entity_positions[i],
                    birthdays[i],
                    entity_types[i],
                )
            )

        return entities

    # [absolute_position, block_type]
    def generateBlocks(n: int = 1) -> list[(str, int)]:
        blocks = []

        absolute_positions = HelperFuncs.generateAbsolutePosition(n)
        block_types = HelperFuncs.generateDecodedEnumValue(n)

        # add data to array
        for i in range(n):
            blocks.append((absolute_positions[i], block_types[i]))

        return blocks

    # [absolute_position, isOnFire] but only half of n
    def generateWoods(n: int = 1, cursor=None) -> Optional[list[(str, int)]]:
        n = n // 2
        woods = []

        abspos = getRealFirstAbsolute_positions(cursor)
        if abspos is None:
            Logger.Logger.error(
                "Couldn't generate wood because there are no blocks in the database."
            )
            return None
        absolute_positions = abspos
        # get the first half of the block positions
        absolute_positions = absolute_positions[: len(absolute_positions) // 2]
        random.shuffle(absolute_positions)  #  randomize the order of the positions
        isOnFire = HelperFuncs.generateBoolean(n)

        # add data to array
        for i in range(n):
            woods.append((absolute_positions[i], isOnFire[i]))

        return woods

    # [absolute_position, hasGrass]  but only half of n
    def generateDirt(n: int = 1, cursor=None) -> Optional[list[(str, int)]]:
        n = n // 2
        dirts = []

        abspos = getRealFirstAbsolute_positions(cursor)
        if abspos is None:
            Logger.Logger.error(
                "Couldn't generate dirt because there are no blocks in the database."
            )
            return None
        absolute_positions = abspos
        # get the second half of the block positions
        absolute_positions = absolute_positions[len(absolute_positions) // 2 :]
        random.shuffle(absolute_positions)  #  randomize the order of the positions
        hasGrass = HelperFuncs.generateBoolean(n)

        # add data to array
        for i in range(n):
            dirts.append((absolute_positions[i], hasGrass[i]))

        return dirts

    # [player_id, serverworld_id, session_begin, player_position, role]
    def generatePlays(
        n: int = 1, cursor=None
    ) -> Optional[list[(int, int, int, str, str)]]:
        plays = []

        pids = getRealPlayerIds(cursor, n)
        if pids is None:
            Logger.Logger.error(
                "Couldn't generate plays because there are no players in the database."
            )
            return None
        player_ids = pids
        sids = getRealServerworldIds(cursor, n)
        if sids is None:
            Logger.Logger.error(
                "Couldn't generate plays because there are no servers in the database."
            )
            return None
        serverworld_ids = sids

        # fix double pairs for unique constraint
        tries = 0  # only try it up to 50% of the ids
        # cannot be None since it was already checked
        cache = getRealServerworldIds(
            cursor, n
        )  # instead of getting all the ids over and over, cache them and use them
        idx = searchForFirstDoublePair(player_ids, serverworld_ids)
        # only try it while there are collisions and up to once all of the n times
        while idx != -1 and tries < n:
            # replace the serverworld_id at idx with a new one
            serverworld_ids[idx] = random.choice(cache)

            idx = searchForFirstDoublePair(
                player_ids, serverworld_ids
            )  # search for new collision

        # idx is still set from the very last while loop iteration
        if idx != -1:
            Logger.Logger.error(
                "Couldn't generate plays because there are probably no unique pairs anymore."
            )
            return None

        session_begins = HelperFuncs.generateTimestamp(n)
        player_positions = HelperFuncs.generateAbsolutePosition(n)
        roles = HelperFuncs.generateRoles(n)

        # add data to array
        for i in range(n):
            plays.append(
                (
                    player_ids[i] & TRIM,
                    serverworld_ids[i] & TRIM,
                    session_begins[i],
                    player_positions[i],
                    roles[i],
                )
            )

        return plays

    # [m_entities_id, serverworld_id]
    def generatePopulatedBy(n: int = 1, cursor=None) -> Optional[list[(int, int)]]:
        populatedBy = []

        meids = getRealMEntityIds(cursor, n)
        if meids is None:
            Logger.Logger.error(
                "Couldn't generate populatedBy because there are no entities in the database."
            )
            return None
        m_entities_ids = meids
        swids = getRealServerworldIds(cursor, n)
        if swids is None:
            Logger.Logger.error(
                "Couldn't generate populatedBy because there are no servers in the database."
            )
            return None
        serverworld_ids = swids

        # fix double pairs for unique constraint
        tries = 0  # only try it up to 50% of the ids
        cache = getRealServerworldIds(
            cursor, n
        )  # instead of getting all the ids over and over, cache them and use them
        # cannot be None since it was already checked
        idx = searchForFirstDoublePair(m_entities_ids, serverworld_ids)
        # only try it while there are collisions and up to once all of the n times
        while idx != -1 and tries < n:
            # replace the serverworld_id at idx with a new one
            serverworld_ids[idx] = random.choice(cache)

            idx = searchForFirstDoublePair(
                m_entities_ids, serverworld_ids
            )  # search for new collision

        # idx is still set from the very last while loop iteration
        if idx != -1:
            Logger.Logger.error(
                "Couldn't generate populatedBy because there are probably no unique pairs anymore."
            )
            return None

        # add data to array
        for i in range(n):
            populatedBy.append((m_entities_ids[i] & TRIM, serverworld_ids[i] & TRIM))

        return populatedBy

    # [absolute_position, serverworld_id]
    def generateBuildOf(n: int = 1, cursor=None) -> Optional[list[(str, int)]]:
        buildOfs = []

        abspos = getRealAbsolute_positions(cursor, n)
        if abspos is None:
            Logger.Logger.error(
                "Couldn't generate buildOf because there are no blocks in the database."
            )
            return None
        absolute_positions = abspos
        swids = getRealServerworldIds(cursor, n)
        if swids is None:
            Logger.Logger.error(
                "Couldn't generate buildOf because there are no servers in the database."
            )
            return None
        serverworld_ids = swids

        # fix double pairs for unique constraint
        tries = 0  # only try it up to 50% of the ids
        # cannot be None since it was already checked
        cache = getRealServerworldIds(
            cursor, n
        )  # instead of getting all the ids over and over, cache them and use them
        idx = searchForFirstDoublePair(absolute_positions, serverworld_ids)
        # only try it while there are collisions and up to once all of the n times
        while idx != -1 and tries < n:
            # replace the serverworld_id at idx with a new one
            serverworld_ids[idx] = random.choice(cache)

            idx = searchForFirstDoublePair(
                absolute_positions, serverworld_ids
            )  # search for new collision

        if idx != -1:
            Logger.Logger.error(
                "Couldn't generate buildOf because there are probably no unique pairs anymore."
            )
            return None

        # add data to array
        for i in range(n):
            buildOfs.append((absolute_positions[i], serverworld_ids[i] & TRIM))

        return buildOfs
