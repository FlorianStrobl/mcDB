# Serverworld, Player, MEntities, Block
tablesStrong = {
    "Serverworld": """CREATE TABLE IF NOT EXISTS Serverworld (
    serverworld_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    icon TEXT
    );""",

    "Player": """CREATE TABLE IF NOT EXISTS Player (
    player_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    skin TEXT NOT NULL
    );""",

    "MEntities": """CREATE TABLE IF NOT EXISTS MEntities (
    m_entities_id INTEGER PRIMARY KEY,
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
tablesWeak = {
    "Wood": """CREATE TABLE IF NOT EXISTS Wood (
    absolute_position TEXT NOT NULL,
    isOnFire INTEGER NOT NULL,
    primary key(absolute_position),
    FOREIGN KEY(absolute_position) REFERENCES Block(absolute_position)
    );""",

    "Dirt": """CREATE TABLE IF NOT EXISTS Dirt (
    absolute_position TEXT NOT NULL,
    hasGras INTEGER NOT NULL,
    primary key(absolute_position),
    FOREIGN KEY(absolute_position) REFERENCES Block(absolute_position)
    );"""
}

# plays, populatedBy, buildOf
tableRelations = {
    "plays": """CREATE TABLE IF NOT EXISTS plays (
    player_id INTEGER NOT NULL,
    serverworld_id INTEGER NOT NULL,
    session_begin INTEGER NOT NULL,
    player_position TEXT NOT NULL,
    role TEXT NOT NULL,
    primary key(player_id, serverworld_id),
    FOREIGN KEY(player_id) REFERENCES Player(player_id)
      on UPDATE cascade
      on DELETE cascade,
    FOREIGN KEY(serverworld_id) REFERENCES Serverworld(serverworld_id)
      on UPDATE cascade
      on DELETE cascade
    );""",

    "populatedBy": """CREATE TABLE IF NOT EXISTS populatedBy (
    m_entities_id INTEGER NOT NULL,
    serverworld_id INTEGER NOT NULL,
    primary key(m_entities_id, serverworld_id),
    FOREIGN KEY(m_entities_id) REFERENCES MEntities(m_entities_id)
      on UPDATE cascade
      on DELETE cascade,
    FOREIGN KEY(serverworld_id) REFERENCES Serverworld(serverworld_id)
      on UPDATE cascade
      on DELETE cascade
    );""",

    "buildOf": """CREATE TABLE IF NOT EXISTS buildOf (
    absolute_position TEXT NOT NULL,
    serverworld_id TEXT NOT NULL,
    primary key(absolute_position, serverworld_id),
    FOREIGN KEY(absolute_position) REFERENCES Block(absolute_position)
      on UPDATE cascade
      on DELETE cascade,
    FOREIGN KEY(serverworld_id) REFERENCES Chunk(serverworld_id)
      on UPDATE cascade
      on DELETE cascade
    );"""
}