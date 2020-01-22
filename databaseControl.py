import sqlite3
import discord
from sqlite3 import Error
database = r"discord.db"
def create_connection(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as e:
        print(e)

    return conn

class User:
    def __init__(self, id, name, guild_id, santa):
        self.userId = id
        self.userName = name
        self.userGuildId = guild_id
        self.santa = santa
class Guild:
    def __init__(self, id, name):
        self.guildId = id
        self.guildName = name
class Channel:
    def __init__(self, id, name, readFrom,guild_id):
        self.channelName = name
        self.channelReadable = readFrom
        self.channelId = id
        self.channelGuildId =guild_id
#Computes non SELECT statements like INSERT, DELETE, UPDATE
def executeQuery(query):
    conn = create_connection(database)
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(query)
        except Error as e:
            print(e)
        conn.commit()
        conn.close()
    else:
        print("Error! cannot create the database connection.")
#Returns the results of SELECT statements
def executeSelect(query):
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows
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
    #database = r"discord.db"
    sqlite3CreateGuildsTable = """
        CREATE TABLE IF NOT EXISTS guild (
            id integer PRIMARY KEY DESC,
            name text NOT NULL
        );
        """
    sqlite3CreateChannelsTable = """
        CREATE TABLE IF NOT EXISTS channel (
            id integer PRIMARY KEY DESC,
            name text NOT NULL,
            readFrom BOOLEAN,
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
            PRIMARY KEY (id, guild_id)

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
    #database = r"discord.db"
    sqlite3UpdateUser = f"""
        UPDATE USER
        SET name = \"{newUserData.userName}\",
        santa = {newUserData.santa}
        WHERE id = {newUserData.userId}
        AND guild_id = {newUserData.userGuildId}
    """
    executeQuery(sqlite3UpdateUser)
def UpdateGuild(newGuildData):
    #database = r"discord.db"
    sqlite3UpdateGuild = f"""
        UPDATE GUILD
        SET name = \"{newGuildData.guildName}\"
        WHERE id = {newGuildData.guildId}
    """
    executeQuery(sqlite3UpdateGuild)
def UpdateChannel(newChannelData):
    #database = r"discord.db"
    sqlite3UpdateChannel = f"""
        UPDATE CHANNEL
        SET name = \"{newChannelData.channelName}\",
        readFrom = {newChannelData.channelReadable}
        WHERE id = {newChannelData.channelId}
        AND guild_id = {newChannelData.channelGuildId}
    """
    executeQuery(sqlite3UpdateChannel)
def InsertUser(newUserData):
    #database = r"discord.db"
    sqlite3InsertUser = f"""
        INSERT INTO USER (id, name, santa, guild_id)
        VALUES
            ({newUserData.userId},
            \"{newUserData.userName}\",
            {newUserData.santa},
            {newUserData.userGuildId})
    """
    executeQuery(sqlite3InsertUser)
def InsertGuild(newGuildData):
    #database = r"discord.db"
    sqlite3InsertGuild = f"""
        INSERT INTO GUILD (id, name)
        VALUES
        ({newGuildData.guildId},
        \"{newGuildData.guildName}\");
    """

    executeQuery(sqlite3InsertGuild)
def InsertChannel(newChannelData):
    #database = r"discord.db"
    sqlite3InsertChannel = f"""
        INSERT INTO CHANNEL (id, name,readFrom, guild_id)
        VALUES
            ({newChannelData.channelId},
            \"{newChannelData.channelName}\",
            {newChannelData.channelReadable},
            {newChannelData.channelGuildId})
    """
    executeQuery(sqlite3InsertChannel)
#returns all user tuples of a given guild
def SelectAllUsers(guildId):

    sqlite3SelectUsers = f"""
        SELECT *
        FROM User
        WHERE guild_id = {guildId}
    """
    return executeSelect(sqlite3SelectUsers)
#returns all guild tuples
def SelectAllGuilds():
    #database = r"discord.db"
    sqlite3SelectGuilds = f"""
        SELECT *
        FROM GUILD
    """
    return executeSelect(sqlite3SelectGuilds)
#returns all channel tuples of a given guild
def SelectAllChannels(guildId):
    sqlite3SelectChannels = f"""
        SELECT *
        FROM CHANNEL
        WHERE guild_id = {guildId}
    """
    return executeSelect(sqlite3SelectChannels)
def SelectSanta(guildId):
    sqlite3SelectUsers = f"""
        SELECT *
        FROM User
        WHERE guild_id = {guildId}
        AND santa = true
    """
    return executeSelect(sqlite3SelectUsers)
#Query to select single guild based off primary key
def SelectGuild(guildId):
    sqlite3SelectGuild = f"""
        SELECT *
        FROM Guild
        WHERE id = {guildId}
        """
    #Returns single guild tuple
    return executeSelect(sqlite3SelectGuild)
#Query to select single User based off primary keys
def SelectUser(userId, guildId):

    sqlite3SelectUser = f"""
        SELECT *
        FROM User
        WHERE guild_id = {guildId}
        AND id = {userId}
    """
    #Returns single user tuple
    return executeSelect(sqlite3SelectUser)
#query to select a single user who is in a secret santa list
def SelectSantaUsers():
    sqlite3SelectSantaUser = f"""
        SELECT *
        FROM User
        WHERE santa = True
        """
    return executeSelect(sqlite3SelectSantaUser)
#query to select single channel based off primary keys
def SelectChannel(channelId, guildId):
    sqlite3SelectChannel = f"""
        SELECT *
        FROM CHANNEL
        WHERE id = {channelId}
        AND guild_id = {guildId}
    """
    #Returns single channel tuple from above query
    return executeSelect(sqlite3SelectChannel)
