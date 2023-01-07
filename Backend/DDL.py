# SQLite3 commands for CREATE TABLE

# Serverworld(serverworld_id: bigint, name: str, icon: str | null)
# Player(player_id: bigint, username: str, skin: str)
# MEntities(m_entities_id: bigint, entity_position: str, birthday: int, entity_type: int)
# Block(absolute_position: str, block_type: int)

# Wood(absolute_position: str, isOnFire: int)
# Dirt(absolute_position: str, hasGrass: int)

# plays(player_id: bigint, serverworld_id: bigint, session_begin: int, player_position: str, role: str)
# populatedBy(m_entities_id: bigint, serverworld_id: bigint)
# buildOf(absolute_position: str, serverworld_id: bigint)

# Serverworld, Player, MEntities, Block
tablesStrong: dict[str, str] = {
    "Serverworld": """
    CREATE TABLE IF NOT EXISTS Serverworld (
      serverworld_id bigint PRIMARY KEY
        CHECK (serverworld_id > 0),
      name TEXT NOT NULL
        CHECK (name != ""),
      icon TEXT
    );
    """,
    "Player": """
    CREATE TABLE IF NOT EXISTS Player (
      player_id bigint PRIMARY KEY
        CHECK (player_id > 0),
      username TEXT NOT NULL
        CHECK (username != ""),
      skin TEXT NOT NULL
        CHECK (skin != "")
    );
    """,
    "MEntities": """
    CREATE TABLE IF NOT EXISTS MEntities (
      m_entities_id bigint PRIMARY KEY
        CHECK (m_entities_id > 0),
      entity_position TEXT NOT NULL
        CHECK (entity_position != ""
          AND entity_position LIKE "(%,%,%)"),
      birthday DATE NOT NULL
        CHECK (birthday > 0),
      entity_type INTEGER NOT NULL
        CHECK (entity_type >= 0 AND entity_type < 10)
    );
    """,
    "Block": """
    CREATE TABLE IF NOT EXISTS Block (
      absolute_position TEXT PRIMARY KEY
        CHECK (absolute_position != "" AND absolute_position LIKE "(%,%,%)"),
      block_type INTEGER NOT NULL
        CHECK (block_type >= 0 AND block_type < 10)
    );
  """,
}

# Wood, Dirt
tablesWeak: dict[str, str] = {
    "Wood": """
    CREATE TABLE IF NOT EXISTS Wood (
      absolute_position TEXT NOT NULL UNIQUE
        CHECK (absolute_position != "" AND absolute_position LIKE "(%,%,%)"),
      isOnFire INTEGER DEFAULT 0
        CHECK (isOnFire == 0 OR isOnFire == 1),

      PRIMARY KEY(absolute_position),

      FOREIGN KEY(absolute_position) REFERENCES Block(absolute_position)
        on UPDATE cascade
        on DELETE cascade
    );
    """,
    "Dirt": """
    CREATE TABLE IF NOT EXISTS Dirt (
      absolute_position TEXT NOT NULL UNIQUE
        CHECK (absolute_position != "" AND absolute_position LIKE "(%,%,%)"),
      hasGrass INTEGER DEFAULT 0
        CHECK (hasGrass == 0 OR hasGrass == 1),

      PRIMARY KEY(absolute_position),

      FOREIGN KEY(absolute_position) REFERENCES Block(absolute_position)
        on UPDATE cascade
        on DELETE cascade
    );""",
}

# plays, populatedBy, buildOf
tableRelations: dict[str, str] = {
    "plays": """
    CREATE TABLE IF NOT EXISTS plays (
      player_id bigint NOT NULL
        CHECK (player_id > 0),
      serverworld_id bigint NOT NULL
        CHECK (serverworld_id > 0),
      session_begin DATE NOT NULL
        CHECK (session_begin > 0),
      player_position TEXT NOT NULL
        CHECK (player_position != "" AND player_position LIKE "(%,%,%)"),
      role TEXT NOT NULL
        CHECK (role != "" AND role IN ("Admin", "Moderator", "Player")),

      PRIMARY KEY(player_id, serverworld_id),

      FOREIGN KEY(player_id) REFERENCES Player(player_id)
        on UPDATE cascade
        on DELETE cascade,

      FOREIGN KEY(serverworld_id) REFERENCES Serverworld(serverworld_id)
      on UPDATE cascade
      on DELETE cascade
    );""",
    "populatedBy": """
    CREATE TABLE IF NOT EXISTS populatedBy (
      m_entities_id bigint NOT NULL
        CHECK (m_entities_id > 0),
      serverworld_id bigint NOT NULL
        CHECK (serverworld_id > 0),

      PRIMARY KEY(m_entities_id, serverworld_id),

      FOREIGN KEY(m_entities_id) REFERENCES MEntities(m_entities_id)
        on UPDATE cascade
        on DELETE cascade,

      FOREIGN KEY(serverworld_id) REFERENCES Serverworld(serverworld_id)
      on UPDATE cascade
      on DELETE cascade
    );""",
    "buildOf": """
    CREATE TABLE IF NOT EXISTS buildOf (
      absolute_position TEXT NOT NULL
        CHECK (absolute_position != "" AND absolute_position LIKE "(%,%,%)"),
      serverworld_id bigint NOT NULL
        CHECK (serverworld_id > 0),

      PRIMARY KEY(absolute_position, serverworld_id),

      FOREIGN KEY(absolute_position) REFERENCES Block(absolute_position)
        on UPDATE cascade
        on DELETE cascade,

      FOREIGN KEY(serverworld_id) REFERENCES Serverworld(serverworld_id)
      on UPDATE cascade
      on DELETE cascade
    );""",
}
