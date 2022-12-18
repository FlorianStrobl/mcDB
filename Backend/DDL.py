# Serverworld(serverworld_id: bigint, name: str, icon: str | null)
# Player(player_id: bigint, username: str, skin: str)
# MEntities(m_entities_id: bigint, entity_postion: str, birthday: int, entity_type: int)
# Block(absolute_position: str, block_type: int)
# Wood(absolute_position: str, isOnFire: int)
# Dirt(absolute_position: str, hasGras: int)
# plays(player_id: bigint, serverworld_id: bigint, session_begin: int, player_position: str, role: str)
# populatedBy(m_entities_id: bigint, serverworld_id: bigint)
# buildOf(absolute_position: str, serverworld_id: bigint)

# Serverworld, Player, MEntities, Block
tablesStrong: dict[str, str] = {
    "Serverworld": """CREATE TABLE IF NOT EXISTS Serverworld (
    serverworld_id bigint PRIMARY KEY,
    name TEXT NOT NULL,
    icon TEXT
    );""",

    "Player": """CREATE TABLE IF NOT EXISTS Player (
    player_id bigint PRIMARY KEY,
    username TEXT NOT NULL,
    skin TEXT NOT NULL
    );""",

    "MEntities": """CREATE TABLE IF NOT EXISTS MEntities (
    m_entities_id bigint PRIMARY KEY,
    entity_postion TEXT NOT NULL,
    birthday INTEGER NOT NULL,
    entity_type INTEGER NOT NULL
    );""",

    "Block": """CREATE TABLE IF NOT EXISTS Block  (
    absolute_position TEXT PRIMARY KEY,
    block_type INTEGER NOT NULL
  );"""
}

# Wood, Dirt
tablesWeak: dict[str, str] = {
    "Wood": """CREATE TABLE IF NOT EXISTS Wood (

    absolute_position TEXT NOT NULL UNIQUE,
    isOnFire INTEGER DEFAULT 0,

    PRIMARY KEY(absolute_position),

    FOREIGN KEY(absolute_position) REFERENCES Block(absolute_position)
      on UPDATE cascade
      on DELETE cascade
    );""",

    "Dirt": """CREATE TABLE IF NOT EXISTS Dirt (

    absolute_position TEXT NOT NULL UNIQUE,
    hasGras INTEGER DEFAULT 0,

    PRIMARY KEY(absolute_position),

    FOREIGN KEY(absolute_position) REFERENCES Block(absolute_position)
      on UPDATE cascade
      on DELETE cascade
    );"""
}

# plays, populatedBy, buildOf
tableRelations: dict[str, str] = {
    "plays": """CREATE TABLE IF NOT EXISTS plays (

    player_id bigint NOT NULL,
    serverworld_id bigint NOT NULL,
    session_begin INTEGER NOT NULL,
    player_position TEXT NOT NULL,
    role TEXT NOT NULL,

    PRIMARY KEY(player_id, serverworld_id),

    FOREIGN KEY(player_id) REFERENCES Player(player_id)
      on UPDATE cascade
      on DELETE cascade,

    FOREIGN KEY(serverworld_id) REFERENCES Serverworld(serverworld_id)
      on UPDATE cascade
      on DELETE cascade
    );""",

    "populatedBy": """CREATE TABLE IF NOT EXISTS populatedBy (

    m_entities_id bigint NOT NULL,
    serverworld_id bigint NOT NULL,

    PRIMARY KEY(m_entities_id, serverworld_id),

    FOREIGN KEY(m_entities_id) REFERENCES MEntities(m_entities_id)
      on UPDATE cascade
      on DELETE cascade,

    FOREIGN KEY(serverworld_id) REFERENCES Serverworld(serverworld_id)
      on UPDATE cascade
      on DELETE cascade
    );""",

    "buildOf": """CREATE TABLE IF NOT EXISTS buildOf (

    absolute_position TEXT NOT NULL,
    serverworld_id bigint NOT NULL,

    PRIMARY KEY(absolute_position, serverworld_id),

    FOREIGN KEY(absolute_position) REFERENCES Block(absolute_position)
      on UPDATE cascade
      on DELETE cascade,

    FOREIGN KEY(serverworld_id) REFERENCES Serverworld(serverworld_id)
      on UPDATE cascade
      on DELETE cascade
    );"""
}