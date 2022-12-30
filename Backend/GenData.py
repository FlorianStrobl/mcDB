import random
import uuid
import time
from typing import Union, Optional
from Names import *

TRIM = 2**63 - 1  # max 64 bit integers


class HelperFuncs:
    # generate UIDs in hex format
    def generateUID(n: int = 1) -> list[str]:
        UIDs = []
        for i in range(n):
            UIDs.append(uuid.uuid4().hex)
        return UIDs

    def generateIcons(n: int = 1) -> list[Optional[str]]:
        icons = []
        for i in range(n):
            if random.random() < 0.2:
                icons.append(None)  # 20% of the time the server icon is null
            else:
                icons.append("https://mc-icons/" + uuid.uuid4().hex)
        return icons

    def generateSkins(n: int = 1) -> list[str]:
        icons = []
        for i in range(n):
            icons.append("https://mc-skin/" + uuid.uuid4().hex)
        return icons

    def generateBoolean(n: int = 1) -> list[int]:
        bools = []
        for i in range(n):
            bools.append(int(random.random() < 0.5))
        return bools

    # uses current time and adds/subtracts 0s to 10000000s (about 115 days)
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

    def generateServernames(n: int = 1, namePool: list[str] = names1) -> list[str]:
        possibleNames = namePool.splitlines()
        names = []
        while len(names) < n:
            names.append(random.choice(possibleNames))
        return names

    def generateUsernames(n: int = 1, namePool: list[str] = names2) -> list[str]:
        possibleNames = namePool.splitlines()

        names = []
        while len(names) < n:
            names.append(random.choice(possibleNames))
        return names

    # generate roles which can be "Admin", "Moderator", "Player"
    def generateRoles(
        n: int = 1, possibleRoles: list[str] = ["Admin", "Moderator", "Player"]
    ) -> list[str]:
        roles = []
        while len(roles) < n:
            roles.append(random.choice(possibleRoles))
        return roles

    def convertUIDStrToInt(uid: str) -> int:
        return int(uid, 16)

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

    # [absolute_position, isOnFire]
    def generateWoods(n: int = 1) -> list[(str, int)]:
        woods = []

        absolute_positions = HelperFuncs.generateAbsolutePosition(n)
        isOnFire = HelperFuncs.generateBoolean(n)

        # add data to array
        for i in range(n):
            woods.append((absolute_positions[i], isOnFire[i]))

        return woods

    # [absolute_position, hasGrass]
    def generateDirt(n: int = 1) -> list[(str, int)]:
        dirts = []

        absolute_positions = HelperFuncs.generateAbsolutePosition(n)
        hasGrass = HelperFuncs.generateBoolean(n)

        # add data to array
        for i in range(n):
            dirts.append((absolute_positions[i], hasGrass[i]))

        return dirts

    # [player_id, serverworld_id, session_begin, player_position, role]
    def generatePlays(n: int = 1) -> list[(int, int, int, str, str)]:
        plays = []

        player_ids = HelperFuncs.convertUIDsStrToInts(HelperFuncs.generateUID(n))
        serverworld_ids = HelperFuncs.convertUIDsStrToInts(HelperFuncs.generateUID(n))
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
    def generatePopulatedBy(n: int = 1) -> list[(int, int)]:
        populatedBy = []

        m_entities_ids = HelperFuncs.convertUIDsStrToInts(HelperFuncs.generateUID(n))
        serverworld_ids = HelperFuncs.convertUIDsStrToInts(HelperFuncs.generateUID(n))

        # add data to array
        for i in range(n):
            populatedBy.append((m_entities_ids[i] & TRIM, serverworld_ids[i] & TRIM))

        return populatedBy

    # [absolute_position, serverworld_id]
    def generateBuildOf(n: int = 1) -> list[(str, int)]:
        buildOfs = []

        absolute_positions = HelperFuncs.generateAbsolutePosition(n)
        serverworld_ids = HelperFuncs.convertUIDsStrToInts(HelperFuncs.generateUID(n))

        # add data to array
        for i in range(n):
            buildOfs.append((absolute_positions[i], serverworld_ids[i] & TRIM))

        return buildOfs
