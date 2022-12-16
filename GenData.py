import random
import uuid
import time
from Names import *


class HelperFuncs:
    # generieren n UIDs mit dem Wert: String
    def generateUID(n=1):
        UIDs = []
        for i in range(n):
            UIDs.append(uuid.uuid4().hex)
        return UIDs

    # generiere n Servernamen mit dem Wert: String
    def generateServernames(n=1):
        possibleNames = names1.splitlines()

        names = []
        while len(names) < n:
            name = random.choice(possibleNames)
            if n < len(possibleNames):
                # and not name in names
                names.append(name)
        return names

    # generiere n icons mit Wert: String oder None
    def generateIcons(n=1):
        icons = []
        for i in range(n):
            if random.random() < 0.2:
                icons.append(None)  # 20% of the time the server icon is null
            else:
                icons.append("https://mc-icons/" + uuid.uuid4().hex)
        return icons

    # generiere n Skins mit dem Wert: String
    def generateSkins(n=1):
        icons = []
        for i in range(n):
            icons.append("https://mc-skin/" + uuid.uuid4().hex)
        return icons

    # generiere n Timestamps mit dem Wert: Integer
    def generateTimestamp(n=1):
        timestamps = []
        for i in range(n):
            timestamps.append(int(time.time()) + int(random.random() * 10000000))
        return timestamps

    # generiere n enum values mit dem Wert: int (zwischen 0 und maxVal)
    def generateDecodedEnumValue(n=1, maxVal=10):
        values = []
        for i in range(n):
            values.append(int(random.random() * maxVal))
        return values

    # genriere n Booleans mit dem Wert: bool
    def generateBoolean(n=1):
        bools = []
        for i in range(n):
            bools.append(int(random.random() < 0.5))
        return bools

    # generiere n Positionen mit dem Wert: str((int, int, int))
    def generateAbsolutePosition(n=1):
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

    # generiere n Roles mit dem Wert: String
    def generateRoles(n=1):
        possibleRoles = ["Admin", "Moderator", "Player"]
        roles = []
        while len(roles) < n:
            roles.append(random.choice(possibleRoles))
        return roles

    # generiere n Usernames mit dem Wert: String
    def generateUsernames(n=1):
        possibleNames = names2.splitlines()

        names = []
        while len(names) < n:
            name = random.choice(possibleNames)
            if n < len(possibleNames):
                # and not name in names
                names.append(name)
        return names

    def convertUIDStrToInt(uid):
        return int(uid, 16)


class GenerateTableData:
    def generateServerworlds(n=1):
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
