#!/usr/bin/env python3
import discord
import markovify
import time
import os
import json
import codecs

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in at {}'.format(time.time()))

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return

    m_text = ""
    if message.content.startswith('!markovme'):
        print("markoving ", message.author.id)
        await message.channel.send("Rob wrote this, yell at him. These are generated from the last 100,000 messages in whichever channel you sent this in ({})".format(message.channel.name))
        if os.path.exists('lom_{}.msg'.format(message.channel.id)):
            lom = codecs.open('lom_{}.msg'.format(message.channel.id), 'r', encoding="utf-8")
            stuff = json.loads(lom.read())
            for thing in stuff:
                if thing[0] == message.author.id:
                    m_text += thing[1] + "\n"
        else:        
            lom = codecs.open('lom_{}.msg'.format(message.channel.id), 'w', encoding="utf-8")
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
        text_model = markovify.NewlineText(m_text)

        await message.channel.send("'{}' said, \"{}\"".format(message.author.nick, text_model.make_sentence(tries=100)))


tfile = open('token', 'r')
tok = tfile.read()

client.run(tok)
