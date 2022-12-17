from Names import *
import random
import uuid
import time
from typing import Union

class HelperFuncs:
    # generieren n UIDs
    def generateUID(n: int = 1) -> [str]:
        UIDs = []
        for i in range(n):
            UIDs.append(uuid.uuid4().hex)
        return UIDs

    # generiere n Servernamen
    def generateServernames(n: int = 1) -> [str]:
        possibleNames = names1.splitlines()

        names = []
        while len(names) < n:
            name = random.choice(possibleNames)
            # not name in names
            names.append(name)
        return names

    # generiere n icons
    def generateIcons(n: int = 1) -> [Union[str, None]]:
        icons = []
        for i in range(n):
            if random.random() < 0.2:
                icons.append(None)  # 20% of the time the server icon is null
            else:
                icons.append("https://mc-icons/" + uuid.uuid4().hex)
        return icons

    # generiere n Skins
    def generateSkins(n: int = 1) -> [str]:
        icons = []
        for i in range(n):
            icons.append("https://mc-skin/" + uuid.uuid4().hex)
        return icons

    # generiere n Timestamps
    def generateTimestamp(n: int = 1) -> [int]:
        timestamps = []
        for i in range(n):
            timestamps.append(int(time.time()) + int(random.random() * 10000000))
        return timestamps

    # generiere n enum values zwischen 0 und maxVal
    def generateDecodedEnumValue(n: int = 1, maxVal: int = 10) -> [int]:
        values = []
        for i in range(n):
            values.append(int(random.random() * maxVal))
        return values

    # genriere n Booleans
    def generateBoolean(n: int = 1) -> [bool]:
        bools = []
        for i in range(n):
            bools.append(int(random.random() < 0.5))
        return bools

    # generiere n Positionen mit dem Format (int, int, int)
    def generateAbsolutePosition(n: int = 1) -> [str]:
        positions = []
        for i in range(n):
            positions.append(
                str(
                    (
                        int(random.random() * 30_000_000),
                        int(random.random() * 30_000_000),
                        int(random.random() * 30_000_000),
                    )
                )
            )
        return positions

    # generiere n Roles
    def generateRoles(n: int = 1) -> [str]:
        possibleRoles = ["Admin", "Moderator", "Player"]
        roles = []
        while len(roles) < n:
            roles.append(random.choice(possibleRoles))
        return roles

    # generiere n Usernames
    def generateUsernames(n: int = 1) -> [str]:
        possibleNames = names2.splitlines()

        names = []
        while len(names) < n:
            name = random.choice(possibleNames)
            if n < len(possibleNames):
                # and not name in names
                names.append(name)
        return names

    def convertUIDStrToInt(uid: str) -> int:
        return int(uid, 16)


class GenerateTableData:
    def generateServerworlds(n: int = 1) -> [(int, str, Union[str, None])]:
        serverworld = []
        serverworld_ids = HelperFuncs.generateUID(n)
        for i in range(len(serverworld_ids)):
            serverworld_ids[i] = HelperFuncs.convertUIDStrToInt(serverworld_ids[i])
        names = HelperFuncs.generateServernames(n)
        icons = HelperFuncs.generateIcons(n)

        for i in range(n):
            serverworld.append((serverworld_ids[i], names[i], icons[i]))

        return serverworld

    def generatePlayers(n=1):
        players = []

        player_ids = HelperFuncs.generateUID(n)
        usernames = HelperFuncs.generateUsernames(n)
        skins = HelperFuncs.generateSkins(n)

        for i in range(n):
            players.append((player_ids[i], usernames[i], skins[i]))

        return players

    def generateMEntities(n=1):
        entities = []

        m_entities_ids = HelperFuncs.generateUID(n)
        entity_positions = HelperFuncs.generateAbsolutePosition(n)
        birthdays = HelperFuncs.generateTimestamp(n)
        entity_types = HelperFuncs.generateDecodedEnumValue(n)

        for i in range(n):
            entities.append(
                (m_entities_ids[i], entity_positions[i], birthdays[i], entity_types[i])
            )

        return entities

    def generateBlocks(n=1):
        blocks = []

        absolute_positions = HelperFuncs.generateAbsolutePosition(n)
        block_types = HelperFuncs.generateDecodedEnumValue(n)

        for i in range(n):
            blocks.append((absolute_positions[i], block_types[i]))

        return blocks

    def generateWoods(n=1):
        woods = []

        absolute_positions = HelperFuncs.generateAbsolutePosition(n)
        isOnFire = HelperFuncs.generateBoolean(n)

        for i in range(n):
            woods.append((absolute_positions[i], isOnFire[i]))

        return woods

    def generateDirt(n=1):
        dirts = []

        absolute_positions = HelperFuncs.generateAbsolutePosition(n)
        hasGras = HelperFuncs.generateBoolean(n)

        for i in range(n):
            dirts.append((absolute_positions[i], hasGras[i]))

        return dirts

    def generatePlays(n=1):
        plays = []

        player_ids = HelperFuncs.generateUID(n)
        serverworld_ids = HelperFuncs.generateUID(n)
        session_begins = HelperFuncs.generateTimestamp(n)
        player_positions = HelperFuncs.generateAbsolutePosition(n)
        roles = HelperFuncs.generateRoles(n)

        for i in range(n):
            plays.append(
                (
                    player_ids[i],
                    serverworld_ids[i],
                    session_begins[i],
                    player_positions[i],
                    roles[i],
                )
            )

        return plays

    def generatePopulatedBy(n=1):
        populatedBy = []

        m_entities_ids = HelperFuncs.generateUID(n)
        serverworld_ids = HelperFuncs.generateUID(n)

        for i in range(n):
            populatedBy.append((m_entities_ids[i], serverworld_ids[i]))

        return populatedBy

    def generateBuildOf(n=1):
        buildOfs = []

        absolute_positions = HelperFuncs.generateAbsolutePosition(n)
        serverworld_ids = HelperFuncs.generateUID(n)

        for i in range(n):
            buildOfs.append((absolute_positions[i], serverworld_ids[i]))

        return buildOfs
