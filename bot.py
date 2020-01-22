# Work with Python 3.6
import discord
import time
import asyncio
import functions
from databaseControl import *
#TOKEN = 'NjMwODE5NTk1Mzc2MTMyMTM5.XdDVAQ.hkTME3OmvmqFnlNqcg0HCKZnQSU'
TOKEN = 'NjQ3NTY1Njk1NDI0NjU5NDg3.XiKfkQ.myHUG3GF0yCd7NWVqJcei7GlJzU'
#TOKEN = 'NjMwODE5NTk1Mzc2MTMyMTM5.XZuLOw.JBPbCurmDyquUzqNu7Q7FhRTcmw'
client = discord.Client()
messages = joined = 0


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")
            messages = 0
            joined = 0
            await asyncio.sleep(60)
        except Exception as e:
            print(e)
            await asyncio.sleep(60)

@client.event
async def on_message(message):
    global messages
    messages += 1

    #gid = client.get_guild(570466644611039242)
    channels = ["bot-commands", "general-chat", "programming"]

    if str(message.channel) in channels:
        #if message.author == client.user:
        #    return
        if message.content.startswith('!santa Join'):
            if(SelectUser(message.author.id,message.guild.id)[0][3]):
                msg = f"{message.author.mention} is already in the Secret Santa list"
                await message.channel.send(msg)
            else:
                UpdateUser(User(message.author.id, message.author.name, message.guild.id, True))
                msg = f"Added {message.author.mention} to Secret Santa list"
                await message.channel.send(msg)
        if message.content.startswith('!santa Leave'):
            if(SelectUser(message.author.id,message.guild.id)[0][3]):
                msg = f"Removed {message.author.mention} from Secret Santa list"
                UpdateUser(User(message.author.id, message.author.name, message.guild.id, False))
                await message.channel.send(msg)
            else:
                msg = f"{message.author.mention} is not in the Secret Santa list"
                await message.channel.send(msg)
        if message.content.startswith('!santa Begin'):
            santaList = SelectSantaUsers()
            incrementalList = [x for x in range(len(santaList))]
            santaIndices = santa(incrementalList)
            for pair in santaIndices:
                await get_user(santaList[pair[0]][0]).send(f"You are {santaList[pair[1]][1]}s secret santa!")
        if message.content.startswith('!santa Users'):
            santaList = SelectSantaUsers()
            for user in santaList:
                await message.channel.send(user[1])

        if message.content.startswith('!hello'):
            msg = f"Hello {message.author.mention}"
            await message.channel.send(msg)

        #if message.content.startswith('!users'):
        #    msg = f"""# of Members {gid.member_count}"""
        #    await message.channel.send(msg)


#@client.event
async def on_member_join(member):
    InsertUser(User(member.id,member.name,member.guild.id,False))

#    global joined
#    joined += 1
#    welcome = client.get_channel(570466644611039244)
#    msg = f"""Welcome to my cave, {member.mention}!"""
#    await welcome.send(msg)

@client.event
async def on_ready():
    print("Logged in as", client.user.name, client.user.id)
    #Upon startup, go through all guilds and update all tables accordingly
    guilds = client.guilds
    print(guilds)
    for g in guilds:
        #check is used to see if the guild already exists in our GUILD table
        check = SelectGuild(g.id)
        if(len(check)==0):
            newGuild = Guild(g.id,g.name)
            InsertGuild(newGuild)
        elif(check[0][1] != g.name):
            newGuild = Guild(g.id,g.name)
            UpdateGuild(newGuild)
        for u in g.members:
            #userCheck is used to see if our user already exists in our USER table
            userCheck = SelectUser(u.id,g.id)
            print(userCheck)
            if(len(userCheck)==0):
                newUser = User(u.id,u.name,g.id,False)
                InsertUser(newUser)
            elif(userCheck[0][1] != u.name):
                #if the user has new data, we update it
                UpdateUser(User(u.id,u.name,g.id, userCheck[0][3]))
        for c in g.channels:

            channelCheck = SelectChannel(c.id, g.id)
            print(channelCheck)
            if(len(channelCheck) == 0):
                newChannel = Channel(c.id,c.name,True,g.id)
                InsertChannel(newChannel)
                #if the channel has new data, update it
            elif(channelCheck[0][1] != c.name):
                newChannel = Channel(c.id,c.name,channelCheck[0][3],g.id)
                UpdateChannel(newChannel)

#client.loop.create_task(update_stats())
client.run(TOKEN)
