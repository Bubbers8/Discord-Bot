import sqlite3
def create_connection(dbFile):
    """ create a database connection to a database that resides
        in the memory
    """
    conn = None;
    try:
        conn = sqlite3.connect(dbFile)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


database = r"discord.db"
sqlite3CreateGuildsTable = """
    CREATE TABLE IF NOT EXISTS guild (
        id integer PRIMARY KEY,
        name text NOT NULL,
    );
    """
sqlite3CreateChannelsTable = """
    CREATE TABLE IF NOT EXISTS channel (
        id integer PRIMARY KEY,
        FOREIGN KEY (guilds_id) REFERENCES guild (id)
    )
"""
