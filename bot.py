#!/usr/bin/env python3
import discord
import markovify
import time
import os
import json
import codecs
import sys

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in at {}'.format(time.time()))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    m_text = ""
    if message.content.startswith('!markovme'):
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
        await message.channel.send("Rob wrote this, yell at him. These are generated from the last 100,000 messages in whichever channel you sent this in ({})".format(message.channel.name))
        if os.path.exists('channel_messages_{}.msg'.format(message.channel.id)):
            lom = codecs.open('channel_messages_{}.msg'.format(message.channel.id), 'r', encoding="utf-8")
            stuff = json.loads(lom.read())
            for thing in stuff:
                if thing[0] == message.author.id:
                    m_text += thing[1] + "\n"
        else:        
            lom = codecs.open('channel_messages_{}.msg'.format(message.channel.id), 'w', encoding="utf-8")
            lom.flush()
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

        for i in range(numSentences):
            said = text_model.make_sentence(tries=100)
            if said is None:
                await message.channel.send("Couldn't markov for ya with those arguments.")
            else:
                await message.channel.send("'{}' said, \"{}\"".format(message.author.nick, said))


tok = ""
if os.path.exists('token'):
    tfile = open('token', 'r')
    tok = tfile.read()
else:
    tok = os.environ['DISCORD_TOKEN']

if tok == "":
    print("No token provided", file=sys.stderr)

client.run(tok)
