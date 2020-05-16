import discord
import markovify
import time
import os
import json

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
        await message.channel.send("Blame Rob. These are generated from the last 100,000 messages in General Chat (ish)")
        if os.path.exists('lom.msg'):
            lom = open('lom.msg', 'r')
            stuff = json.loads(lom.read())
            for thing in stuff:
                if thing[0] == message.author.id:
                    if m_text is "":
                        m_text = thing[1] + ". "
                    else:
                        m_text = m_text + thing[1] + ". "
        else:        
            messages = await message.channel.history(limit=100000).flatten()
            big_array = []
            lom = open('lom_{}'.format(time.time()), 'w')
            for m in messages:
                if m.content.startswith('!markovme'):
                    continue
                tu = (m.author.id, m.content)
                big_array.append(tu)
                if m.author.id == message.author.id:
                    if m_text is "":
                        m_text = m.content + ". "
                    else:
                       m_text = m_text + m.content + ". "
            output_file = open('{}_{}'.format(message.author.nick, time.time()), 'w')
            output_file.write(m_text)
            lom.write(json.dumps(big_array))
            lom.flush()
            lom.close()
        text_model = markovify.Text(m_text)

        await message.channel.send("Well, something I once heard '{}' say is, \"{}\"".format(message.author.nick, text_model.make_sentence(tries=100)))


tfile = open('token', 'r')
tok = tfile.read()

client.run(tok)
