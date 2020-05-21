#!/usr/bin/env python3
import discord
import markovify
import time
import os
import json
import codecs
import sys

async def markovme(message):
    m_text = ""
    args = message.content.split(' ')
    numSentences = 1
    stateSize = 2
    if len(args) > 1:
        try:
            numSentences = int(args[1])
        except:
            return
    if len(args) > 2:
        try:
            stateSize = int(args[2])
        except:
            return
    print("markoving ", message.author.id)
    file_name = 'person_messages_{}.msg'.format(message.author.id)
    if os.path.exists(file_name):
        lom = codecs.open(file_name, 'r', encoding="utf-8")
        stuff = json.loads(lom.read())
        for thing in stuff:
            m_text += thing + "\n"
    elif os.path.exists('channel_messages_{}.msg'.format(message.channel.id)):
        lom = codecs.open('channel_messages_{}.msg'.format(message.channel.id), 'r', encoding="utf-8")
        stuff = json.loads(lom.read())
        for thing in stuff:
            if thing[0] == message.author.id:
                m_text += thing[1] + "\n"
    else:        
        lom = codecs.open('channel_messages_{}.msg'.format(message.channel.id), 'w', encoding="utf-8")
        lom.flush()
        await message.channel.send("Hold up, gathering some data...")
        messages = await message.channel.history(limit=100000).flatten()
        big_array = []
        for m in messages:
            if m.author.id == client.user.id:
                continue
            if m.content.startswith('!markovme'):
                continue
            tu = (m.author.id, m.content)
            big_array.append(tu)
            if m.author.id == message.author.id:
                m_text += m.content + "\n"
        lom.write(json.dumps(big_array))
        lom.flush()
        lom.close()
    text_model = markovify.NewlineText(m_text, state_size=stateSize)

    said = ""
    for i in range(numSentences):
        sent = text_model.make_sentence(tries=200)
        if sent is None:
            continue
        else:
            if "@" in sent:
                continue
            if i == numSentences - 1:
                said += "{}.".format(sent)
            else:
                said += "{}. ".format(sent)
    if said == "":
        await message.channel.send("Couldn't markov for ya with those arguments.")
    else:
        await message.channel.send("'{}' said, \"{}\"".format(message.author.nick, said))

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in at {}'.format(time.time()))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!markovme'):
        await markovme(message)
    if message.content.startswith('!markovthem'):
        m_text = ""
        data = message.content.split(' ')
        if len(data) < 2:
            return
        personId = int(data[1][3:data[1].find('>')])
        personNick = ""
        for guild in client.guilds:
            for memb in guild.members:
                if memb.id == personId:
                    personNick = memb.nick        
        numSentences = 1
        stateSize = 2
        if len(data) > 2:
            try:
                numSentences = int(data[2])
            except:
                return
        if len(data) > 3:
            try:
                stateSize = int(data[3])
            except:
                return        
        file_name = 'person_messages_{}.msg'.format(personId)
        if os.path.exists(file_name):
            lom = codecs.open(file_name, 'r', encoding="utf-8")
            stuff = json.loads(lom.read())
            for thing in stuff:
                m_text += thing + "\n"
            text_model = markovify.NewlineText(m_text, state_size=stateSize)
            said = ""
            for i in range(numSentences):
                sent = text_model.make_sentence(tries=200)
                if sent is None:
                    continue
                else:
                    if "@" in sent:
                        continue
                    if i == numSentences - 1:
                        said += "{}.".format(sent)
                    else:
                        said += "{}. ".format(sent)
            if said == "":
                await message.channel.send("Couldn't markov for ya with those arguments.")
            else:
                await message.channel.send("'{}' said, \"{}\"".format(personNick, said))            
        else:
            await message.channel.send("You need to spy on them first")
            return            
    if message.content.startswith('!markovhelp'):
        await message.channel.send("Rob wrote this. Use !markovme to have a markov chain generated based on your chat.")        
    if message.content.startswith('!spy'):
        data = message.content.split(' ')
        if len(data) < 2:
            return
        personId = int(data[1][3:data[1].find('>')])
        personNick = ""
        for guild in client.guilds:
            for memb in guild.members:
                if memb.id == personId:
                    personNick = memb.nick        
        file_name = 'person_messages_{}.msg'.format(personId)
        if os.path.exists(file_name):
            await message.channel.send("Already spied on them, you're gucci")
        else:
            await message.channel.send("Okay, I'm spying on {}. This takes forever.".format(personNick))
            lom = codecs.open(file_name, 'w', encoding="utf-8")
            big_array = []
            for guild in client.guilds:
                for chan in guild.text_channels:
                    messages = await chan.history(limit=100000).flatten()
                    for m in messages:
                        if "markov" in m.content:
                            continue
                        if m.author.id == personId:
                            big_array.append(m.content)
            lom.write(json.dumps(big_array))
            lom.flush()
            lom.close()
            print("Finished spying on {}".format(personNick))
        

tok = ""
if os.path.exists('token'):
    tfile = open('token', 'r')
    tok = tfile.read()
else:
    tok = os.environ['DISCORD_TOKEN']

if tok == "":
    print("No token provided", file=sys.stderr)

client.run(tok)
