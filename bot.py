# Work with Python 3.6
import discord
import time
import asyncio
import functions
#TOKEN = 'NjMwODE5NTk1Mzc2MTMyMTM5.XdDVAQ.hkTME3OmvmqFnlNqcg0HCKZnQSU'
TOKEN = 'NjQ3NTY1Njk1NDI0NjU5NDg3.XgKlsg.hk78CHf_6zL1iLV1p8tzoU4Ll7I'
#TOKEN = 'NjMwODE5NTk1Mzc2MTMyMTM5.XZuLOw.JBPbCurmDyquUzqNu7Q7FhRTcmw'
client = discord.Client()

messages = joined = 0
joinedSanta = []
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
            if(str(message.author) in joinedSanta):
                msg = f"{message.author.mention} is already in the Secret Santa list"
                await message.channel.send(msg)
            else:
                joinedSanta.append(str(message.author))
                msg = f"Added {message.author.mention} to Secret Santa list"
                await message.channel.send(msg)
        if message.content.startswith('!santa Leave'):
            if(str(message.author) in joinedSanta):
                msg = f"Removed {message.author.mention} from Secret Santa list"
                joinedSanta.remove(str(message.author))
                await message.channel.send(msg)
            else:
                msg = f"{message.author.mention} is not in the Secret Santa list"
                await message.channel.send(msg)
        if message.content.startswith('!hello'):
            msg = f"Hello {message.author.mention}"
            await message.channel.send(msg)

        #if message.content.startswith('!users'):
        #    msg = f"""# of Members {gid.member_count}"""
        #    await message.channel.send(msg)


#@client.event
#async def on_member_join(member):
#    global joined
#    joined += 1
#    welcome = client.get_channel(570466644611039244)
#    msg = f"""Welcome to my cave, {member.mention}!"""
#    await welcome.send(msg)

@client.event
async def on_ready():
        print("Logged in as", client.user.name, client.user.id)

client.loop.create_task(update_stats())
client.run(TOKEN)
