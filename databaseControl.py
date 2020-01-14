import sqlite3
from sqlite3 import Error
def create_connection(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as e:
        print(e)

    return conn
class User:
    def __init__(id, name, guild_id, santa):
        self.userId = id
        self.userName = name
        self.userGuildId = guild_id
        self.santa = santa
class Guild:
    def __init__(id, name):
        self.guildId = guild_id
        self.guildName = name
class Channel:
    def __init__(id, name, guild_id):
        self.channelName = name
        self.channelId = id
        self.channelGuildId =guild_id

def executeQuery(db, query):
    conn = create_connection(db)
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(query)
        except Error as e:
            print(e)
        conn.close()
    else:
        print("Error! cannot create the database connection.")


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
def dbCreateTables():
    database = r"discord.db"
    sqlite3CreateGuildsTable = """
        CREATE TABLE IF NOT EXISTS guild (
            id integer PRIMARY KEY,
            name text NOT NULL
        );
        """
    sqlite3CreateChannelsTable = """
        CREATE TABLE IF NOT EXISTS channel (
            id integer PRIMARY KEY,
            name text NOT NULL,
            guild_id INTEGER NOT NULL,
            FOREIGN KEY (guild_id) REFERENCES guild (id)
        )
    """
    sqlite3CreateUsersTable = """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER NOT NULL,
            name TEXT NOT NULL,
  			guild_id INTEGER NOT NULL,
            santa BOOLEAN NOT NULL,
            FOREIGN KEY (guild_id) REFERENCES guild (id),
            PRIMARY KEY (id, name, guild_id)

        )
    """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        # create tasks table
        create_table(conn, sqlite3CreateGuildsTable)

        create_table(conn, sqlite3CreateUsersTable)

        create_table(conn, sqlite3CreateChannelsTable)
        conn.close()
    else:
        print("Error! cannot create the database connection.")
def UpdateUser(newUserData):
    database = r"discord.db"
    sqlite3UpdateUser = f"""
        UPDATE USER
        SET name = {newUserData.userName},
        santa = {newUserData.santa},
        WHERE id = {newUserData.userId}
        AND guild_id = {newUserData.userGuildId}
    """
    executeQuery(sqlite3UpdateUser)
def UpdateGuild(newGuildData):
    database = r"discord.db"
    sqlite3UpdateGuild = f"""
        UPDATE GUILD
        SET name = {newGuildData.guildName}
        WHERE id = {newGuildData.guildId}
    """
    executeQuery(database, sqlite3UpdateGuild)
def UpdateChannel(newChannelData):
    database = r"discord.db"
    sqlite3UpdateChannel = f"""
        UPDATE CHANNEL
        SET name = {newChannelData.channelName}
        WHERE id = {newChannelData.channelId}
        AND guild_id = {newChannelData.channelGuildId}
    """
    executeQuery(database, sqlite3UpdateChannel)
def InsertUser(newUserData):
    database = r"discord.db"
    sqlite3InsertUser = f"""
        INSERT INTO USER (id, name, santa, guild_id)
        VALUES
            {newUserData.userId},
            {newUserData.userName},
            {newUserData.santa},
            {newUserData.guild_id}
    """
    executeQuery(sqlite3InsertUser)
def InsertGuild(newGuildData):
    database = r"discord.db"
    sqlite3InsertGuild = f"""
        INSERT INTO GUILD (id, name)
        VALUES
        {newGuildData.guildId},
        {newGuildData.guildName}
    """
    executeQuery(sqlite3InsertGuild)
def InsertChannel(newChannelData):
    database = r"discord.db"
    sqlite3InsertChannel = f"""
        INSERT INTO CHANNEL (id, name, guild_id)
        VALUES
            {newChannelData.channelId},
            {newChannelData.channelName},
            {newChannelData.channelGuildId}
    """
    executeQuery(sqlite3InsertChannel)
